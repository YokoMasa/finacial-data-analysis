import re

YEAR_RE = re.compile('[12１２][0-9０-９]{3}年')
JP_YEAR_RE = re.compile('((昭和)|(平成)|(令和))([0-9０-９]+|元)年')
MONTH_RE = re.compile('[0-9０-９]{1,2}月')
DATE_RE = re.compile('[0-9０-９]{1,2}日')
NUM_RE = re.compile('[0-9０-９]+')

JP_YEAR_MAP = {
    '昭和': 1926,
    '平成': 1989,
    '令和': 2019
}

class Date:

    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
    
    def __str__(self):
        return 'year: %d, month: %d, day: %d' % (self.year, self.month, self.day)

def extract_jp_date(text):
    date = Date()
    year_match = YEAR_RE.search(text)
    jp_year_match = JP_YEAR_RE.search(text)
    if year_match:
        date.year = int(year_match[0][0:4])
        text = text[year_match.end():]
    elif jp_year_match:
        date.year = _parse_jp_year(jp_year_match[0])
        text = text[jp_year_match.end():]
    else:
        return None

    match = MONTH_RE.match(text)
    if match:
        num_match = NUM_RE.match(match[0])
        date.month = int(num_match[0])
        text = text[match.end():]
    else:
        return date
    
    match = DATE_RE.match(text)
    if match:
        num_match = NUM_RE.match(match[0])
        date.day = int(num_match[0])
    return date


# JP_YEAR_REGEXにマッチした文字列が前提
def _parse_jp_year(text):
    reki = text[0:2]
    if not reki in JP_YEAR_MAP:
        raise Exception('unknown era name')

    if text[2] == '元':
        return JP_YEAR_MAP[reki]
    
    match = NUM_RE.search(text)

    if not match:
        raise Exception('year not specified')
    
    return JP_YEAR_MAP[reki] + int(match[0]) - 1
    
def main():
    text = '【98870】株式会社松屋フーズホールディングス 平成31年3月期 第3四半期決算短信〔日本基準〕（連結）'
    print(extract_jp_date(text))
    text = '【69460】日本アビオニクス株式会社 ２０１９年３月期 決算短信〔日本基準〕（連結）'
    print(extract_jp_date(text))
    text = '【71840】株式会社　富山第一銀行 平成29年3月期　第2四半期（中間期）決算短信〔日本基準〕（連結）'
    print(extract_jp_date(text))
    text = '昭和３９年５月１日'
    print(extract_jp_date(text))
    text = '令和元年2月'
    print(extract_jp_date(text))

if __name__ == '__main__':
    main()
