class IExtractor:
    def extract_from_json_file(self, filename):
        raise NotImplementedError


class FakeUrlExtractor(IExtractor):
    def extract_from_json_file(self, filename : str):
        if filename.split(".")[-1] != "json":
            raise Exception("Bad file extension")
        return ["www.yahoo.com.tw",
                "www.google.com.tw",
                "https://ants.example.com/",
                "http://www.example.org/", ]
