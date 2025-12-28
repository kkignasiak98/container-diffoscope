import polars as pl
from filesystem_comparison import filter_files


def test_basic_filter():
    df1 = pl.DataFrame(
        {"hash": ["123", "456", "789"], "path": ["/bin/a", "/bin/b", "/bin/c"]}
    )
    df2 = pl.DataFrame({"hash": ["123", "999"], "path": ["/bin/a", "/bin/d"]})

    result = filter_files(df1, df2)
    assert len(result) == 2
    assert result["path"].to_list() == ["/bin/b", "/bin/c"]
    assert result["hash"].to_list() == ["456", "789"]


def test_empty_dataframes():
    # Arrange
    df1 = pl.DataFrame({"hash": [], "path": []})
    df2 = pl.DataFrame({"hash": ["123"], "path": ["/bin/a"]})

    # Act
    result_1 = filter_files(df1, df2)
    result_2 = filter_files(df2, df1)

    # Assert
    assert len(result_1) == 0
    assert len(result_2) == 1


def test_identical_dataframes():
    # Arrange
    df = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/a", "/bin/b"]})

    # Act
    result = filter_files(df, df)
    # Assert
    assert len(result) == 0


def test_same_hash_different_paths():
    # Arrange
    df1 = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/a", "/bin/b"]})
    df2 = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/x", "/bin/y"]})

    # Act
    result = filter_files(df1, df2)
    # Assert
    assert len(result) == 2
