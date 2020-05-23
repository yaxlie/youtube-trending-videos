import inspect
import random
import src.analyzers, src.analyzers.text_analyzers, src.analyzers.image_analyzers
from src import analyze
from src.analyzers.text_analyzers import *
from src.analyzers.image_analyzers import *
from src.analyzers.dummy_analyzers import *

if __name__ == "__main__":
	csv_files = ['data/GB_videos_5p.csv', 'data/US_videos_5p.csv']

	txt_columns=['title', 'channel_title', 'tags', 'description', 'publish_time', 'category_id', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed']

	# Use reflection, to get available analyzers
	txt_analyzers = [m[0] for m in inspect.getmembers(src.analyzers.text_analyzers, inspect.isclass) if m[1].__module__ == 'src.analyzers.text_analyzers']

	img_columns=['thumbnail_link']
	img_analyzers = [m[0] for m in inspect.getmembers(src.analyzers.image_analyzers, inspect.isclass) if m[1].__module__ == 'src.analyzers.image_analyzers']

	dummy_columns=['views', 'likes', 'dislikes', 'comment_count']
	dummy_analyzers = [m[0] for m in inspect.getmembers(src.analyzers.dummy_analyzers, inspect.isclass) if m[1].__module__ == 'src.analyzers.dummy_analyzers']

	# analyze.execute(csv_files, txt_columns, txt_analyzers, 'text')
	# analyze.execute(csv_files, img_columns, img_analyzers, 'images')

	# generate data for step3

	rows = random.sample(range(1, 35000), 1000)
	analyze.execute(csv_files, txt_columns, txt_analyzers, 'text', rows, True)
	analyze.execute(csv_files, img_columns, img_analyzers, 'images', rows, True)
	analyze.execute(csv_files, dummy_columns, dummy_analyzers, 'dummy', rows, True)