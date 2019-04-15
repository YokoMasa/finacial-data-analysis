import re
import zipfile
import xbrl

XBRL_FILE_PATTERN = '[xX][bB][rR][lL][dD][aA][tT][aA]/Summary/.*\.htm$'

def extract(xbrl_zip_file_path):
    try:
        regex = re.compile(XBRL_FILE_PATTERN)
        xbrl_zip_file = zipfile.ZipFile(xbrl_zip_file_path)
        for member in xbrl_zip_file.namelist():
            if (regex.match(member)):
                with xbrl_zip_file.open(member) as file:
                    xbrl_string = file.read()
                    return xbrl.Xbrl(xbrl_string=xbrl_string)
    except Exception as e:
        return None

if __name__ == '__main__':
    xbrl = extract('sample_zip.zip')
    key = 'ChangeInOperatingIncome'

    print('今期実績' + '*' * 40)
    for data in xbrl.get_result_data_list(key):
        print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))
    print('\r')
    print('次期予想' + '*' * 40)
    for data in xbrl.get_forecast_data_list(key):
        print('営業利益増加率: %s, contextRef: %s' % (data.text, data.context_ref))