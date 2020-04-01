from finders import *

if __name__ == "__main__":
    data = None
    txt_columns=['title', 'channel_title', 'tags', 'description']


    # TODO: Reflection in python? Instead of multiple loops make list of classes and use it in one loop
    for column in txt_columns:
        with UpperCaseFinder('youtube_data/GB_videos_5p.csv', column, data) as finder:
            print(f'"{finder.name}"";"{finder.column_name}"";{finder.found};{finder.total};{finder.missing}')
            reader = finder.data

    for column in txt_columns:
        with LowerCaseFinder('youtube_data/GB_videos_5p.csv', column, data) as finder:
            print(f'"{finder.name}"";"{finder.column_name}"";{finder.found};{finder.total};{finder.missing}')
    
    for column in txt_columns:
        with DigitsFinder('youtube_data/GB_videos_5p.csv', column, data) as finder:
            print(f'"{finder.name}"";"{finder.column_name}"";{finder.found};{finder.total};{finder.missing}')
    
    for column in txt_columns:
        with ContainSpecialCharsFinder('youtube_data/GB_videos_5p.csv', column, data) as finder:
            print(f'"{finder.name}"";"{finder.column_name}"";{finder.found};{finder.total};{finder.missing}')