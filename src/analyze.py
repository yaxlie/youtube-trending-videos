import src.analyzers, src.analyzers.text_analyzers, src.analyzers.image_analyzers, src.analyzers.dummy_analyzers
import json
import nltk
from collections import Counter
from src.analyzers.text_analyzers import *
from src.analyzers.image_analyzers import *
from src.analyzers.dummy_analyzers import *
from progress.bar import Bar

nltk.download('punkt')
nltk.download('maxent_treebank_pos_tagger')
nltk.download('averaged_perceptron_tagger')

def execute(csv_files, columns, analyzers, output='result', selected_rows=None, save_to_csv=False):
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
					with Analyzer(csv_file, column, data, selected_rows, save_to_csv) as analyzer:
						if type(analyzer.found) == int:
							result[csv_file][analyzername][column] = analyzer.found
						else:
							result[csv_file][analyzername][column] = dict(Counter(analyzer.found).most_common(15))
				except (ValueError, TypeError):
					# It just means, that the specific column is not for this specific analyzer - ignore.
					pass
	bar.finish()

	with open(f'{output}.json','w') as f:
		_json = json.dumps(result, sort_keys=True, indent=4)
		f.write(_json)
		print(_json)
