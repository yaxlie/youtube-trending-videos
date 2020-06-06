from abc import ABC, abstractmethod
import csv
import collections
import os
import re
import urllib.request
from urllib.request import HTTPError

CACHE_DIR = '.cache'
# MOST_COMMON_COUNT = 15 #TODO
MOST_COMMON_COUNT = None

class Analyzer(ABC):
    def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv,  name: str = __name__, multiple=False, omit_missing=True):
        self.name = name
        self.file_name = file_name
        self.column_name = column_name.strip()
        self.total = 0
        self.found = {} if multiple else 0 
        self.missing = 0 if omit_missing else None
        self.data = data
        self.multiple = multiple
        self.progress = 0
        self.selected_rows = selected_rows
        self.save_to_csv = save_to_csv
        self.generated_data = [] 
    
    def __enter__(self):
        if not self.data:
            with open(self.file_name, newline='', encoding='utf-8', errors='replace') as f:
                self.data = [{key.strip(): value for key, value in row.items()} for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]
        self.total = len(self.data)
        self.count()
        
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if self.save_to_csv:
            self._save_to_csv()

    @abstractmethod
    def decide(self, data: str, **kwargs):
        pass
    
    def _save_to_csv(self):
        # TODO: output directory as argument
        name = self.file_name.split('.')[0]
        directory = f'out/{name}'
        filename = f'{self.name}_{self.column_name}'.replace('/', '-')
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(f'{directory}/{filename}.csv', 'w+') as csv_file:
            csv_file.write(f'{self.name}_{self.column_name};\n')
            csv_file.writelines([f'"{str(row)}";\n' for row in self.generated_data])

    def count(self):
        # import time
        for row in self.data:
            # start_time = time.time()
            self.progress += 1

            if self.selected_rows and self.progress not in self.selected_rows:
                continue

            if self.missing is not None and (not self.column_name in row or any(row[self.column_name] == x for x in [None, ''])):
                if self.save_to_csv:
                    self.generated_data.append('-1')
                self.missing += 1
                continue
            
            decide = self.decide(row[self.column_name])

            if self.save_to_csv:
                self.generated_data.append(decide)

            # print("--- %s seconds ---" % (time.time() - start_time))

            if type(decide) == str:
                if not decide in self.found:
                    self.found[decide] = 0
                self.found[decide] += 1
            elif type(decide) == bool:
                if decide:
                    self.found += 1
            elif type(decide) == collections.Counter:
                for key in decide.keys():
                    if not key in self.found:
                        self.found[key] = 0
                    self.found[key] += decide[key]
            elif type(decide) == list:
                for key in decide:
                    if not key in self.found:
                        self.found[key] = 0
                    self.found[key] += 1
            else:
                pass

    def __str__(self):
        from collections import Counter
        import json
        # return f'"{{found": {self.found}; "total": {self.total}; "missing": {self.missing}}}'
        if type(self.found) == dict:
            if MOST_COMMON_COUNT:
                j = json.dumps(dict(Counter(self.found).most_common(MOST_COMMON_COUNT)))
            else:
                j = json.dumps(dict(Counter(self.found)))
            return f'{{"found": [{j}]}}'
        else:
            return f'{{"found": {self.found}}}' 

