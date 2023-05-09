# dib imports
from dib.constants import *
from dib.core import DIB

# 3rd party imports
import pytest

mock_string_list = ["test", "py"]
second_mock_string_list = ["ter", "fo"]


def test_search_file_system():
    dib = DIB()

    assert dib._search_file_system(["er"]) == {'er': []}
