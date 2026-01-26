import os
import pytest
from container_diffoscope.main import __cleanup_cache


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Create a temporary cache directory with some test files."""
    cache_dir = tmp_path / "test_cache"
    cache_dir.mkdir()

    # Create some test files and subdirectories
    (cache_dir / "file1.txt").write_text("test content")
    subdir = cache_dir / "subdir"
    subdir.mkdir()
    (subdir / "file2.txt").write_text("test content 2")

    return str(cache_dir)


def test_cleanup_cache_existing_directory(temp_cache_dir):
    """Test cleanup of an existing cache directory."""
    assert os.path.exists(temp_cache_dir)
    __cleanup_cache(temp_cache_dir)
    assert not os.path.exists(temp_cache_dir)


def test_cleanup_cache_nonexistent_directory():
    """Test cleanup_cache with a non-existent directory."""
    non_existent_dir = "/tmp/nonexistent_dir_12345"
    __cleanup_cache(non_existent_dir)  # Should not raise any exception
