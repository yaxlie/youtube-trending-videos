from abc import ABC, abstractmethod
import csv
import re

class AttributeFinder(ABC):
    def __init__(self, file_name: str, column_name: str, data,  name: str = __name__):
        self.name = name
        self.file_name = file_name
        self.column_name = column_name.strip()
        self.total = 0
        self.found = 0
        self.missing = 0
        self.data = data
    
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
    def is_condition_met(self, data: str) -> bool:
        pass

    def count(self):
        for row in self.data:
            if not self.column_name in row or any(row[self.column_name] == x for x in [None, '']):
                self.missing += 1
                continue

            if self.is_condition_met(row[self.column_name]):
                self.found += 1

    def __str__(self):
        return self.name

class UpperCaseFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Upper case')

    def is_condition_met(self, data: str) -> bool:
        return data.isupper()

class LowerCaseFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Lower case')

    def is_condition_met(self, data: str) -> bool:
        return data.islower()

class DigitsFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'With digits')

    def is_condition_met(self, data: str) -> bool:
        return re.match(r'\d', data)

class ContainSpecialCharsFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'With special characters')

    def is_condition_met(self, data: str) -> bool:
        return re.match(r'[^a-zA-Z.? !0-9]', data)
