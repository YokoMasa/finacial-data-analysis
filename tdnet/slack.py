import json
import urllib.request

class Slack:

    CONFIG_FILE = 'slack_config.json'
    CHANNEL_MAIN = 'main'
    CHANNEL_GREAT = 'great'
    CHANNEL_ERROR = 'error'

    def __init__(self):
        with open(self.CONFIG_FILE) as f:
            config = json.load(f)
            self._main_url = config[self.CHANNEL_MAIN]
            self._great_url = config[self.CHANNEL_GREAT]
            self._error_url = config[self.CHANNEL_ERROR]
    
    def post_main(self, message):
        self.post(message, self._main_url)
    
    def post_great(self, message):
        self.post(message, self._great_url)
    
    def post_error(self, message):
        self.post(message, self._error_url)

    def post(self, message, url):
        method = 'POST'
        headers = {'Content-Type': 'application/json'}
        data_obj = {'text': message}
        data_bytes = json.dumps(data_obj).encode('utf-8')

        request = urllib.request.Request(url, data=data_bytes, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            print(response)

if __name__ == '__main__':
    slack = Slack()
    slack.post_main('test')
    slack.post_great('test')
    slack.post_error('test')


