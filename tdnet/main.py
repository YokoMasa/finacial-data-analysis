import time
import datetime

import tdnet
import uho_catcher
from slack import Slack
from history import History

CODE = 'SecuritiesCode'
COMPANY_NAME = 'CompanyName'
FILING_DATE = 'FilingDate'
NET_SALES = 'ChangeInNetSales'
OPERATING_INCOME = 'ChangeInOperatingIncome'
ORDINARY_INCOME = 'ChangeInOrdinaryIncome'

class FinantialData:

    PERIOD_CURRENT_YEAR_DURATION = 'CurrentYearDuration'
    PERIOD_CURRENT_YEAR_INSTANT = 'CurrentYearInstant'
    PERIOD_PRIOR_YEAR_DURATION = 'PriorYearDuration'
    PERIOD_PRIOR_YEAR_INSTANT = 'PriorYearInstant'
    PERIOD_NEXT_YEAR_DURATION = 'NextYearDuration'
    PERIOD_NEXT_YEAR_INSTANT = 'NextYearInstant'

    UNIT_CONSOLIDATE = 'ConsolidatedMember'
    UNIT_NON_CONSOLIDATE = 'NonConsolidatedMember'

    TYPE_FORECAST = 'ForecastMember'
    TYPE_RESULT = 'ResultMember'

    def __init__(self, xbrl):
        self.xbrl = xbrl
    
    def get_data(self, name, period, unit, type):
        context = ('%s_%s_%s') % (period, unit, type)
        data_list = self.xbrl.get_data_list(name)
        for data in data_list:
            if data.context_ref == context:
                return data.text
    
    def get_forecast_duration_data(self, name, unit):
        return self.get_data(name, self.PERIOD_NEXT_YEAR_DURATION, unit, self.TYPE_FORECAST)

    def get_result_duration_data(self, name, unit):
        return self.get_data(name, self.PERIOD_CURRENT_YEAR_DURATION, unit, self.TYPE_RESULT)

def print_data(xbrl):
        print('---基本情報---')
        data = xbrl.get_data(CODE)
        if data:
            print('コード: %s' % (data.text, ))
        
        data = xbrl.get_data(COMPANY_NAME)
        if data:
            print('企業名: %s' % (data.text, ))

        data = xbrl.get_data(FILING_DATE)
        if data:
            print('提出日: %s' % (data.text, ))

        fd = FinantialData(xbrl)

        print('---連結---')
        data = fd.get_result_duration_data(NET_SALES, FinantialData.UNIT_CONSOLIDATE)
        if data:
            print('売上高前期比: %s' % (data, ))
     
        data = fd.get_result_duration_data(OPERATING_INCOME, FinantialData.UNIT_CONSOLIDATE)
        if data:
            print('営業利益前期比: %s' % (data, ))

        data = fd.get_result_duration_data(ORDINARY_INCOME, FinantialData.UNIT_CONSOLIDATE)
        if data:
            print('経常利益前期比: %s' % (data, ))
        
        data = fd.get_forecast_duration_data(NET_SALES, FinantialData.UNIT_CONSOLIDATE)
        if data:
            print('予想次期売上高前期比: %s' % (data, ))
     
        data = fd.get_forecast_duration_data(OPERATING_INCOME, FinantialData.UNIT_CONSOLIDATE)
        if data:
            print('予想次期営業利益前期比: %s' % (data, ))

        data = fd.get_forecast_duration_data(ORDINARY_INCOME, FinantialData.UNIT_CONSOLIDATE)
        if data:
            print('予想次期経常利益前期比: %s' % (data, ))


        print('---個別---')
        data = fd.get_result_duration_data(NET_SALES, FinantialData.UNIT_NON_CONSOLIDATE)
        if data:
            print('売上高前期比: %s' % (data, ))
     
        data = fd.get_result_duration_data(OPERATING_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
        if data:
            print('営業利益前期比: %s' % (data, ))

        data = fd.get_result_duration_data(ORDINARY_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
        if data:
            print('経常利益前期比: %s' % (data, ))
        
        data = fd.get_forecast_duration_data(NET_SALES, FinantialData.UNIT_NON_CONSOLIDATE)
        if data:
            print('予想次期売上高前期比: %s' % (data, ))
     
        data = fd.get_forecast_duration_data(OPERATING_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
        if data:
            print('予想次期営業利益前期比: %s' % (data, ))

        data = fd.get_forecast_duration_data(ORDINARY_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
        if data:
            print('予想次期経常利益前期比: %s' % (data, ))
        
        print('\r')

def print_diff(xbrl, previous_xbrl):
    text = '*' * 20 + '\r'
    text += '---基本情報---\r'
    print('---基本情報---')
    data = xbrl.get_data(CODE)
    if data:
        print('コード: %s' % (data.text, ))
        text += 'コード: %s\r' % (data.text, )
        
    data = xbrl.get_data(COMPANY_NAME)
    if data:
        print('企業名: %s' % (data.text, ))
        text += '企業名: %s\r' % (data.text, )
    
    data = xbrl.get_data(FILING_DATE)
    if data:
        print('今期提出日: %s' % (data.text, ))
        text += '今期提出日: %s\r' % (data.text, )

    data = previous_xbrl.get_data(FILING_DATE)
    if data:
        print('前期提出日: %s' % (data.text, ))
        text += '前期提出日: %s\r' % (data.text, )
    
    fd = FinantialData(xbrl)
    p_fd = FinantialData(previous_xbrl)

    print('---連結差分---')
    text += '\r---連結差分---\r'
    data = fd.get_result_duration_data(NET_SALES, FinantialData.UNIT_CONSOLIDATE)
    p_data = p_fd.get_forecast_duration_data(NET_SALES, FinantialData.UNIT_CONSOLIDATE)
    if data and p_data:
        diff = float(data) - float(p_data)
        print('売上高前期比差分: %f' % (diff, ))
        text += '売上高前期比差分: %f\r' % (diff, )
    
    data = fd.get_result_duration_data(OPERATING_INCOME, FinantialData.UNIT_CONSOLIDATE)
    p_data = p_fd.get_forecast_duration_data(OPERATING_INCOME, FinantialData.UNIT_CONSOLIDATE)
    if data and p_data:
        diff = float(data) - float(p_data)
        print('営業利益前期比差分: %f' % (diff, ))
        text += '営業利益前期比差分: %f\r' % (diff, )
    
    data = fd.get_result_duration_data(ORDINARY_INCOME, FinantialData.UNIT_CONSOLIDATE)
    p_data = p_fd.get_forecast_duration_data(ORDINARY_INCOME, FinantialData.UNIT_CONSOLIDATE)
    if data and p_data:
        diff = float(data) - float(p_data)
        print('経常利益前期比差分: %f' % (diff, ))
        text += '経常利益前期比差分: %f\r' % (diff, )

    print('---個別差分---')
    text += '\r---個別差分---\r'
    data = fd.get_result_duration_data(NET_SALES, FinantialData.UNIT_NON_CONSOLIDATE)
    p_data = p_fd.get_forecast_duration_data(NET_SALES, FinantialData.UNIT_NON_CONSOLIDATE)
    if data and p_data:
        diff = float(data) - float(p_data)
        print('売上高前期比差分: %f' % (diff, ))
        text += '売上高前期比差分: %f\r' % (diff, )
    
    data = fd.get_result_duration_data(OPERATING_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
    p_data = p_fd.get_forecast_duration_data(OPERATING_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
    if data and p_data:
        diff = float(data) - float(p_data)
        print('営業利益前期比差分: %f' % (diff, ))
        text += '営業利益前期比差分: %f\r' % (diff, )
    
    data = fd.get_result_duration_data(ORDINARY_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
    p_data = p_fd.get_forecast_duration_data(ORDINARY_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
    if data and p_data:
        diff = float(data) - float(p_data)
        print('経常利益前期比差分: %f' % (diff, ))
        text += '経常利益前期比差分: %f\r' % (diff, )
    
    print('---連結次期予想---')
    text += '\r---連結次期予想---\r'
    data = fd.get_forecast_duration_data(NET_SALES, FinantialData.UNIT_CONSOLIDATE)
    if data:
        print('売上高前期比: %s' % (data, ))
        text += '売上高前期比: %s\r' % (data, )
    data = fd.get_forecast_duration_data(OPERATING_INCOME, FinantialData.UNIT_CONSOLIDATE)
    if data:
        print('営業利益前期比: %s' % (data, ))
        text += '営業利益前期比: %s\r' % (data, )
    data = fd.get_forecast_duration_data(ORDINARY_INCOME, FinantialData.UNIT_CONSOLIDATE)
    if data:
        print('経常利益前期比: %s' % (data, ))
        text += '経常利益前期比: %s\r' % (data, )
    
    print('---個別次期予想---')
    text += '\r---個別次期予想---\r'
    data = fd.get_forecast_duration_data(NET_SALES, FinantialData.UNIT_NON_CONSOLIDATE)
    if data:
        print('売上高前期比: %s' % (data, ))
        text += '売上高前期比: %s\r' % (data, )
    data = fd.get_forecast_duration_data(OPERATING_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
    if data:
        print('営業利益前期比: %s' % (data, ))
        text += '営業利益前期比: %s\r' % (data, )
    data = fd.get_forecast_duration_data(ORDINARY_INCOME, FinantialData.UNIT_NON_CONSOLIDATE)
    if data:
        print('経常利益前期比: %s' % (data, ))
        text += '経常利益前期比: %s\r' % (data, )

    print('\r\r')
    return text

def tdnet_test():
    #from_date = datetime.datetime(2019, 4, 24)
    #to_date = datetime.datetime(2019, 4, 24)
    from_date = datetime.datetime.today()
    to_date = from_date

    docs = tdnet.search_tanshin(to_date, from_date)
    for doc in docs:
        time.sleep(3)

        xbrl = tdnet.get_xbrl(doc)
        if not xbrl:
            print('no xbrl')
            continue
        
        print_data(xbrl)

def uho_test():
    docs = uho_catcher.search_tanshin('1803')
    for doc in docs:
        time.sleep(3)

        xbrl = uho_catcher.get_xbrl_from_doc(doc)
        if not xbrl:
            print('no xbrl')
            continue
        
        print_data(xbrl)

def diff_test():
    date = datetime.datetime(2019, 4, 15)
    td_docs = tdnet.search_tanshin(date, date)

    history = History(date)
    slack = Slack()

    for td_doc in td_docs:
        hash = td_doc.get_hash()
        if history.has_entry(hash):
            continue
        
        history.add_entry(hash)
        history.save()
        time.sleep(3)

        xbrl = tdnet.get_xbrl(td_doc)
        if not xbrl:
            print('%s: no xbrl' % (td_doc.doc_name, ))
            continue
        
        data = xbrl.get_data(CODE)
        if not data:
            print('could not find company code')
            continue
        
        code = data.text

        last_year = date.year - 1
        uho_doc = uho_catcher.get_tanshin(code, last_year)
        previous_xbrl = uho_catcher.get_xbrl_from_doc(uho_doc)
        if not previous_xbrl:
            print('could not find previous xbrl')
            continue
        
        text = print_diff(xbrl, previous_xbrl)
        text += '\r今期短信: %s\r' % (td_doc.get_pdf_url())
        text += '前期短信: %s\r' % (uho_doc.pdf_url)
        slack.post(text)

if __name__ == '__main__':
    diff_test()
    