import libxml2
import cStringIO
import exceptions

def process_introspection_data(data):
    method_map = {}

    XMLREADER_START_ELEMENT_NODE_TYPE = 1
    XMLREADER_END_ELEMENT_NODE_TYPE = 15

    stream = cStringIO.StringIO(data.encode('utf-8'))
    input_source = libxml2.inputBuffer(stream)
    reader = input_source.newTextReader("urn:introspect")

    ret = reader.Read()
    current_iface=''
    current_method=''
    current_sigstr = ''
    
    while ret == 1:
        name = reader.LocalName()
        if reader.NodeType() == XMLREADER_START_ELEMENT_NODE_TYPE:
            if name == 'interface':
                current_iface = reader.GetAttribute('name')
            elif name == 'method':
                current_method = reader.GetAttribute('name')
                if reader.IsEmptyElement():
                    method_map[current_iface + '.' + current_method] = '' 
                    current_method = ''
                    current_sigstr = ''
                    
            elif name == 'arg':
                direction = reader.GetAttribute('direction')

                if not direction or direction == 'in':
                    current_sigstr = current_sigstr + reader.GetAttribute('type')

        elif reader.NodeType() == XMLREADER_END_ELEMENT_NODE_TYPE:
            if name == 'method':
                method_map[current_iface + '.' + current_method] = current_sigstr 
                current_method = ''
                current_sigstr = ''

         
        ret = reader.Read()

    if ret != 0:
        raise exceptions.IntrospectionParserException(data)

    return method_map
