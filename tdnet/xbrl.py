import xml.etree.ElementTree as ET

class Data:

    def __init__(self):
        self.name = ''
        self.text = ''
        self.context_ref = ''
        self.unit_ref = ''
        self.decimals = ''
    
    def __str__(self):
        return 'name: %s, text: %s, contextRef: %s, unitRef: %s, decimals: %s' % (self.name, self.text, self.context_ref, self.unit_ref, self.decimals)

class Xbrl:

    FINACIAL_DATA_NS_KEY = 'ix'
    NAME_KEY = 'name'
    CONTEXT_REF_KEY = 'contextRef'
    UNIT_REF_KEY = 'unitRef'
    DECIMALS_KEY = 'decimals'

    def __init__(self, xbrl_file_path):
        self._ns = {}
        self.data = {}
        self._parse(xbrl_file_path)

    def _parse(self, xbrl_file_path):
        with open(xbrl_file_path, encoding='utf8') as file:
            parser = ET.XMLPullParser(('start-ns', 'end'))
            line = file.readline()

            while line != '':
                parser.feed(line)
                for event in parser.read_events():
                    event_name = event[0]
                    payload = event[1]
                    if event_name == 'start-ns':
                        self._handle_ns_event(payload)
                    elif event_name == 'end':
                        self._handle_end_event(payload)
                line = file.readline()
    
    def _handle_ns_event(self, ns_data):
        ns_key = ns_data[0]
        ns_uri = ns_data[1]
        self._ns[ns_key] = ns_uri
        if ns_key == self.FINACIAL_DATA_NS_KEY:
            self._ix_prefix = '{%s}' % (ns_uri, )
    
    def _handle_end_event(self, element):
        if not self._ix_prefix:
            return
        if element.tag.startswith(self._ix_prefix):
            data = self._create_data_obj_from_element(element)
            if data:
                print(data)
    
    def _create_data_obj_from_element(self, element):
        data = Data()

        # name
        raw_name = element.get(self.NAME_KEY)
        if raw_name:
            if ':' in element.tag:
                data.name = raw_name.split(':', maxsplit=1)[1]
            else:
                data.name = raw_name
        
        #text
        if element.text:
            data.text = element.text
        else:
            return None

        # others
        data.context_ref = element.get(self.CONTEXT_REF_KEY)
        data.unit_ref = element.get(self.UNIT_REF_KEY)
        data.decimals = element.get(self.DECIMALS_KEY)
        return data

if __name__ == '__main__':
    xbrl = Xbrl('sample_xbrl/Summary/tse-acedjpsm-62790-20180405362790-ixbrl.htm')
