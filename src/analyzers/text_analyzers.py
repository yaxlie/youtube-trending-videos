import re
import datetime  
import calendar
import nltk
from src.analyzers.analyzer import Analyzer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter

class MissingValuesAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Missing', omit_missing=False)

    def decide(self, data: str):
        return data == '' or data == None

class CaseAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data, multiple=True):
        super().__init__(file_name, column_name, data, 'Case', multiple)

    def decide(self, data: str):
        if data.isupper():
            return 'Upper'
        elif data.islower():
            return 'Lower'
        elif all([word.strip()[0].isupper() for word in data.split()]):
            return 'Title-like'
        else:
            return 'Mixed'


class DigitsAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Contain digits')

    def decide(self, data: str):
        result = re.match(r'\d', data)
        return True if result else False


class SpecialCharsAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'With special characters')

    def decide(self, data: str):
        result = re.match(r'[^a-zA-Z.? !0-9]', data)
        return True if result else False


class BooleanAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Boolean')

    def decide(self, data: str):
        if data.lower() in ['true', 't']:
            return True
        elif data.lower() in ['false', 'f']:
            return False
        else: 
            raise ValueError


class HyperlinkAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, 'Is True')

    def decide(self, data: str):
        result = re.match(r'https?:\/\/', data)
        return True if result else False


class DayAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Upload day', multiple=True)

    def decide(self, data: str):
        dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        date = datetime.datetime.strptime(data, dt_format).weekday()
        day = (calendar.day_name[date])
        return day


class HourAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Upload hour', multiple=True)

    def decide(self, data: str):
        dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        date = datetime.datetime.strptime(data, dt_format)
        return str(date.hour)


class CommonWordsAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Common words', multiple=True)

    def decide(self, data: str):
        stemmer = PorterStemmer()

        words = [stemmer.stem(word) for word in data.split()]
        words_count= Counter(words)

        return words_count


class PartsOfSpeechAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Common words', multiple=True)
        if not column_name in ['title', 'tags', 'description']: # To skip and save time
            raise TypeError() # TODO: Custom exception

    def decide(self, data: str):
        tokens = nltk.word_tokenize(data)
        pos_t = nltk.pos_tag(tokens)
        words_count= Counter([pos[1] for pos in pos_t])

        return words_count


class LongTextWordsAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Words counter', multiple=True)

    def decide(self, data: str):
        words_count = len(data.split())
        long_level = int(words_count/5)
        return str(long_level)


class LongTextLettersAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data):
        super().__init__(file_name, column_name, data, f'Letters counter', multiple=True)

    def decide(self, data: str):
        letters_count = len(data)
        long_level = int(letters_count/10)
        return str(long_level)
