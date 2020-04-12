import inspect
import finders, finders.text_finders, finders.image_finders
import json
from collections import Counter
from finders.text_finders import *
from finders.image_finders import *
from progress.bar import Bar
import nltk

nltk.download('punkt')
nltk.download('maxent_treebank_pos_tagger')
nltk.download('averaged_perceptron_tagger')

def execute(csv_files, columns, finders):
	data = None
	result = {}
	bar = Bar('Processing', max=len(csv_files) * len(finders) * len(columns))
	for csv_file in csv_files:
		result[csv_file] = {}
		for findername in finders:
			result[csv_file][findername] = {}
			Finder = globals()[findername]
			for column in columns:
				bar.next()
				try:
					with Finder(csv_file, column, data) as finder:
						result[csv_file][findername][column] = dict(Counter(finder.found).most_common(15))
				except Exception as e: #TODO: only specific exceptions
					pass
	bar.finish()

	with open('result.json','w') as f:
		_json = json.dumps(result, sort_keys=True, indent=4)
		f.write(_json)
		print(_json)

if __name__ == "__main__":
	csv_files = ['youtube_data/GB_videos_5p.csv', 'US_videos_5p.csv']

	txt_columns=['title', 'channel_title', 'tags', 'description', 'publish_time', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed']
	txt_finders = [m[0] for m in inspect.getmembers(finders.text_finders, inspect.isclass) if m[1].__module__ == 'finders.text_finders']

	img_columns=['thumbnail_link']
	img_finders = [m[0] for m in inspect.getmembers(finders.image_finders, inspect.isclass) if m[1].__module__ == 'finders.image_finders']

	# execute(csv_files, txt_columns, txt_finders)
	execute(csv_files, img_columns, img_finders)