import json
import urllib.request

class Slack:

    CONFIG_FILE = 'slack_config.txt'

    def __init__(self):
        with open(self.CONFIG_FILE) as f:
            self.url = f.read()
    
    def post(self, message):
        method = 'POST'
        headers = {'Content-Type': 'application/json'}
        data_obj = {'text': message}
        data_bytes = json.dumps(data_obj).encode('utf-8')

        request = urllib.request.Request(self.url, data=data_bytes, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            print(response)
    

