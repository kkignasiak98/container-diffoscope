import polars as pl
import os.path

def load_list_to_dataframe(path: str) -> pl.DataFrame:
    """
    Load the file hash list into a polars DataFrame.

    Args:
        image (str): Name of the Docker image whose hash list should be loaded

    Returns:
        pl.DataFrame: A DataFrame with two columns:
            - hash: SHA256 hash of the file
            - path: Path of the file in the container
    """
    if os.path.getsize(path) == 0:
        return pl.DataFrame({"hash": [], "path": []})
    df = pl.read_csv(path, separator=" ", has_header=False, truncate_ragged_lines=True)
    df = df.rename({df.columns[0]: "hash", df.columns[2]: "path"})
    df = df.select(["hash", "path"])
    return df


def _get_common_files(df1: pl.DataFrame, df2: pl.DataFrame) -> pl.DataFrame:
    """
    Find files that are identical (same hash and path) between two DataFrames.

    Args:
        df1 (pl.DataFrame): First DataFrame
        df2 (pl.DataFrame): Second DataFrame

    Returns:
        pl.DataFrame: A DataFrame containing only the files that are the same in both
                     DataFrames
    """
    if df1.is_empty() or df2.is_empty():
        return pl.DataFrame({"hash": [], "path": []})
    common_rows = df1.join(df2, on=["hash", "path"], how="inner")
    return common_rows


def _get_changed_files(df1: pl.DataFrame, df2: pl.DataFrame) -> pl.DataFrame:
    """
    Find files that exist in both DataFrames but have different content.

    Args:
        df1 (pl.DataFrame): First DataFrame
        df2 (pl.DataFrame): Second DataFrame

    Returns:
        pl.DataFrame: A DataFrame containing files that exist in both DataFrames
                     but have different content(based of the hashes)
    """
    if df1.is_empty() or df2.is_empty():
        return pl.DataFrame({"hash": [], "path": []})
    different_hashes = df1.join(df2, on="path", how="inner", suffix="_2")
    changed_files = different_hashes.filter(
        different_hashes["hash"] != different_hashes["hash_2"]
    )
    return changed_files


def _filter_files(df1: pl.DataFrame, df2: pl.DataFrame) -> pl.DataFrame:
    """
    Find files that exist only in the first DataFrame and not in the second.

    Args:
        df1 (pl.DataFrame): First DataFrame
        df2 (pl.DataFrame): Second DataFrame

    Returns:
        pl.DataFrame: A DataFrame containing only the files that exist in first DataFrame
                     and not in the second DataFrame
    """
    if df1.is_empty():
        return pl.DataFrame({"hash": [], "path": []})
    if df2.is_empty():
        return df1
    return df1.join(df2, on=["path"], how="anti")

def compare_file_lists(
    df1: pl.DataFrame, df2: pl.DataFrame
) -> tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    """
    Compare file lists between two Dataframes and categorize the differences.

    Args:
        df1 (pl.DataFrame): First DataFrame
        df2 (pl.DataFrame): Second DataFrame

    Returns:
        tuple containing:
            - common_rows (pl.DataFrame): Files identical in both images
            - changed_files (pl.DataFrame): Files that exist in both but have different content
            - only_in_df1 (pl.DataFrame): Files that exist only in first image
            - only_in_df2 (pl.DataFrame): Files that exist only in second image
    """

    common_rows = _get_common_files(df1, df2)
    changed_files = _get_changed_files(df1, df2)
    only_in_df1 = _filter_files(df1, df2)
    only_in_df2 = _filter_files(df2, df1)

    return (common_rows, changed_files, only_in_df1, only_in_df2)
