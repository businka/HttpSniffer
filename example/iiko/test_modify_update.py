import xml.etree.ElementTree as ET
from uuid import uuid4


def parse_response_data(data):
    root = ET.fromstring(data.decode('utf-8'))
    items_node = root.find('./returnValue/items')
    order_number = '16'
    order_id = f'00000000-0000-0000-0000-00000000000{order_number}'
    with open('new_order.xml', 'r', encoding='utf-8') as file:
        xml = file.read()
    item = xml.format(order_id=order_id, order_number=order_number, guest_id=str(uuid4()), item_id=str(uuid4()))
    item_root = ET.fromstring(item)
    items_node.append(item_root)
    a = ET.tostring(root, encoding='utf-8', method='xml')
    pass


def parse_wireshark_result():
    # if 'null' in entities_node.attrib:
    #     a = 1
    # else:
    #     a = 2
    a = '''01d0  35 31 2d 61 32 31 39 2d 66 61 62 30 36 36 66 62   51-a219-fab066fb'''
    rows = a.split('\n')
    res = ''
    for elem in rows:
        if len(elem) > 56:
            res += elem[56:]
    pass


if __name__ == '__main__':
    with open('response_update_items.xml', 'rb') as file:
        parse_response_data(file.read())
