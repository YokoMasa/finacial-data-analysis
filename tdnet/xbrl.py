import xml.etree.ElementTree as ET

class Data:

    def __init__(self):
        self.name = ''
        self.text = ''
        self.context_ref = ''
        self.unit_ref = ''
        self.decimals = ''
    
    def is_forecast(self):
        if self.context_ref != '':
            if 'forecast' in self.context_ref.lower():
                return True
        return False

    def is_result(self):
        if self.context_ref != '':
            if 'result' in self.context_ref.lower():
                return True
        return False
    
    def __str__(self):
        return 'name: %s, text: %s, contextRef: %s, unitRef: %s, decimals: %s' % (self.name, self.text, self.context_ref, self.unit_ref, self.decimals)

class Xbrl:

    FINACIAL_DATA_NS_KEY = 'ix'
    NAME_KEY = 'name'
    CONTEXT_REF_KEY = 'contextRef'
    UNIT_REF_KEY = 'unitRef'
    DECIMALS_KEY = 'decimals'
    SIGN_KEY = 'sign'

    def __init__(self, xbrl_file_path=None, xbrl_string=None):
        self._ns = {}
        self.result_data = {}
        self.forecast_data = {}
        self.other_data = {}
        if xbrl_file_path:
            self._parse(xbrl_file_path)
        elif xbrl_string:
            self._parse_string(xbrl_string)
    
    def get_result_data_list(self, name):
        if name in self.result_data:
            return self.result_data[name]
        else:
            return []
    
    def get_forecast_data_list(self, name):
        if name in self.forecast_data:
            return self.forecast_data[name]
        else:
            return []  
    
    def get_data_list(self, name):
        result_list = []
        result_list.extend(self.get_forecast_data_list(name))
        result_list.extend(self.get_result_data_list(name))
        if name in self.other_data:
            result_list.extend(self.other_data[name])
        #for key in self.other_data:
        #    print(self.other_data[key][0])
        return result_list

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

    def _parse_string(self, xbrl_string):
        parser = ET.XMLPullParser(('start-ns', 'end'))
        parser.feed(xbrl_string)
        for event in parser.read_events():
            event_name = event[0]
            payload = event[1]
            if event_name == 'start-ns':
                self._handle_ns_event(payload)
            elif event_name == 'end':
                self._handle_end_event(payload)
    
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
            if not data:
                return

            if data.is_result():
                if data.name in self.result_data:
                    self.result_data[data.name].append(data)
                else:
                    self.result_data[data.name] = [data]
            elif data.is_forecast():
                if data.name in self.forecast_data:
                    self.forecast_data[data.name].append(data)
                else:
                    self.forecast_data[data.name] = [data]
            else:
                if data.name in self.other_data:
                    self.other_data[data.name].append(data)
                else:
                    self.other_data[data.name] = [data]
    
    def _create_data_obj_from_element(self, element):
        data = Data()

        # name
        raw_name = element.get(self.NAME_KEY)
        if raw_name:
            if ':' in element.tag:
                data.name = raw_name.split(':', maxsplit=1)[1]
            else:
                data.name = raw_name
        
        # text
        text = self._extract_text(element)
        if text:
            data.text = text
        else:
            return None

        # others
        data.context_ref = element.get(self.CONTEXT_REF_KEY, '')
        data.unit_ref = element.get(self.UNIT_REF_KEY, '')
        data.decimals = element.get(self.DECIMALS_KEY, '')

        # when minus
        sign = element.get(self.SIGN_KEY)
        if sign and sign == '-':
            data.text = '-' + data.text
            
        return data
    
    def _extract_text(self, element):
        if element.text:
            return element.text
        else:
            children = list(element)
            if 1 <= len(children):
                return self._extract_text(children[0])
            else:
                return None
    
    def _inspect_recursively(self, element, gen=1):
        print('gen: %d, tag: %s, text: %s' % (gen, element.tag, element.text))
        gen += 1
        for child in list(element):
            self._inspect_recursively(child, gen)

if __name__ == '__main__':
    xbrl = Xbrl('sample_xbrl/Summary/tse-acedjpsm-62790-20180405362790-ixbrl.htm')
    key = 'ChangeInOperatingIncome'
    code_key = 'SecuritiesCode'
    for data in xbrl.get_data_list(code_key):
        print('コード: %s' % (data.text, ))

    print('今期実績' + '*' * 40)
    for data in xbrl.get_result_data_list(key):
        print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))
    print('\r')
    print('次期予想' + '*' * 40)
    for data in xbrl.get_forecast_data_list(key):
        print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))
