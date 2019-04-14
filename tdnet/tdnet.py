import urllib.request
import urllib.parse
import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XMLPullParser
import xml.dom.minidom as minidom

from bs4 import BeautifulSoup

URL = 'https://www.release.tdnet.info/onsf/TDJFSearch/TDJFSearch'
HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.release.tdnet.info',
    'Referer': 'https://www.release.tdnet.info/onsf/TDJFSearch/I_head',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
START_DATE_KEY = 't0'
END_DATE_KEY = 't1'
Q_KEY = 'q'
DATE_FORMAT = '%Y%m%d'

TD_SELECTOR_TIME = 'td.time'
TD_SELECTOR_CODE = 'td.code'
TD_SELECTOR_COMPANY_NAME = 'td.companyname'
TD_SELECTOR_TITLE = 'td.title'
TD_SELECTOR_XBRL = 'td.xbrl'
TD_SELECTOR_EXCHANGE = 'td.exchange'
TD_SELECTOR_UPDATE = 'td.update'

MAIN_TABLE_SELECTOR = '#maintable'

def search(start_date, end_date, q):
    if not start_date or not end_date:
        raise RuntimeError('date should not be None')
    
    start_date_string = start_date.strftime(DATE_FORMAT)
    end_date_string = end_date.strftime(DATE_FORMAT)
    data_dict = {
        START_DATE_KEY: start_date_string,
        END_DATE_KEY: end_date_string,
        Q_KEY: q,
        'm': 0 #謎
    }
    data = urllib.parse.urlencode(data_dict)
    data = data.encode('ascii')

    request = urllib.request.Request(URL, data, HEADERS)
    response = urllib.request.urlopen(request)
    body = str(response.read())
    _parse(body)

def _parse(body):
    soup = BeautifulSoup(body, features='html.parser')
    soup_result = soup.select(MAIN_TABLE_SELECTOR)
    if len(soup_result) != 0:
        table_element = soup_result[0]
        for row_element in table_element.find_all('tr'):
            print(row_element.select(TD_SELECTOR_TIME)[0].get_text())
            print(row_element.select(TD_SELECTOR_CODE)[0].get_text())
            print(row_element.select(TD_SELECTOR_COMPANY_NAME)[0].get_text())
            print(row_element.select(TD_SELECTOR_EXCHANGE)[0].get_text())
            print(row_element.select(TD_SELECTOR_UPDATE)[0].get_text())


if __name__ == '__main__':
    date = datetime.datetime(2019, 4, 3)
    search(date, date, '短信')
