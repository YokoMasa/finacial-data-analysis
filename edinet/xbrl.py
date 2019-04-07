from enum import Enum
from xml.etree.ElementTree import XMLPullParser
import xml.etree.ElementTree as ET

class Data:

    def __init__(self, tag, text, context, decimals=None, unit=None):
        self.tag = tag
        self.text = text
        self.context = context
        self.decimals = decimals
        self.unit = unit
    
    def __str__(self):
        return 'tag: %s, text: %s, context: %s' % (self.tag, self.text, self.context)

CONTEXT_TAG = 'context'
FILING_DATE_INSTANT_ID = 'FilingDateInstant'

CONTEXT_REF_KEY = 'contextRef'
DECIMALS_KEY = 'decimals'
UNIT_REF_KEY = 'unitRef'

class Xbrl:

    CONTEXT_CURRENT_YEAR_INSTANT = 'CurrentYearInstant'
    CONTEXT_PRIOR_1_YEAR_INSTANT = 'Prior1YearInstant'
    CONTEXT_PRIOR_2_YEAR_INSTANT = 'Prior2YearInstant'
    CONTEXT_PRIOR_3_YEAR_INSTANT = 'Prior3YearInstant'
    CONTEXT_PRIOR_4_YEAR_INSTANT = 'Prior4YearInstant'

    CONTEXT_CURRENT_YEAR_DURATION = 'CurrentYearDuration'
    CONTEXT_PRIOR_1_YEAR_DURATION = 'Prior1YearDuration'
    CONTEXT_PRIOR_2_YEAR_DURATION = 'Prior2YearDuration'
    CONTEXT_PRIOR_3_YEAR_DURATION = 'Prior3YearDuration'
    CONTEXT_PRIOR_4_YEAR_DURATION = 'Prior4YearDuration'

    NS_JPPFS = 'jppfs_cor'
    NS_JPDEI = 'jpdei_cor'
    NS_XBRLI = 'xbrli'

    def __init__(self, xbrl_file_path):
        self.filing_date = ''
        self._ns = {}

        element_tree = ET.parse(xbrl_file_path)
        self._xbrl_root = element_tree.getroot()
        self._prepare_basic_data(xbrl_file_path)
    
    def _prepare_basic_data(self, xbrl_file_path):
        # 名前空間取得
        with open(xbrl_file_path, encoding='utf8') as file:
            parser = XMLPullParser(('start-ns',))
            line = file.readline()

            while line != '':
                parser.feed(line)
                for event in parser.read_events():
                    ns_key = event[1][0]
                    ns_uri = event[1][1]
                    self._ns[ns_key] = ns_uri
                line = file.readline()
        
        # Filing date取得
        ns_filter = {self.NS_XBRLI: self._ns[self.NS_XBRLI]}
        path = "./xbrli:context[@id='%s']/xbrli:period/xbrli:instant" % (FILING_DATE_INSTANT_ID, )
        filing_date_element = self._xbrl_root.find(path, ns_filter)
        if filing_date_element != None:
            self.filing_date = filing_date_element.text
    
    def _list_elements(self, tag_name, ns_key):
        if ns_key not in self._ns:
            return []

        tag = '{%s}%s' % (self._ns[ns_key], tag_name)
        return self._xbrl_root.findall(tag)
    
    def list_data(self, tag_name, ns_key, context=None):
        data_array = []
    
        for element in self._list_elements(tag_name, ns_key):
            if context and context == element.get(CONTEXT_REF_KEY):
                continue
            
            data = Data(tag_name, element.text, element.get(CONTEXT_REF_KEY), element.get(DECIMALS_KEY), element.get(UNIT_REF_KEY))
            data_array.append(data)
        return data_array
    
    def find_data(self, tag_name, ns_key, context=None):
        for element in self._list_elements(tag_name, ns_key):
            if context and context != element.get(CONTEXT_REF_KEY):
                continue
            
            return Data(tag_name, element.text, element.get(CONTEXT_REF_KEY), element.get(DECIMALS_KEY), element.get(UNIT_REF_KEY))
        return None

    def find_finacial_data(self, tag_name, context=None):
        return self.find_data(tag_name, self.NS_JPPFS, context)

    def get_ns_dict(self):
        return self._ns 

if __name__ == '__main__':
    xbrl = Xbrl('sample_xbrl\PublicDoc\jpcrp030000-asr-001_E05033-000_2018-12-31_01_2019-03-27.xbrl')
    print('filing date: %s' % (xbrl.filing_date,))
    print(xbrl.find_finacial_data('OperatingIncome', Xbrl.CONTEXT_PRIOR_1_YEAR_DURATION))