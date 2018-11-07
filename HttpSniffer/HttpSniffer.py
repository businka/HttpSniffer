from aiohttp import web, ClientSession


class HttpSniffer:
    target = None
    proxy = None

    @classmethod
    async def sniffer(cls, request):
        print(request.method, request.raw_path)
        request_target = cls.target
        request_path = request.path
        request_params = request.query
        request_headers = request.headers.copy()
        request_data = await request.read()
        handler_name = 'on_{0}_request_{1}'.format(request.method.lower(), request.path.replace('/', '_'))
        if hasattr(request.app['sniffer'], handler_name):
            target, path, request_params, headers, data = getattr(request.app['sniffer'], handler_name)(
                request_target,
                request_path,
                request_params,
                request_headers,
                request_data
            )
        async with ClientSession() as session:
            async with session.request(
                    request.method,
                    "{0}{1}".format(request_target, request_path),
                    params=request_params,
                    proxy=cls.proxy,
                    headers=request_headers,
                    data=request_data) as response:
                response_data = await response.read()

        response_headers = response.headers.copy()
        response_headers.popone('Content-Encoding', False)
        response_headers.popone('Transfer-Encoding', False)

        handler_name = 'on_{0}_response_{1}'.format(request.method.lower(), request.path.replace('/', '_'))
        if hasattr(request.app['sniffer'], handler_name):
            response_headers, response_data = getattr(request.app['sniffer'], handler_name)(
                request_target,
                request_path,
                request_params,
                request_headers,
                request_data,
                response_headers,
                response_data
            )
        # if headers.popone('Cache-Control', False):
        #     headers.add('Cache-Control', 'no-cache, no-store, max-age=0')

        response_headers.popone('Content-Length', False)
        resp = web.Response(
            body=response_data,
            headers=response_headers,
            status=response.status,
        )
        return resp

    @classmethod
    def run_proxy(cls, target, **kwargs):
        app = web.Application()
        app.router.add_route('*', '/{wildcard:.*}', cls.sniffer)
        cls.target = target
        cls.sniffer = kwargs.get('proxy', None)
        app['sniffer'] = cls()
        web.run_app(app, port=kwargs.get("port"))


if __name__ == '__main__':
    HttpSniffer.run_proxy('http://10.76.172.92/', proxy="http://127.0.0.1:8888")
