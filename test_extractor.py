import pytest
import GLOBALS
from extractor import FakeUrlExtractor


def test_ExtractFromJsonFile_SmallJsonFile_ReturnListOfUrls():
    FakeUrlExtractor()
    extractor = FakeUrlExtractor()

    actual = extractor.extract_urls_from_json(GLOBALS.EXPERT_JSON_LOCATION)
    expected = ["www.yahoo.com.tw",
                "www.google.com.tw",
                "https://ants.example.com/",
                "http://www.example.org/", ]
    assert actual == expected


@pytest.mark.parametrize("filename", [
    "expert.jon",
    "readme.md",
    "expert.cfg",
])
def test_ExtractFromJsonFile_InvalidFileExtension_RaiseException(filename):
    extractor = FakeUrlExtractor()

    with pytest.raises(Exception):
        extractor.extract_urls_from_json(filename)
