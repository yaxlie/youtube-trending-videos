import os
import csv
from api_manager import ApiManager
from video import Video

csv_files = ['data\\GB_videos_5p.csv', 'data\\US_videos_5p.csv']

def get_ids(csv_file):
    ids = []
    with open(csv_file, errors='ignore') as csv_in:
        for row in csv.DictReader(csv_in, skipinitialspace=True, delimiter=';'):
            try:
                _id = row['video_id']
                if '#' not in _id:
                    ids.append(row['video_id'])
            except Exception as e:
                print(e)
    return ids

def try_fill_cell(column_name, csv_file, ids, break_after=None):
    i = 0

    with ApiManager() as manager:
        videos = manager.get_videos(ids)

    with open(csv_file, errors='ignore') as csv_in:
        with open(os.path.join('out', csv_file), 'w', errors='ignore') as csv_out:
            for row in csv.DictReader(csv_in, skipinitialspace=True, delimiter=';'):
                if column_name in row:
                    try:
                        video = videos[row['video_id']]
                        row[column_name] = video.__dict__[column_name] # TODO: for every/choosen column
                    except Exception as e:
                        print(e)

                csv_out.write(';'.join(row.values()) + '\n')
                i += 1

                if break_after and i == break_after:
                    break

for csv_file in csv_files:
    ids = get_ids(csv_file)
    try_fill_cell('category_id', csv_file, ids, 100)