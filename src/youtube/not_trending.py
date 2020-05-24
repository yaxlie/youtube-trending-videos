import os
import csv
from api_manager import ApiManager
from video import Video

csv_files = ['data\\GB_videos_5p.csv']

class Trending():
    def __init__(self, date):
        self.date = date # date of trending check
        self.videos = []

    def get_latest_video(self):
        self.videos.sort(key=lambda x: x.publish_time, reverse=True)
        return str(self.videos[0].publish_time).split('T')[0] + 'T00:00:00Z'

    # Don't pick from tail (there can be a few videos from completely different date [very old])
    def get_oldest_video(self):
        self.videos.sort(key=lambda x: x.publish_time, reverse=False)
        index = int(0.1 * len(self.videos))
        return str(self.videos[index].publish_time).split('T')[0] + 'T00:00:00Z'

    def add_video(self, video:Video):
        if video.trending_date == self.date and video.publish_time:
            self.videos.append(video)


def get_trendings(csv_file):
    trendings = {}
    trending_ids = []

    with open(csv_file, errors='ignore') as csv_in:
        for row in csv.DictReader(csv_in, skipinitialspace=True, delimiter=';'):
            try:
                video_id = row['video_id']
                trending_date = row['trending_date']
                publish_time = row['publish_time']
                video = Video(trending_date=trending_date, publish_time=publish_time, video_id=video_id)
                if not trending_date in trendings:
                    trendings[trending_date] = Trending(trending_date)
                trendings[trending_date].add_video(video)
                trending_ids.append(video_id)

            except Exception as e:
                print(e)
    return (trendings, trending_ids)


def get_not_trendings(csv_file, region='GB', limit=10, limit_trendings=None):
    # Get trendings to find date range
    trendings, trending_ids = get_trendings(csv_file)
    found_videos = []
    i = 0

    with ApiManager() as manager:
        for trending_key, trending_value in trendings.items():
            videos = manager.search_videos(trending_value.get_latest_video(), trending_value.get_oldest_video(), region, limit)
            found_videos = found_videos + videos
            i += 1
            if limit_trendings and i > limit_trendings:
                break

        # Remove videos, that are on "trending" list
        ids = [video.video_id for video in found_videos if video.video_id not in trending_ids]
        
        # Remove duplicates
        ids = list(set(ids))

        not_trendings = manager.get_videos(ids)

        return not_trendings

for csv_file in csv_files:
    videos = get_not_trendings(csv_file, limit_trendings=10)
    filename = csv_file.replace('.csv', '')
    with open(os.path.join('out', f'{filename}-not-trending.csv'), 'w', errors='ignore') as csv_out:
        for video in videos:
            try:
                video = videos[row.split(';')[0]]
                row_to_write = str(video) + '\n'
                csv_out.write(row_to_write)
            except Exception as e:
                print(e)