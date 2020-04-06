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

class TrueFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Is True')

    def is_condition_met(self, data: str) -> bool:
        return data.upper == 'TRUE'


class HyperlinkFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Is True')

    def is_condition_met(self, data: str) -> bool:
        return re.match(r'https?:\/\/', data)


class DayFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Upload day', multiple=True)

    def is_condition_met(self, data: str) -> bool:
        import datetime  
        import calendar
        dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        date = datetime.datetime.strptime(data, dt_format).weekday()
        day = (calendar.day_name[date])
        return day

class HourFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Upload hour', multiple=True)

    def is_condition_met(self, data: str) -> bool:
        import datetime  
        import calendar
        dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        date = datetime.datetime.strptime(data, dt_format)
        return str(date.hour)

class CommonWordsFinder(AttributeFinder):
    from collections import Counter
    
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Common words', multiple=True)

    def is_condition_met(self, data: str) -> bool:
        from nltk.tokenize import word_tokenize
        from nltk.stem import PorterStemmer
        from collections import Counter

        stemmer = PorterStemmer()

        words = [stemmer.stem(word) for word in data.split()]
        words_count= Counter(words)

        return words_count

    def __str__(self):
        return f'"{{found": {dict(Counter(finder.found).most_common(15))}'

class LongTextWordsFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Words counter', multiple=True)

    def is_condition_met(self, data: str) -> bool:
        words_count = len(data.split())
        long_level = int(words_count/5)
        return str(long_level)

class LongTextLettersFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Letters counter', multiple=True)

    def is_condition_met(self, data: str) -> bool:
        letters_count = len(data)
        long_level = int(letters_count/10)
        return str(long_level)
