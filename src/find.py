import inspect
import finders, finders.finders
from collections import Counter
from finders.finders import *

if __name__ == "__main__":
	data = None
	txt_columns=['title', 'channel_title', 'tags', 'description']
	csv_file = 'youtube_data/GB_videos_5p.csv'


	all_finders = [m[0] for m in inspect.getmembers(finders.finders, inspect.isclass) if m[1].__module__ == 'finders.finders']

	json = []
	for findername in all_finders:
		print('.') # TODO: progress bar
		Finder = globals()[findername]
		results = []
		try:
			for column in txt_columns:
				with Finder(csv_file, column, data) as finder:
					results.append(f'"{column}": {finder}')
					# TODO: Check if any improve
					# if not data:
					# 	data = finder.data
			columns_array = ','.join(results)
		except Exception as e:
			print(e)
		json.append(f'{{"{findername}": [{{{columns_array}}}]}}')

	result = ','.join(json)
	print(f'[{result}]')
