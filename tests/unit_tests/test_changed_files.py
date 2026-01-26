import polars as pl
from container_diffoscope.comparator import _get_changed_files


def test_basic_changed_files():
    # Arrange
    df1 = pl.DataFrame(
        {"hash": ["123", "456", "789"], "path": ["/bin/a", "/bin/b", "/bin/c"]}
    )
    df2 = pl.DataFrame(
        {"hash": ["999", "456", "000"], "path": ["/bin/a", "/bin/b", "/bin/c"]}
    )

    # Act
    result = _get_changed_files(df1, df2)

    # Assert
    assert len(result) == 2
    assert result["path"].to_list() == ["/bin/a", "/bin/c"]
    assert result["hash"].to_list() == ["123", "789"]
    assert result["hash_2"].to_list() == ["999", "000"]


def test_no_changed_files():
    # Arrange
    df1 = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/a", "/bin/b"]})
    df2 = df1.clone()

    # Act
    result = _get_changed_files(df1, df2)

    # Assert
    assert len(result) == 0


def test_empty_dataframes():
    # Arrange
    df1 = pl.DataFrame({"hash": [], "path": []})
    df2 = pl.DataFrame({"hash": ["123"], "path": ["/bin/a"]})

    # Act
    result = _get_changed_files(df1, df2)

    # Assert
    assert len(result) == 0


def test_all_files_changed():
    # Arrange
    df1 = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/a", "/bin/b"]})
    df2 = pl.DataFrame({"hash": ["789", "012"], "path": ["/bin/a", "/bin/b"]})

    # Act
    result = _get_changed_files(df1, df2)

    # Assert
    assert len(result) == 2
    assert result["hash"].to_list() == ["123", "456"]
    assert result["hash_2"].to_list() == ["789", "012"]


def test_different_paths():
    # Arrange
    df1 = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/a", "/bin/b"]})
    df2 = pl.DataFrame({"hash": ["123", "456"], "path": ["/bin/x", "/bin/y"]})

    # Act
    result = _get_changed_files(df1, df2)

    # Assert
    assert len(result) == 0
