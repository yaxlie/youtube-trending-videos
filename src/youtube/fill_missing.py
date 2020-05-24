import os
import csv
from api_manager import ApiManager
from video import Video

# csv_files = ['data\\GB_videos_5p.csv', 'data\\US_videos_5p.csv']
csv_files = ['data\\GB_videos_5p.csv']

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

def try_fill_cell(csv_file, ids, break_after=None):
    i = 0

    if break_after:
        ids = ids[0:break_after]

    with ApiManager() as manager:
        videos = manager.get_videos(ids)

    with open(csv_file, errors='ignore') as csv_in:
        header = csv_in.readline()
        with open(os.path.join('out', csv_file), 'w', errors='ignore') as csv_out:
            csv_out.write(header)
            for row in csv_in.readlines():
                try:
                    video = videos[row.split(';')[0]]
                    row_to_write = str(video) + '\n'
                except Exception as e:
                    row_to_write = [r for r in row.split(';')]
                    row_to_write[14] = 'True'
                    row_to_write = ';'.join(row_to_write)
                    print(e)

                csv_out.write(row_to_write)
                i += 1

                if break_after and i == break_after:
                    break

for csv_file in csv_files:
    ids = get_ids(csv_file)
    # For testing
    # try_fill_cell(csv_file, ids, 100)

    # For getting full data
    try_fill_cell(csv_file, ids)