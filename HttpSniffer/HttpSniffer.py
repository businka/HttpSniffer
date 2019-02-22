from aiohttp import web, ClientSession


class HttpSniffer:
    target = None
    local_port = None
    proxy = None

    @classmethod
    async def sniffer(cls, request):
        try:
            print(request.method, request.raw_path)
            _request = dict(
                target=cls.target,
                raw_path=request.raw_path,
                headers=request.headers.copy(),
                data=await request.read(),
            )
            handler_name = 'on_{0}_request_{1}'.format(
                request.method.lower(), request.path.replace('/', '_').replace('.', '_'))
            if hasattr(request.app['sniffer'], handler_name):
                getattr(request.app['sniffer'], handler_name)(_request, request)
            async with ClientSession() as session:
                async with session.request(
                        request.method,
                        "{0}{1}".format(_request['target'], _request['raw_path']),
                        # params=request_params,
                        proxy=cls.proxy,
                        headers=_request['headers'],
                        # ssl=False,
                        # verify_ssl=False,
                        data=_request['data']) as response:
                    response_data = await response.read()

            response_headers = response.headers.copy()
            response_headers.popone('Content-Encoding', False)
            response_headers.popone('Transfer-Encoding', False)

            handler_name = 'on_{0}_response_{1}'.format(
                request.method.lower(), request.path.replace('/', '_').replace('.', '_'))
            if hasattr(request.app['sniffer'], handler_name):
                response_headers, response_data = getattr(request.app['sniffer'], handler_name)(
                    _request,
                    request,
                    response_headers,
                    response_data
                )
            if response_headers.popone('Cache-Control', False):
                response_headers.add('Cache-Control', 'no-cache, no-store, max-age=0')

            response_headers.popone('Content-Length', False)
            resp = web.Response(
                body=response_data,
                headers=response_headers,
                status=response.status,
            )
            return resp
        except Exception as e:
            return web.Response(body=str(e), status=400)

    @classmethod
    def run_proxy(cls, target, **kwargs):
        app = web.Application()
        app.router.add_route('*', '/{wildcard:.*}', cls.sniffer)
        cls.target = target
        cls.local_port = kwargs.get("port", 8080)
        cls.proxy = kwargs.get('proxy', None)
        app['sniffer'] = cls()
        web.run_app(app, port=cls.local_port)


if __name__ == '__main__':
    HttpSniffer.run_proxy('http://10.76.172.92', proxy="http://127.0.0.1:8888")
