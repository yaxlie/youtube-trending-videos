import inspect
import analyzers, analyzers.text_analyzers, analyzers.image_analyzers
import json
import nltk
from collections import Counter
from analyzers.text_analyzers import *
from analyzers.image_analyzers import *
from progress.bar import Bar

nltk.download('punkt')
nltk.download('maxent_treebank_pos_tagger')
nltk.download('averaged_perceptron_tagger')

def execute(csv_files, columns, analyzers, output='result'):
	data = None
	result = {}
	bar = Bar('Processing', max=len(csv_files) * len(analyzers) * len(columns))
	for csv_file in csv_files:
		result[csv_file] = {}
		for analyzername in analyzers:
			result[csv_file][analyzername] = {}
			Analyzer = globals()[analyzername]
			for column in columns:
				bar.next()
				try:
					with Analyzer(csv_file, column, data) as analyzer:
						result[csv_file][analyzername][column] = dict(Counter(analyzer.found).most_common(15))
				except (ValueError, TypeError):
					# It just means, that the specific column is not for this specific analyzer - ignore.
					pass
	bar.finish()

	with open(f'{output}.json','w') as f:
		_json = json.dumps(result, sort_keys=True, indent=4)
		f.write(_json)
		print(_json)

if __name__ == "__main__":
	csv_files = ['data/GB_videos_5p.csv', 'data/US_videos_5p.csv']

	txt_columns=['title', 'channel_title', 'tags', 'description', 'publish_time', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed']
	
	# Use reflection, to get available analyzers
	txt_analyzers = [m[0] for m in inspect.getmembers(analyzers.text_analyzers, inspect.isclass) if m[1].__module__ == 'analyzers.text_analyzers']

	img_columns=['thumbnail_link']
	img_analyzers = [m[0] for m in inspect.getmembers(analyzers.image_analyzers, inspect.isclass) if m[1].__module__ == 'analyzers.image_analyzers']

	execute(csv_files, txt_columns, txt_analyzers, 'text')
	execute(csv_files, img_columns, img_analyzers, 'images')