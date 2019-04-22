import time
import datetime

import tdnet
import xbrl_extractor

def main():
    date = datetime.datetime(2019, 4, 3)
    result = tdnet.search(date, date, '短信')
    for doc in result:
        time.sleep(3)
        zipfilename = tdnet.download_xbrl(doc)
        if not zipfilename:
            print('failed to download xbrl')
            continue

        xbrl = xbrl_extractor.extract(zipfilename)
        if not xbrl:
            print('no xbrl')
            continue

        data_list = xbrl.get_data_list('SecuritiesCode')
        if data_list:
            print('コード: %s' % (data_list[0].text, ))
        
        data_list = xbrl.get_data_list('CompanyName')
        if data_list:
            print('企業名: %s' % (data_list[0].text, ))

        key = 'ChangeInOperatingIncome'
        print('---今期実績---')
        for data in xbrl.get_result_data_list(key):
            print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))

        print('---次期予想---')
        for data in xbrl.get_forecast_data_list(key):
            print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))
        
        print('\r')

if __name__ == '__main__':
    main()
    