import inspect
import src.analyzers, src.analyzers.text_analyzers, src.analyzers.image_analyzers
from src import analyze
from src.analyzers.text_analyzers import *
from src.analyzers.image_analyzers import *

if __name__ == "__main__":
	csv_files = ['data/GB_videos_5p.csv', 'data/US_videos_5p.csv']

	txt_columns=['title', 'channel_title', 'tags', 'description', 'publish_time', 'category_id', 'comments_disabled', 'ratings_disabled', 'video_error_or_removed']

	# Use reflection, to get available analyzers
	txt_analyzers = [m[0] for m in inspect.getmembers(src.analyzers.text_analyzers, inspect.isclass) if m[1].__module__ == 'src.analyzers.text_analyzers']

	img_columns=['thumbnail_link']
	img_analyzers = [m[0] for m in inspect.getmembers(src.analyzers.image_analyzers, inspect.isclass) if m[1].__module__ == 'src.analyzers.image_analyzers']

	analyze.execute(csv_files, txt_columns, txt_analyzers, 'text')
	analyze.execute(csv_files, img_columns, img_analyzers, 'images')