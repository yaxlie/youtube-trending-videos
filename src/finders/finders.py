import re

from finders.finder import AttributeFinder

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