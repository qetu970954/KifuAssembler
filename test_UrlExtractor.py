import pytest

from UrlExtractor import FakeUrlExtractor


def test_ExtractFromJsonFile_SmallJsonFile_ReturnListOfUrls():
    extractor = FakeUrlExtractor()

    actual = extractor.extract_from_json_file("expert.json")

    assert type(actual) == list
    assert len(actual) == 4


@pytest.mark.parametrize("filename", [
    "expert.jon",
    "readme.md",
    "expert.cfg",
    ])
def test_ExtractFromJsonFile_InvalidFileExtension_RaiseException(filename):
    extractor = FakeUrlExtractor()

    with pytest.raises(Exception):
        extractor.extract_from_json_file(filename)
