import inspect
import finders, finders.finders
from collections import Counter
from finders.finders import *

if __name__ == "__main__":
	data = None
	txt_columns=['title', 'channel_title', 'tags', 'description']
	csv_file = 'youtube_data/GB_videos_5p.csv'
	reader = None


	all_finders = [m[0] for m in inspect.getmembers(finders.finders, inspect.isclass) if m[1].__module__ == 'finders.finders']
	for findername in all_finders:
		Finder = globals()[findername]
		try:
			for column in txt_columns:
				with Finder(csv_file, column, data) as finder:
					print(finder)

					# TODO: does it work?
					if not reader:
						reader = finder.data
		except Exception as e:
			print(e)

	# for column in txt_columns:
	# 	with UpperCaseFinder(csv_file, column, data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')
	# 		reader = finder.data

	# for column in txt_columns:
	# 	with LowerCaseFinder(csv_file, column, data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')
	
	# for column in txt_columns:
	# 	with DigitsFinder(csv_file, column, data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')
	
	# for column in txt_columns:
	# 	with ContainSpecialCharsFinder(csv_file, column, data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')
	
	# for column in txt_columns:
	# 	with HyperlinkFinder(csv_file, column, data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')
	
	# for column in txt_columns:
	# 	with CommonWordsFinder(csv_file, 'title', data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{dict(Counter(finder.found).most_common(15))};-;-')
	
	# for column in txt_columns:
	# 	with LongTextWordsFinder(csv_file, 'title', data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};-;-')

	# for column in txt_columns:
	# 	with LongTextLettersFinder(csv_file, 'title', data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};-;-')
	
	# with TrueFinder(csv_file, 'comments_disabled', data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')
	
	# with TrueFinder(csv_file, 'ratings_disabled', data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')

	# with TrueFinder(csv_file, 'comments_disabled', data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')

	# with TrueFinder(csv_file, 'video_error_or_removed', data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')

	# with DayFinder(csv_file, 'publish_time', data) as finder:
	# 		print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')

	# with HourFinder(csv_file, 'publish_time', data) as finder:
	# 	print(f'"{finder.name}";"{finder.column_name}";{finder.found};{finder.total};{finder.missing}')
