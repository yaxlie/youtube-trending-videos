from finders import *

if __name__ == "__main__":
    reader = None
    with UpperCaseFinder('youtube_data/GB_videos_5p.csv', 'title', reader) as finder:
        print(f'"{finder.name}"";"{finder.column_name}"";{finder.found};{finder.total}')