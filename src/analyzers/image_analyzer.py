import os
import pickle
import urllib.request
import csv
from urllib.request import HTTPError
from abc import ABC, abstractmethod
from http.client import RemoteDisconnected
from analyzers.analyzer import Analyzer
from pathlib import Path
from progress.bar import Bar
from copy import copy
from PIL import Image
from io import BytesIO

CACHE_DIR = '.cache'

class ImageAnalyzer(Analyzer):
    def __init__(self, file_name: str, column_name: str, data,  name: str = __name__, multiple=False, limit=None):
        super().__init__(file_name, column_name, data, name, multiple=True)
        self.images = None
        self.cached_images_path = os.path.join(CACHE_DIR, Path(self.file_name).stem)
        self.limit = limit

    def __enter__(self):
        if not self.data:
            with open(self.file_name, newline='', encoding='utf-8', errors='replace') as f:
                self.data = [{key.strip(): value for key, value in row.items()} for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]
        self.total = len(self.data)
        self.download_images()
        self.load_images()

        # If you don't want to process full dataset (time limit)
        if self.limit:
            self.data = self.data[0:self.limit]

        self.convert_data()

        self.count()

        return self
    
    def convert_data(self):
        # convert data to images:
        tmp_data = []
        for data in self.data:
            converted_data = self.data2image(data)
            if converted_data:
                tmp_data.append(converted_data)
        self.data = tmp_data

    def data2image(self, data):
        url = data[self.column_name]
        if url in self.images:
            image_data = self.images[url]
            image = Image.open(BytesIO(image_data))
            data[self.column_name] = image
            return data
        else:
            self.missing += 1
            return None

    @abstractmethod
    def decide(self, data: str, **kwargs):
        pass
    
    def load_images(self):
        with open(self.cached_images_path, 'rb') as f:
            self.images = pickle.load(f)

    def download_images(self):
        if not os.path.exists(self.cached_images_path):
            images = {}

            bar = Bar('Downloading images...', max=len(self.data))

            for row in self.data:
                bar.next()
                try:
                    url = row[self.column_name]
                    downloaded = False
                    while not downloaded:
                        try:
                            content = urllib.request.urlopen(url).read()
                            images[url] = content
                            downloaded = True
                        except (RemoteDisconnected, ConnectionError):
                            pass
                except (HTTPError, urllib.error.URLError):
                    continue
            bar.finish()

            with open(self.cached_images_path,'wb') as f:
                pickle.dump(images, f)