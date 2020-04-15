import os
import pickle
import urllib.request
import csv
from urllib.request import HTTPError
from abc import ABC, abstractmethod
from http.client import RemoteDisconnected
from finders.finder import AttributeFinder
from pathlib import Path

CACHE_DIR = '.cache'

class ImageFinder(AttributeFinder):
    def __init__(self, file_name: str, column_name: str, data,  name: str = __name__, multiple=False):
        super().__init__(file_name, column_name, data, name, multiple=True)
        self.images = None
        self.cached_images_path = os.path.join(CACHE_DIR, Path(self.file_name).stem)

    def __enter__(self):
        if not self.data:
            with open(self.file_name, newline='', encoding='utf-8', errors='replace') as f:
                self.data = [{key.strip(): value for key, value in row.items()} for row in csv.DictReader(f, skipinitialspace=True, delimiter=';')]
        self.total = len(self.data)
        self.download_images()
        self.load_images()
        self.count()

        return self
    
    @abstractmethod
    def is_condition_met(self, data: str, **kwargs):
        pass
    
    def load_images(self):
        with open(self.cached_images_path, 'rb') as f:
            self.images = pickle.load(f)

    def download_images(self):
        from progress.bar import Bar

        if not os.path.exists(self.cached_images_path):
            images = {}

            bar = Bar('Processing', max=len(self.data))

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