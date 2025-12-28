import pytest
import polars as pl
import shutil
from filesystem_comparison import load_list_to_dataframe


@pytest.fixture(autouse=True)
def cleanup(tmp_path):
    yield
    if tmp_path.exists():
        shutil.rmtree(tmp_path)


@pytest.fixture
def sample_hash_file(tmp_path):
    content = """abc123 * /bin/bash
def456 * /etc/config
ghi789 * /usr/lib/file.so"""
    file_path = tmp_path / "hash_list.txt"
    file_path.write_text(content)
    return str(file_path)


def test_load_list_to_dataframe_successful(sample_hash_file):
    df = load_list_to_dataframe(sample_hash_file)

    assert isinstance(df, pl.DataFrame)
    assert df.shape == (3, 2)
    assert df.columns == ["hash", "path"]
    assert df["hash"].to_list() == ["abc123", "def456", "ghi789"]
    assert df["path"].to_list() == ["/bin/bash", "/etc/config", "/usr/lib/file.so"]


def test_load_list_to_dataframe_empty_file(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    df = load_list_to_dataframe(str(empty_file))
    assert df.is_empty()
    assert df.columns == ["hash", "path"]


def test_load_list_to_dataframe_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        load_list_to_dataframe("nonexistent.txt")
