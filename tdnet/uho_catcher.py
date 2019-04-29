import re
import urllib

import feedparser

import xbrl
import jp_date

BASE_URL = 'https://resource.ufocatch.com/atom/tdnetx/query/'

PDF_URL_RE = re.compile('pdfpage')
XBRL_URL_RE = re.compile('XBRLData/Summary/.*-ixbrl\.htm')
TANSHIN_RE = re.compile('(?!(.*半期|.*訂正)).*決算短信.*')

class UHODocument:

    def __init__(self):
        self.title = ''
        self.pdf_url = ''
        self.xbrl_url = ''

def search_tanshin(company_code, year=None):
    result = []
    docs = search(company_code)
    for doc in docs:
        if TANSHIN_RE.match(doc.title):
            if year:
                date = jp_date.extract_jp_date(doc.title)
                if date.year == year: 
                    result.append(doc)
            else:
                result.append(doc)
    return result

def get_tanshin(company_code, year):
    result = search_tanshin(company_code, year)
    if result:
        return result[0]

def search(company_code):
    url = BASE_URL + company_code
    d = feedparser.parse(url)
    result = []

    for entry in d.entries:
        doc = UHODocument()
        doc.title = entry.title

        href_key = 'href'
        for link in entry.links:
            if href_key in link:
                url = link[href_key]
                if PDF_URL_RE.search(url):
                    doc.pdf_url = url
                elif XBRL_URL_RE.search(url):
                    doc.xbrl_url = url
        result.append(doc)
    return result

def get_xbrl_from_doc(doc):
    with urllib.request.urlopen(doc.xbrl_url) as request:
        return xbrl.Xbrl(xbrl_string=request.read())

def get_xbrl(company_code, year):
    doc = get_tanshin(company_code, year) 
    if doc:
        return get_xbrl_from_doc(doc)
    else:
        return None

def test_docs():
    docs = search_tanshin('2229')
    for doc in docs:
        print(doc.title)

def text_xbrl():
    xbrl = get_xbrl('2229', 2016)
    if xbrl:
        code_key = 'SecuritiesCode'
        data = xbrl.get_data(code_key)
        print('コード: %s' % (data.text, ))

        date_key = 'FilingDate'
        data = xbrl.get_data(date_key)
        print('日付: %s' % (data.text, ))

        key = 'ChangeInOperatingIncome'
        print('今期実績' + '*' * 40)
        for data in xbrl.get_result_data_list(key):
            print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))
        print('\r')
        print('次期予想' + '*' * 40)
        for data in xbrl.get_forecast_data_list(key):
            print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))

if __name__ == '__main__':
    test_docs()
    