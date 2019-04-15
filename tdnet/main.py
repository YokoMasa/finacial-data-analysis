import datetime

import tdnet
import xbrl_extractor

if __name__ == '__main__':
    date = datetime.datetime(2019, 4, 9)
    result = tdnet.search(date, date, '短信')
    if len(result) != 0:
        doc = result[0]
        print('docname: %s' % (doc.doc_name))

        zipfilename = tdnet.download_xbrl(doc)

        xbrl = xbrl_extractor.extract(zipfilename)
        key = 'ChangeInOperatingIncome'
        print('今期実績' + '*' * 40)
        for data in xbrl.get_result_data_list(key):
            print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))
        print('\r')
        print('次期予想' + '*' * 40)
        for data in xbrl.get_forecast_data_list(key):
            print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))