import polars as pl
from container_diffoscope.comparator import _get_common_files


def test_basic_common_files():
    # Arrange
    df1 = pl.DataFrame(
        {"hash": ["123", "456", "789"], "path": ["/bin/a", "/bin/b", "/bin/c"]}
    )
    df2 = pl.DataFrame(
        {"hash": ["123", "456", "999"], "path": ["/bin/a", "/bin/b", "/bin/d"]}
    )

    # Act
    result = _get_common_files(df1, df2)

    # Assert
    assert len(result) == 2
    assert result["path"].to_list() == ["/bin/a", "/bin/b"]
    assert result["hash"].to_list() == ["123", "456"]


def test_no_common_files():
    # Arrange
    df1 = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/a", "/bin/b"]})
    df2 = pl.DataFrame({"hash": ["789", "012"], "path": ["/bin/c", "/bin/d"]})

    # Act
    result = _get_common_files(df1, df2)

    # Assert
    assert len(result) == 0


def test_empty_dataframes():
    # Arrange
    df1 = pl.DataFrame({"hash": [], "path": []})
    df2 = pl.DataFrame({"hash": ["123"], "path": ["/bin/a"]})

    # Act
    result = _get_common_files(df1, df2)

    # Assert
    assert len(result) == 0


def test_all_files_common():
    # Arrange
    df1 = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/a", "/bin/b"]})
    df2 = df1.clone()

    # Act
    result = _get_common_files(df1, df2)

    # Assert
    assert len(result) == 2
    assert result.equals(df1)
