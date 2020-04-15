from abc import ABC, abstractmethod
import csv
import collections
import os
import re
import urllib.request
from urllib.request import HTTPError

CACHE_DIR = '.cache'

class Analyzer(ABC):
    def __init__(self, file_name: str, column_name: str, data,  name: str = __name__, multiple=False):
        self.name = name
        self.file_name = file_name
        self.column_name = column_name.strip()
        self.total = 0
        self.found = {} if multiple else 0 
        self.missing = 0
        self.data = data
        self.multiple = multiple
        self.progress = 0
    
    def __enter__(self):
        if not self.data:
            with open(self.file_name, newline='', encoding='utf-8', errors='replace') as f:
                self.data = [{key.strip(): value for key, value in row.items()} for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]
        self.total = len(self.data)
        self.count()
        
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    @abstractmethod
    def decide(self, data: str, **kwargs):
        pass

    def count(self):
        # import time
        for row in self.data:

            # start_time = time.time()

            self.progress += 1
            if not self.column_name in row or any(row[self.column_name] == x for x in [None, '']):
                self.missing += 1
                continue
            
            decide = self.decide(row[self.column_name])

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
            else:
                pass

    def __str__(self):
        from collections import Counter
        import json
        # return f'"{{found": {self.found}; "total": {self.total}; "missing": {self.missing}}}'
        if type(self.found) == dict:
            j = json.dumps(dict(Counter(self.found).most_common(15)))
            return f'{{"found": [{j}]}}'
        else:
            return f'{{"found": {self.found}}}' 

