import xml.etree.ElementTree as ET

class Xbrl:

    def __init__(self, xbrl_file_path):
        self._ns = {}
        self._parse(xbrl_file_path)

    def _parse(self, xbrl_file_path):
        with open(xbrl_file_path, encoding='utf8') as file:
            parser = ET.XMLPullParser(('start-ns', 'end'))
            line = file.readline()

            while line != '':
                parser.feed(line)
                for event in parser.read_events():
                    event_name = event[0]
                    if event_name == 'start-ns':
                        ns_key = event[1][0]
                        ns_uri = event[1][1]
                        self._ns[ns_key] = ns_uri
                        if ns_key == 'ix':
                            self._ix_prefix = '{%s}' % (ns_uri, )

                    elif event_name == 'end':
                        if not self._ix_prefix:
                            continue

                        element = event[1]
                        if element.tag.startswith(self._ix_prefix):
                            print(element.get('name'))

                line = file.readline()
        
        print(self._ns)
    

if __name__ == '__main__':
    xbrl = Xbrl('sample_xbrl/Summary/tse-acedjpsm-62790-20180405362790-ixbrl.htm')
