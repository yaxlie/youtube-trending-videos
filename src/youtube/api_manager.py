# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
# https://developers.google.com/youtube/v3/docs/videos

import os
import pickle
import csv

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from video import Video


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "yt_client_secret.json"
cache = '.manager'

class ApiManager():
    def __init__(self):
        self.save = False

    def __enter__(self):
        # try to load previous object isntance, to prevent from allowing api authorization
        if os.path.exists(cache):
            try:
                with open(cache, 'rb') as f:
                    self = pickle.load(f)
            except Exception as e:
                self.authorize()
                print(e)
        else:
            self.authorize()

        return self

    def __exit__(self, type, value, traceback):
        # save object to remember authorization
        if self.save:
            with open(cache, 'wb') as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def authorize(self):
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        
        self.save = True

    def search_videos(self, publishedBefore, publishedAfter, regionCode, limit=10):
        videos = []

        request = self.youtube.search().list(
            part="snippet",
            order="viewCount",
            type="video",
            maxResults=limit,
            publishedAfter=publishedAfter, # "2017-01-01T00:00:00Z",
            publishedBefore=publishedBefore, # "2018-06-01T00:00:00Z",
            regionCode=regionCode # "GB"
        )
        response = request.execute()

        for video in response['items']:
            _id = video['id']['videoId']
            videos.append(Video(video_id=_id))

        return videos

    def get_videos(self, video_ids=None):
        videos = {}
        if video_ids:
            chunks = [video_ids[x:x+50] for x in range(0, len(video_ids), 50)]
            for _ids in chunks:
                ids = ','.join(_ids)
                request = self.youtube.videos().list(
                    part="contentDetails,statistics,snippet",
                    id=ids
                )
                response = request.execute()

                for response in response['items']:
                    try:
                        video_id = response['id'] 
                        trending_date = None
                        title = response['snippet'].get('title', None)
                        channel_title = response['snippet'].get('channelTitle', None)
                        category_id = response['snippet'].get('categoryId', None)
                        publish_time = response['snippet'].get('publishedAt', None)
                        tags = response['snippet'].get('tags', [])
                        views = response['statistics'].get('viewCount', None)
                        thumbnail_link = response['snippet']['thumbnails']['high']['url'] # get highest resolution 480x360

                        if 'commentCount' in response['statistics']:
                            comment_count = response['statistics']['commentCount']
                            comments_disabled = 'False'
                        else:
                            comment_count = None
                            comments_disabled = 'True'

                        if 'likeCount' in response['statistics']:
                            likes = response['statistics']['likeCount']
                            dislikes = response['statistics']['dislikeCount']
                            ratings_disabled = 'False'
                        else:
                            likes = None
                            dislikes = None
                            ratings_disabled = 'True'

                        video_error_or_removed = 'False'
                        description = response['snippet']['description']

                        video = Video(
                            video_id, 
                            trending_date, 
                            title, 
                            channel_title, 
                            category_id, 
                            publish_time, 
                            tags, 
                            views, 
                            likes, 
                            dislikes, 
                            comment_count, 
                            thumbnail_link, 
                            comments_disabled, 
                            ratings_disabled, 
                            video_error_or_removed, 
                            description)
                        videos[video_id] = video
                    except Exception as e:
                        print(e)
        return videos