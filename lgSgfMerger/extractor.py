import json
import os


class IExtractor:
    def extract(self, filename, attribute):
        raise NotImplementedError


class FakeExtractor(IExtractor):
    def extract(self, filename, attribute):
        if filename.split(".")[-1] != "json":
            raise Exception("Bad file extension")
        return ["www.yahoo.com.tw",
                "www.google.com.tw",
                "https://ants.example.com/",
                "http://www.example.org/", ]


class Extractor(IExtractor):
    def extract(self, filename, attribute):
        if not os.path.isfile(filename):
            return []
        if filename.split(".")[-1] != "json":
            raise Exception("Bad file extension")
        with open(filename) as f:
            return [chunk[attribute] for chunk in json.load(f)]
