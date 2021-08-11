from proxy import HttpSniffer
from example.Sbis.XmlJsonSerializer import JsonXmlSerializer
import json


class Sniffer(HttpSniffer):
    folder = '/data'

    def on_get_request_(self, _request, request):
        _request['headers'][':authority'] = 'test-online.sbis.ru'
        _request['headers'][':method'] = 'GET'
        _request['headers'][':path'] = '/'
        _request['headers'][':scheme'] = 'https'
        _request['headers'].pop('Host')
    # def on_post_request__auth_service_(self, _request, request):
    #     _request['data'] = JsonXmlSerializer.decode(_request['data'])
    #     _request['headers'].pop('content-length')
    #     _request['data'] = json.dumps(_request['data']).encode(encoding='utf-8')
    #
    # def on_post_response__auth_service_(self, _request, request, response_headers, response_data):
    #     response_data = json.loads(response_data.decode(), encoding='utf-8')
    #     response_data = JsonXmlSerializer.encode(response_data)
    #     return response_headers, response_data


if __name__ == '__main__':
    Sniffer.run_proxy('https://test-online.sbis.ru/')
    # Sniffer.run_proxy('https://test-online.sbis.ru', proxy="http://127.0.0.1:8888")   # Fiddler
