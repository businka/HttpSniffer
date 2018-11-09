import HttpSniffer
import json
import re


class Web1C(HttpSniffer.HttpSniffer):
    folder = './data'

    def on_post_request__buh3_ru_RU_e1cib_logForm(self, request_target, request_raw_path, request_headers, request_data,
                                                  request):

        data = self.escape_res(request_data.decode())
        data = json.loads(data, encoding='utf-8')
        try:
            if data['root']['key'] == "Справочник.Контрагенты.ФормаСписка":
                self.save_data_to_file(
                    'ЗапросКонтрагентФормаСписка_{0}'.format(request_headers.get('pragma', 0)),
                    data
                )
        except KeyError:
            pass
        return request_target, request_raw_path, request_headers, request_data

    def on_post_request__buh3_ru_RU_e1cib_dlist(self, request_target, request_raw_path, request_headers, request_data,
                                                  request):
        data = self.escape_res(request_data.decode())
        data = json.loads(data, encoding='utf-8')
        try:
            # if data['root']['key'] == "Справочник.Контрагенты.ФормаСписка":
                self.save_data_to_file(
                    'ЗапросDlistКонтрагенты_{0}'.format(request_headers.get('pragma', 0)),
                    data
                )
        except KeyError:
            pass
        return request_target, request_raw_path, request_headers, request_data

    @staticmethod
    def escape_res(text):
        text = text.replace('\t', '\\t').replace('\r', '\\r')
        text = text.replace('\n', '\\n').replace(b'\xef\xbb\xbf'.decode(), '')
        text = re.sub(r"([^\"])undefined", r'\1"undefined"', text)
        return text

    def save_data_to_file(self, name, data):
        with open('{0}/{1}.json'.format(self.folder, name), "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    Web1C.run_proxy('http://10.76.172.92')  # , proxy="http://127.0.0.1:8888")
