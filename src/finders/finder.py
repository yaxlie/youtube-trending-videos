from abc import ABC, abstractmethod
import csv
import collections
import os
import re
import urllib.request
from urllib.request import HTTPError

CACHE_DIR = '.cache'

class AttributeFinder(ABC):
    def __init__(self, file_name: str, column_name: str, data,  name: str = __name__, multiple=False):
        self.name = name
        self.file_name = file_name
        self.column_name = column_name.strip()
        self.total = 0
        self.found = {} if multiple else 0 
        self.missing = 0
        self.data = data
        self.multiple = multiple
    
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
    def is_condition_met(self, data: str, **kwargs):
        pass

    def download_image(self, url: str):
        if not os.path.exists(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        img_name = re.sub(r"[^A-Za-z.]+", '', url)
        img_path = os.path.join(CACHE_DIR, img_name)

        if not os.path.exists(os.path.join(CACHE_DIR, img_path)):
            with open(img_path,'wb') as f:
                try:
                    content = urllib.request.urlopen(url).read()
                    f.write(content)
                    return content
                except HTTPError:
                    return None
        else:
            with open(img_path) as f:
                return f.read()


    def count(self):
        for row in self.data:
            if not self.column_name in row or any(row[self.column_name] == x for x in [None, '']):
                self.missing += 1
                continue
            
            is_condition_met = self.is_condition_met(row[self.column_name])
            if type(is_condition_met) == str:
                if not is_condition_met in self.found:
                    self.found[is_condition_met] = 0
                self.found[is_condition_met] += 1
            elif type(is_condition_met) == bool:
                if is_condition_met:
                    self.found += 1
            elif type(is_condition_met) == collections.Counter:
                for key in is_condition_met.keys():
                    if not key in self.found:
                        self.found[key] = 0
                    self.found[key] += is_condition_met[key]
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

