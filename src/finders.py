from abc import ABC, abstractmethod
import csv

class AttributeFinder(ABC):
    def __init__(self, file_name: str, column_name: str, reader,  name: str = __name__):
        self.name = name
        self.file_name = file_name
        self.column_name = column_name
        self.total = 0
        self.found = 0
        self.data = None
    
    def __enter__(self):
        if not self.data:
            with open(self.file_name, newline='', encoding='utf-8', errors='ignore') as f:
                self.data = [{key: value for key, value in row.items()} for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]
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
            if self.is_condition_met(row[self.column_name]):
                self.found += 1

    def __str__(self):
        return self.name

class UpperCaseFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, reader):
        super().__init__(file_name, column_name, reader, 'Upper Case')

    def is_condition_met(self, data: str) -> bool:
        return data.isupper()