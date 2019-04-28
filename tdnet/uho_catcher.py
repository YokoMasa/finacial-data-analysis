import re

import feedparser

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

if __name__ == '__main__':
    def print_doc(doc):
        print(doc.title)
        print(doc.pdf_url)
        print(doc.xbrl_url)
        print('\r')

    doc = get_tanshin('6273', 2016)
    if doc:
        print_doc(doc)
    