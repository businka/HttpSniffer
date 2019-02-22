import xml.etree.ElementTree as ET


class JsonXmlSerializer:
    xml_types = ['array', 'object', 'str', 'num']
    data_types = dict(
        list='array',
        dict='object',
        str='str',
        int='num',
        float='num'
    )

    @classmethod
    def decode(cls, xml_string):
        root = ET.fromstring(xml_string)
        return cls.decode_node(root, None, '')

    @classmethod
    def decode_node(cls, node, parent, path):
        node_type = node.tag
        if node_type not in cls.xml_types:
            return
        name = node.attrib.get("name")
        result = getattr(cls, 'decode_{}'.format(node_type))(
            node, parent, path + '.' + name if name else node_type)
        if name:
            parent[name] = result
            return
        return result

    @classmethod
    def decode_array(cls, node, parent, path):
        result = []
        for elem in node:
            result.append(cls.decode_node(elem, None, path))
        return result

    @classmethod
    def decode_object(cls, node, parent, path):
        result = {}
        for elem in node:
            cls.decode_node(elem, result, path)
        return result

    @classmethod
    def decode_str(cls, node, parent, path):
        return node.text

    @classmethod
    def decode_num(cls, node, parent, path):
        return float(node.text) if node.text.find('.') >= 0 else int(node.text)

    @classmethod
    def encode(cls, data):
        root = cls.encode_node(data, None, None, '')
        return ET.tostring(root, encoding='utf-8', method='xml')

    @classmethod
    def encode_node(cls, node, name, parent, path):
        try:
            node_type = type(node).__name__
            if node_type not in cls.data_types:
                return
            node_type = cls.data_types[node_type]
            if parent is None:
                elem = ET.Element(node_type)
            else:
                elem = ET.SubElement(parent, node_type)
            if name:
                elem.set('name', name)
            getattr(cls, 'encode_{}'.format(node_type))(node, name, elem, path + '.' + name if name else node_type)
            return elem
        except Exception as err:
            raise('encode {0} error: {1}'.format(path, err))

    @classmethod
    def encode_array(cls, node, name, parent, path):
        for elem in node:
            cls.encode_node(elem, name, parent, path)

    @classmethod
    def encode_object(cls, node, name, parent, path):
        for name in node:
            cls.encode_node(node[name], name, parent, path)

    @classmethod
    def encode_str(cls, node, name, parent, path):
        parent.text = node

    @classmethod
    def encode_num(cls, node, name, parent, path):
        parent.text = str(node)


if __name__ == '__main__':
    # with open('example.xml', 'r', encoding='utf-8') as file:
    #     str1 = file.read()
    # data = JsonXmlSerializer.decode(str1)
    # print(data)
    data = {'jsonrpc': '2.0', 'error': {'code': -32700, 'message': '', 'details': 'Parse error (offset 307): Missing a closing quotation mark in string.', 'type': 'error', 'data': {'classid': '{f4101a18-9ea7-447d-9f98-9a951643f9f0}', 'error_code': -1, 'addinfo': None}}, 'id': None}
    str2 = JsonXmlSerializer.encode(data)
    print(str2)
