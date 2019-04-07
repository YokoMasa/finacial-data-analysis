from xml.etree.ElementTree import XMLPullParser

class Xbrl:

    def __init__(self, xbrl_file_path):
        self._ns = {}

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
        
        print(self._ns)

if __name__ == '__main__':
    xbrl = Xbrl('sample_xbrl/Summary/tse-acedjpsm-62790-20180405362790-ixbrl.htm')
