import polars as pl
from container_diffoscope.main import compare_file_lists


def test_compare_file_lists_normal_case():
    """Test comparison with typical input containing all types of differences."""

    # Arrange
    df1 = pl.DataFrame(
        {
            "hash": ["hash1", "hash2", "hash3", "hash4"],
            "path": [
                "/bin/common",
                "/bin/modified",
                "/bin/only_df1_1",
                "/bin/only_df1_2",
            ],
        }
    )

    df2 = pl.DataFrame(
        {
            "hash": ["hash1", "hash5", "hash6", "hash7"],
            "path": [
                "/bin/common",
                "/bin/modified",
                "/bin/only_df2_1",
                "/bin/only_df2_2",
            ],
        }
    )

    # Act
    common, changed, only_1, only_2 = compare_file_lists(df1, df2)

    # Assert
    assert len(common) == 1
    assert common["path"][0] == "/bin/common"

    assert len(changed) == 1
    assert changed["path"][0] == "/bin/modified"

    # TODO FIX including also the modifed ones
    assert len(only_1) == 2
    assert set(only_1["path"].to_list()) == {"/bin/only_df1_1", "/bin/only_df1_2"}

    assert len(only_2) == 2
    assert set(only_2["path"].to_list()) == {"/bin/only_df2_1", "/bin/only_df2_2"}


def test_compare_file_lists_empty_dataframes():
    """Test comparison with empty DataFrames."""
    # Arrange
    df1 = pl.DataFrame({"hash": [], "path": []})
    df2 = df1.clone()
    # Act
    common, changed, only_1, only_2 = compare_file_lists(df1, df2)

    # Assert
    assert common.is_empty()
    assert changed.is_empty()
    assert only_1.is_empty()
    assert only_2.is_empty()


def test_compare_file_lists_no_matches():
    """Test comparison when there are no matching files."""
    # Arrange
    df1 = pl.DataFrame(
        {"hash": ["hash1", "hash2"], "path": ["/bin/file1", "/bin/file2"]}
    )
    df2 = pl.DataFrame(
        {"hash": ["hash3", "hash4"], "path": ["/bin/file3", "/bin/file4"]}
    )

    # Act
    common, changed, only_1, only_2 = compare_file_lists(df1, df2)

    # Assert
    assert common.is_empty()
    assert changed.is_empty()
    assert len(only_1) == 2
    assert len(only_2) == 2


def test_compare_file_lists_all_common():
    # Arrange
    """Test comparison when all files are identical."""
    df1 = pl.DataFrame(
        {"hash": ["hash1", "hash2"], "path": ["/bin/file1", "/bin/file2"]}
    )
    df2 = df1.clone()

    # Act
    common, changed, only_1, only_2 = compare_file_lists(df1, df2)

    #
    assert len(common) == 2
    assert changed.is_empty()
    assert only_1.is_empty()
    assert only_2.is_empty()
