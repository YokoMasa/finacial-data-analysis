import os
import json
import datetime

class History:

    _unique_instance = None
    HISTORY_FILE = 'history.json'

    DATE_FORMAT = '%Y-%m-%d'
    KEY_DATE = 'date'
    KEY_ENTRIES = 'entries'

    def __init__(self, date):
        self.date_string = date.strftime(self.DATE_FORMAT)
        self.entries = []
        self._load()
    
    def _load(self):
        if os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE) as f:
                data = json.loads(f.read())
                if self.KEY_DATE in data and self.KEY_ENTRIES in data:
                    date = data[self.KEY_DATE]
                    if date == self.date_string:
                        self.entries = data[self.KEY_ENTRIES]
    
    def save(self):
        json_obj = {self.KEY_DATE: self.date_string, self.KEY_ENTRIES: self.entries}
        with open(self.HISTORY_FILE, 'w') as f:
            f.write(json.dumps(json_obj))
    
    def add_entry(self, entry):
        if not entry in self.entries:
            self.entries.append(entry)
    
    def has_entry(self, entry):
        return entry in self.entries

if __name__ == '__main__':
    date = datetime.datetime(2019, 4, 19)
    history = History(date)
    entry = 'aaaaa'
    print(history.has_entry(entry))
    history.add_entry(entry)
    history.save()
    print(history.has_entry(entry))



