import inspect
import finders, finders.finders
import json
from collections import Counter
from finders.finders import *
from progress.bar import Bar
import nltk

nltk.download('punkt')
nltk.download('maxent_treebank_pos_tagger')
nltk.download('averaged_perceptron_tagger')

if __name__ == "__main__":
	data = None
	result = {}
	txt_columns=['title', 'channel_title', 'tags', 'description', 'publish_time', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed']
	csv_files = ['youtube_data/GB_videos_5p.csv', 'US_videos_5p.csv']

	all_finders = [m[0] for m in inspect.getmembers(finders.finders, inspect.isclass) if m[1].__module__ == 'finders.finders']
	bar = Bar('Processing', max=len(csv_files) * len(all_finders) * len(txt_columns))

	for csv_file in csv_files:
		result[csv_file] = {}
		for findername in all_finders:
			result[csv_file][findername] = {}
			Finder = globals()[findername]
			for column in txt_columns:
				bar.next()
				try:
					with Finder(csv_file, column, data) as finder:
						result[csv_file][findername][column] = dict(Counter(finder.found).most_common(15))
				except Exception as e:
					pass
	bar.finish()

	with open('result.json','w') as f:
		json = json.dumps(result, sort_keys=True, indent=4)
		f.write(json)
		print(json)