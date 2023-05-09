import os
import shutil
from pathlib import Path

# dib imports
from dib.core import DIB

mock_string_list = ["test", "py"]
second_mock_string_list = ["ter", "fo"]


def test_search_file_system():
    """
    Giving the dib method a list with only 'er' will five an empty list
    because there is no match to 'er' in the tests directory.
    """
    dib = DIB()

    assert dib._search_file_system(["home"]) == {'home': []}


def test_temporary_directory():
    """
    This test will create a temporary directory tree and test the search
    function on this tree.
    """
    root = Path(os.path.dirname(os.path.abspath(__file__)))
    tmp_folder = Path(f"{root}/test")
    python_folder = Path(tmp_folder) / "python"
    terraform_folder = Path(tmp_folder) / "terraform"
    foo_folder = Path(tmp_folder) / "foo"
    path_list = [tmp_folder, python_folder, terraform_folder, foo_folder]
    for path in path_list:
        if not path.exists():
            path.mkdir()

    dib = DIB(current_dir=root)

    assert dib._search_file_system(mock_string_list) == {
        'py':
            [f'{root.parents[0]}/tests/test/python'],
        'test':
            [f'{root.parents[0]}/tests/test',
             f'{root.parents[0]}/tests/test/foo',
             f'{root.parents[0]}/tests/test/python',
             f'{root.parents[0]}/tests/test/terraform']
    }
    assert dib._search_file_system(second_mock_string_list) == {
        'fo':
            [f'{root.parents[0]}/tests/test/foo',
             f'{root.parents[0]}/tests/test/terraform'],
        'ter':
            [f'{root.parents[0]}/tests/test/terraform']
    }

    # Cleanup of the tmp dir
    shutil.rmtree(tmp_folder)
