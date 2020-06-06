import re
import datetime  
import calendar
import nltk
from src.analyzers.analyzer import Analyzer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter

# class MissingValuesAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, 'Missing', omit_missing=False)

#     def decide(self, data: str):
#         return data == '' or data == None

# class CaseAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv, multiple=True):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, 'Case', multiple)

#     def decide(self, data: str):
#         if data.isupper():
#             return '0' # 'Upper'
#         elif data.islower():
#             return '1' # 'Lower'
#         elif all([word.strip()[0].isupper() for word in data.split()]):
#             return '2' # 'Title-like'
#         else:
#             return '3' # 'Mixed'


# class DigitsAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, 'Contain digits')

#     def decide(self, data: str):
#         result = re.match(r'\d', data)
#         return '1' if result else '0'


# class SpecialCharsAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, 'With special characters')

#     def decide(self, data: str):
#         result = re.match(r'[^a-zA-Z.? !0-9]', data)
#         return '1' if result else '0'


# class BooleanAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, 'Boolean')

#     def decide(self, data: str):
#         if data.lower() in ['true', 't']:
#             return '1'
#         elif data.lower() in ['false', 'f']:
#             return '0'
#         else: 
#             raise ValueError


# class HyperlinkAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, 'Hyperlink')

#     def decide(self, data: str):
#         result = re.match(r'https?:\/\/', data)
#         return '1' if result else '0'


# class DayAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Upload day', multiple=True)

#     def decide(self, data: str):
#         dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
#         date = datetime.datetime.strptime(data, dt_format).weekday()
#         # day = (calendar.day_name[date])
#         # return day
#         return str(date)


# class HourAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Upload hour', multiple=True)

#     def decide(self, data: str):
#         dt_format = '%Y-%m-%dT%H:%M:%S.%fZ'
#         date = datetime.datetime.strptime(data, dt_format)
#         return str(date.hour)


class CommonWordsAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
        super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Common words', multiple=True)

    def decide(self, data: str):
        stemmer = PorterStemmer()

        words = [stemmer.stem(word) for word in data.split()]
        words_count = Counter(words)

        return words_count

# class MostCommonWordAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Most common word', multiple=True)

#     def decide(self, data: str):
#         stemmer = PorterStemmer()

#         sentence = re.sub('[^a-zA-Z0-9 \n\.]', ' ', data)
#         words = [stemmer.stem(word) for word in sentence.split()]
#         words_count = Counter(words)

#         return "" if len (words_count.most_common(1)) == 0 else words_count.most_common(1)[0][0]


# class PartsOfSpeechAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Parts of speech', multiple=True)
#         if not column_name in ['title', 'tags', 'description']: # To skip and save time
#             raise TypeError() # TODO: Custom exception

#     def decide(self, data: str):
#         tokens = nltk.word_tokenize(data)
#         pos_t = nltk.pos_tag(tokens)
#         words_count= Counter([pos[1] for pos in pos_t])

#         return words_count


# class LongTextWordsAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Words counter', multiple=True)

#     def decide(self, data: str):
#         words_count = len(data.split())
#         long_level = int(words_count/5)
#         return str(long_level)


# class LongTextLettersAnalyzer(Analyzer):
#     def __init__(self, file_name: str, column_name: str, data, selected_rows, save_to_csv):
#         super().__init__(file_name, column_name, data, selected_rows, save_to_csv, f'Letters counter', multiple=True)

#     def decide(self, data: str):
#         letters_count = len(data)
#         long_level = int(letters_count/10)
#         return str(long_level)
