import json


class IExtractor:
    def extract_url_from_json(self, filename):
        raise NotImplementedError


class FakeUrlExtractor(IExtractor):
    def extract_url_from_json(self, filename):
        if filename.split(".")[-1] != "json":
            raise Exception("Bad file extension")
        return ["www.yahoo.com.tw",
                "www.google.com.tw",
                "https://ants.example.com/",
                "http://www.example.org/", ]


class UrlExtractor(IExtractor):
    def extract_url_from_json(self, filename):
        if filename.split(".")[-1] != "json":
            raise Exception("Bad file extension")
        with open(filename) as f:
            return [chunk['url'] for chunk in json.load(f)]
