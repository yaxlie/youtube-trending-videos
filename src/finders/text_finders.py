import re
from finders.finder import AttributeFinder

class UpperCaseFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Upper case')

    def is_condition_met(self, data: str):
        return data.isupper()

class LowerCaseFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Lower case')

    def is_condition_met(self, data: str):
        return data.islower()

class DigitsFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'With digits')

    def is_condition_met(self, data: str):
        result = re.match(r'\d', data)
        return True if result else False

class ContainSpecialCharsFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'With special characters')

    def is_condition_met(self, data: str):
        result = re.match(r'[^a-zA-Z.? !0-9]', data)
        return True if result else False

class TrueFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Is True')

    def is_condition_met(self, data: str):
        return data == 'True'


class HyperlinkFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Is True')

    def is_condition_met(self, data: str):
        result = re.match(r'https?:\/\/', data)
        return True if result else False


class DayFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Upload day', multiple=True)

    def is_condition_met(self, data: str):
        import datetime  
        import calendar
        dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        date = datetime.datetime.strptime(data, dt_format).weekday()
        day = (calendar.day_name[date])
        return day

class HourFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Upload hour', multiple=True)

    def is_condition_met(self, data: str):
        import datetime  
        import calendar
        dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        date = datetime.datetime.strptime(data, dt_format)
        return str(date.hour)

class CommonWordsFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Common words', multiple=True)
        if not column_name in ['title', 'tags', 'description']: # To skip and save time
            raise Exception() # TODO: Custom exception

    def is_condition_met(self, data: str):
        from nltk.tokenize import word_tokenize
        from nltk.stem import PorterStemmer
        from collections import Counter

        stemmer = PorterStemmer()

        words = [stemmer.stem(word) for word in data.split()]
        words_count= Counter(words)

        return words_count

class PartsOfSpeechFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Common words', multiple=True)
        if not column_name in ['title', 'tags', 'description']: # To skip and save time
            raise Exception() # TODO: Custom exception

    def is_condition_met(self, data: str):
        import nltk
        from collections import Counter

        tokens = nltk.word_tokenize(data)
        pos_t = nltk.pos_tag(tokens)
        words_count= Counter([pos[1] for pos in pos_t])

        return words_count

class LongTextWordsFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Words counter', multiple=True)

    def is_condition_met(self, data: str):
        words_count = len(data.split())
        long_level = int(words_count/5)
        return str(long_level)

class LongTextLettersFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Letters counter', multiple=True)

    def is_condition_met(self, data: str):
        letters_count = len(data)
        long_level = int(letters_count/10)
        return str(long_level)
