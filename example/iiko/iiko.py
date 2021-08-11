from proxy import HttpSniffer
import xml.etree.ElementTree as ET
from uuid import uuid4


class Sniffer(HttpSniffer):
    folder = '/data'
    a = True

    def on_post_response_resto_services_update(self, _request, request, response_headers, response_data):
        root = ET.fromstring(response_data.decode('utf-8'))
        items_node = root.find('./returnValue/items')
        if len(items_node):
            a = response_data.decode('utf-8')
        else:
            if self.a:
                print('!!!!!!')
                order_number = '7'
                order_id = f'00000000-0000-0000-0000-00000000000{order_number}'
                with open('new_order.xml', 'r', encoding='utf-8') as file:
                    xml = file.read()
                item = xml.format(order_id=order_id, order_number=order_number, guest_id=str(uuid4()),
                                  item_id=str(uuid4()))
                item_root = ET.fromstring(item)
                items_node.append(item_root)
                response_data = ET.tostring(root, encoding='utf-8', method='xml')
                print(response_data)
                self.a = False
        return response_headers, response_data


if __name__ == '__main__':
    Sniffer.run_proxy('http://test-iiko-app:8080', port=8081) #, proxy="http://127.0.0.1:8888")  # Fiddler
