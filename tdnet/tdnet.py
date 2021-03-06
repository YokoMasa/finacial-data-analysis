import os
import re
import hashlib
import urllib.request
import urllib.parse
import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLPullParser
import xml.dom.minidom as minidom

from bs4 import BeautifulSoup

import xbrl_extractor

BASE_URL = 'https://www.release.tdnet.info'
SEARCH_URL = BASE_URL + '/onsf/TDJFSearch/TDJFSearch'
HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.release.tdnet.info',
    'Referer': 'https://www.release.tdnet.info/onsf/TDJFSearch/I_head',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
START_DATE_KEY = 't0'
END_DATE_KEY = 't1'
Q_KEY = 'q'

Q_DATE_FORMAT = '%Y%m%d'
TD_STRP_DATE_FORMAT = '%Y/%m/%d %H:%M'

TANSHIN_RE = re.compile('(?!(.*半期|.*訂正)).*決算短信.*')

TD_SELECTOR_TIME = 'td.time'
TD_SELECTOR_CODE = 'td.code'
TD_SELECTOR_COMPANY_NAME = 'td.companyname'
TD_SELECTOR_TITLE = 'td.title'
TD_SELECTOR_XBRL = 'td.xbrl'
TD_SELECTOR_EXCHANGE = 'td.exchange'
TD_SELECTOR_UPDATE = 'td.update'

MAIN_TABLE_SELECTOR = '#maintable'


class TDDocument:

    def __init__(self):
        self.time = None
        self.code = ''
        self.company_name = ''
        self.doc_name = ''
        self.xbrl_path = ''
        self.pdf_path = ''
    
    def get_pdf_url(self):
        return BASE_URL + self.pdf_path
    
    def get_hash(self):
        base = '%s%s%s' % (self.code, self.company_name, self.doc_name)
        base_bytes = base.encode('utf-8')
        m = hashlib.sha1()
        m.update(base_bytes)
        return m.hexdigest()
    
    def is_pdf_available(self):
        return self.pdf_path != ''

    def is_xbrl_available(self):
        return self.xbrl_path != ''

    def get_pdf_file_name(self):
        return self._extract_file_name_from_path(self.pdf_path)
    
    def get_xbrl_file_name(self):
        return self._extract_file_name_from_path(self.xbrl_path)

    def _extract_file_name_from_path(self, path):
        stripped = path.rsplit('/', maxsplit=1)
        if len(stripped) == 2:
            return stripped[1]
        else:
            return stripped[0]
    
    def __str__(self):
        return 'company: %s, doc_name: %s, xbrl: %s, pdf: %s' % (self.company_name, self.doc_name, self.xbrl_path, self.pdf_path)

def download_xbrl(doc):
    if not doc.is_xbrl_available():
        #print('xbrl unavailable')
        return
        
    try:
        full_url = BASE_URL + doc.xbrl_path
        response = urllib.request.urlopen(full_url)
        with open(doc.get_xbrl_file_name(), mode='w+b') as file:
            file.write(response.read())
        return doc.get_xbrl_file_name()
    except Exception as e:
        print('Error occurred while downloading pdf')
        print(e)

def get_xbrl(doc):
    zip_file_name = download_xbrl(doc)
    if zip_file_name:
        xbrl = xbrl_extractor.extract(zip_file_name)
        os.remove(zip_file_name)
        return xbrl
    else:
        return None

def search_tanshin(start_date, end_date):
    result = []
    docs = search(start_date, end_date, '決算短信')
    for doc in docs:
        if TANSHIN_RE.match(doc.doc_name):
            result.append(doc)
    return result

def search(start_date, end_date, q):
    if not start_date or not end_date:
        raise RuntimeError('date should not be None')
    
    start_date_string = start_date.strftime(Q_DATE_FORMAT)
    end_date_string = end_date.strftime(Q_DATE_FORMAT)
    data_dict = {
        START_DATE_KEY: start_date_string,
        END_DATE_KEY: end_date_string,
        Q_KEY: q,
        'm': 0 #謎
    }
    data = urllib.parse.urlencode(data_dict)
    data = data.encode('ascii')

    request = urllib.request.Request(SEARCH_URL, data, HEADERS)
    response = urllib.request.urlopen(request)
    #body = str(response.read())
    body = response.read().decode('utf-8')
    return _parse(body)

def _parse(body):
    soup = BeautifulSoup(body, features='html.parser')
    soup_result = soup.select(MAIN_TABLE_SELECTOR)
    result_array = []
    if len(soup_result) != 0:
        table_element = soup_result[0]
        for row_element in table_element.find_all('tr'):
            doc = TDDocument()
            el = row_element.select_one(TD_SELECTOR_TIME)
            if el:
                doc.time = datetime.datetime.strptime(el.get_text(), TD_STRP_DATE_FORMAT)
            
            el = row_element.select_one(TD_SELECTOR_CODE)
            if el:
                doc.code = el.get_text()

            el = row_element.select_one(TD_SELECTOR_COMPANY_NAME)
            if el:
                doc.company_name = el.get_text()

            el = row_element.select_one(TD_SELECTOR_EXCHANGE)
            if el:
                doc.exchange = el.get_text()

            el = row_element.select_one(TD_SELECTOR_UPDATE)
            if el:
                doc.update = el.get_text()

            el = row_element.select_one(TD_SELECTOR_XBRL)
            if el:
                a = el.find('a')
                if a:
                    doc.xbrl_path = a["href"]
            
            el = row_element.select_one(TD_SELECTOR_TITLE)
            if el:
                a = el.find('a')
                if a:
                    doc.doc_name = a.get_text()
                    doc.pdf_path = a["href"]
            result_array.append(doc)
    return result_array

if __name__ == '__main__':
    date = datetime.datetime(2019, 4, 18)
    result = search_tanshin(date, date)
    for doc in result:
        print(doc)
    
