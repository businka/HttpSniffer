from aiohttp import web, ClientSession
from urllib.parse import urlparse, urljoin, urlsplit, urlunparse


class HttpSniffer:

    @classmethod
    def modify_requrst_to_target(cls, _request, request):
        local = urlparse(str(request.url))
        _request['raw_url'] = local
        target = request.app['target']
        _request['dest_url'] = local._replace(scheme=target.scheme, netloc=target.netloc)
        if 'headers' not in _request:
            return
        local_url = f'{local.scheme}{local.netloc}'
        target_url = f'{target.scheme}{target.netloc}'
        for elem in _request['headers']:
            _request['headers'][elem].replace(local_url, target_url)
            _request['headers'][elem].replace(local.netloc, target.netloc)

    @classmethod
    async def sniffer(cls, request):
        try:
            handler_suffix = request.path.replace('/', '_').replace('.', '_')
            print(f'{request.method} {request.raw_path} ({handler_suffix})')
            _request = dict(
                raw_path=request.raw_path,
                headers=request.headers.copy(),
                data=await request.read(),
            )
            cls.modify_requrst_to_target(_request, request)

            handler_name = f"on_{request.method.lower()}_request{handler_suffix}"
            if hasattr(request.app['sniffer'], handler_name):
                getattr(request.app['sniffer'], handler_name)(_request, request)

            async with ClientSession(requote_redirect_url=False) as session:
                url = urlunparse(_request['dest_url'])
                async with session.request(
                        request.method,
                        url,
                        # params=request_params,
                        proxy=request.app['proxy'],
                        headers=_request['headers'],

                        # ssl=False,
                        # verify_ssl=False,
                        data=_request['data']) as response:
                    response_data = await response.read()

            response_headers = response.headers.copy()
            response_headers.popone('Content-Encoding', False)
            response_headers.popone('Transfer-Encoding', False)

            handler_name = f'on_{request.method.lower()}_response{handler_suffix}'
            print(handler_name)
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
            print(e)
            return web.Response(body=str(e), status=400)

    @classmethod
    def run_proxy(cls, target, **kwargs):
        app = web.Application()
        app.router.add_route('*', '/{wildcard:.*}', cls.sniffer)
        local_port = kwargs.get('port', 8080)
        local = 'localhost' if local_port == 80 else f"localhost:{local_port}"
        app['target'] = urlparse(target)
        app['local'] = urlparse(local)
        app['proxy'] = kwargs.get('proxy', None)
        app['sniffer'] = cls()
        web.run_app(app, host='localhost', port=local_port)


if __name__ == '__main__':
    HttpSniffer().run_proxy('http://10.76.172.92', proxy='http://127.0.0.1:8888')
