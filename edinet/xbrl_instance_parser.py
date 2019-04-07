from xml.etree.ElementTree import XMLPullParser
import xml.etree.ElementTree as ET

XBRLI_KEY = 'xbrli'
JPPFS_KEY = 'jppfs_cor'

def parse(xbrl_file_name):
    with open(xbrl_file_name, encoding='utf8') as file:
        parser = XMLPullParser(('end', 'start-ns'))
        line = file.readline()

        xbrli_ns_tag_set = False
        context_tag = ''
        instant_tag = ''

        jppfs_ns_tag_set = False
        net_sales_tag = ''          #売上
        operating_income_tag = ''   #営業利益
        ordinary_income_tag = ''    #経常利益
        profit_loss_tag = ''        #当期純利益
        profit_loss_old_tag = ''    #当期純利益（旧バージョン）netincome

        while line != '':
            parser.feed(line)
            for event in parser.read_events():
                event_type = event[0]
                if event_type == 'start-ns':
                    # 名前空間URI取得
                    ns_key = event[1][0]
                    ns_uri = event[1][1]
                    if ns_key == XBRLI_KEY:
                        context_tag = '{%s}context' % (ns_uri,)
                        instant_tag = '{%s}instant' % (ns_uri,)
                        xbrli_ns_tag_set = True

                    elif ns_key == JPPFS_KEY:
                        net_sales_tag = '{%s}NetSales' % (ns_uri,)
                        operating_income_tag = '{%s}OperatingIncome' % (ns_uri,)
                        ordinary_income_tag = '{%s}OrdinaryIncome' % (ns_uri,)
                        profit_loss_tag = '{%s}ProfitLoss' % (ns_uri,)
                        profit_loss_old_tag = '{%s}NetIncome' % (ns_uri,)
                        jppfs_ns_tag_set = True

                elif event_type == 'end' and xbrli_ns_tag_set and jppfs_ns_tag_set:
                    element = event[1]

                    tag = element.tag
                    text = element.text
                    decimal = element.get('decimals', '')
                    context_ref = element.get('contextRef', '')

                    if context_ref == 'CurrentYearInstant':
                        pass
                    elif context_ref == 'CurrentYearDuration':
                        if tag == net_sales_tag:
                            print('売上: %s, decimal: %s' % (text, decimal))
                        elif tag == operating_income_tag:
                            print('営業利益: %s, decimal: %s' % (text, decimal))
                        elif tag == ordinary_income_tag:
                            print('経常利益: %s, decimal: %s' % (text, decimal))
                        elif tag == profit_loss_tag:
                            print('当期純利益: %s, decimal: %s' % (text, decimal))
                        elif tag == profit_loss_old_tag:
                            print('当期純利益: %s, decimal: %s' % (text, decimal))
                            
            line = file.readline()

def parse2(xbrl_file_name):
    element_tree = ET.parse(xbrl_file_name)
    root = element_tree.getroot()
    for e in root.findall('{http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2018-02-28/jppfs_cor}NetSales'):
        print(e.tag)
    
    for e in root.findall('{http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2018-02-28/jppfs_cor}TotalChangesOfItemsDuringThePeriod'):
        print(e)
    
    for e in root.findall('{http://disclosure.edinet-fsa.go.jp/taxonomy/jppfs/2018-02-28/jppfs_cor}NetAssets'):
        print(e)


if __name__ == '__main__':
    parse('sample_xbrl\PublicDoc\jpcrp030000-asr-001_E05033-000_2018-12-31_01_2019-03-27.xbrl')