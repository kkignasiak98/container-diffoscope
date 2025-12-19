
"""
DockFS-Diff: Docker Filesystem Comparison Tool

For detailed documentation, see: source_code/docs/dockfs-diff.md
"""

import subprocess
import polars as pl
import os.path
import atexit
import shutil
import typer
from typing import Annotated

NEW_FILE_PRINT_THRESHOLD = 20  # Number of files that can be different between the images and the list will be printed
UPDATED_FILE_TRESHOLD = 15


def export_filesystem_from_image(image: str) -> None:
    """
    Export the filesystem from a Docker image to a tar archive.

    Args:
        image (str): Name or ID of the Docker image to export

    The function performs the following steps:
    1. Creates a temporary container from the image
    2. Creates a cache directory for the image tar archive
    3. Exports the container's filesystem to a tar archive
    4. Removes the temporary container
    """
    subprocess.run(
        f"docker create --name image_temp {image}",
        shell=True,
        stdout=subprocess.DEVNULL,
        check=True,
    )
    subprocess.run(f"mkdir -p cache/{image}", shell=True, check=True)
    subprocess.run(
        f"docker export image_temp > cache/{image}.tar",
        shell=True,
        stdout=subprocess.DEVNULL,
        check=True,
    )
    subprocess.run(
        "docker rm image_temp", shell=True, stdout=subprocess.DEVNULL, check=True
    )


def get_hash_file_list(image: str) -> None:
    """
    Generate a list of files with their SHA256 hashes from a Docker image tar archive.

    Args:
        image (str): Name of the Docker image whose filesystem has been exported to tar

    The function extracts the tar archive and generates a text file in the cache directory
    containing hash and filepath pairs for each file in the image.
    """
    cmd = f'tar xf cache/{image}.tar --to-command=\'sh -c "sha256sum | sed \\"s|-|$TAR_FILENAME|\\""\' > cache/{image}_list.txt'
    subprocess.run(cmd, shell=True)


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


def get_common_files(df1: pl.DataFrame, df2: pl.DataFrame) -> pl.DataFrame:
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


def get_changed_files(df1: pl.DataFrame, df2: pl.DataFrame) -> pl.DataFrame:
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


def filter_files(df1: pl.DataFrame, df2: pl.DataFrame) -> pl.DataFrame:
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


def extract_file_from_tar(file_path: str, image: str) -> None:
    """
    Extract a single file (based on the file path) from a Docker image tar archive.

    Args:
        file_path (str): Path of the file to extract from the tar archive
        image (str): Name of the Docker image whose tar archive contains the file
    """
    cmd = f'tar -xf cache/{image}.tar -C cache/{image} "{file_path}"'
    subprocess.run(cmd, shell=True)


def get_detailed_file_comparison(
    file_path_1: str, file_path_2: str, export_dir: str
) -> None:
    """
    Generate a detailed comparison between two files (similar to git comparison) and save it as markdown.

    Args:
        file_path_1 (str): Path to the first file
        file_path_2 (str): Path to the second file
        export_dir (str): Directory where the comparison markdown file will be saved

    The function uses diffoscope to generate a detailed comparison between the files
    and saves the output as a markdown file named after first file in the comparison.
    """
    os.makedirs(export_dir, exist_ok=True)
    base_name = os.path.basename(file_path_1)
    print(f"Running comparison for {base_name}.", flush=True)
    cmd = f"diffoscope {file_path_1} {file_path_2}  --exclude-directory-metadata yes  --diff-context=2 --markdown {export_dir}/{base_name}.md"
    subprocess.run(cmd, shell=True)


def analyze_changed_files(
    changed_files: pl.DataFrame, image_1: str, image_2: str, export_dir: str
) -> None:
    """
    Generate detailed comparisons for all files that are different between two Docker images.

    Args:
        changed_files (pl.DataFrame): DataFrame containing files that are different between the two images
        image_1 (str): Name of the first Docker image
        image_2 (str): Name of the second Docker image
        export_dir (str): Directory where the comparison files will be saved

    For each changed file pair, they are extracted from .tar files and compared using diffoscope tool.
    """
    for row in changed_files.iter_rows(named=True):
        path = row["path"]

        extract_file_from_tar(path, image_1)
        extract_file_from_tar(path, image_2)

        file_path_1 = f"cache/{image_1}/{path}"
        file_path_2 = f"cache/{image_2}/{path}"

        get_detailed_file_comparison(file_path_1, file_path_2, export_dir)


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

    common_rows = get_common_files(df1, df2)
    changed_files = get_changed_files(df1, df2)
    only_in_df1 = filter_files(df1, df2)
    only_in_df2 = filter_files(df2, df1)

    return (common_rows, changed_files, only_in_df1, only_in_df2)


def cleanup_cache(cache_dir: str) -> None:
    """
    Remove the specified temporary cache directory and all its contents.

    Args:
        cache_dir (str): Path to the cache directory to be removed

    This function is registered as an exit handler to ensure cleanup
    of temporary files after the program finishes or crashes.
    """
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir, ignore_errors=True)


def compare_filesystem(image_1: str, image_2: str, export_dir: str) -> None:
    """
    Compare filesystems of two Docker images and generate detailed comparisons of differences.

    Args:
        image_1 (str): Name of the first Docker image to compare
        image_2 (str): Name of the second Docker image to compare
        export_dir (str): Directory where detailed file comparisons will be saved

    The function performs the following steps:
    1. Exports filesystems from both images as a tar archive
    2. Generates the list of files with their SHA256 hashes
    3. Find files that are identical, changed, or unique to each image
    4. Generates detailed comparisons for changed files
    5. Cleans up temporary files
    """
    cache_dir = "cache"
    atexit.register(cleanup_cache, cache_dir)

    export_filesystem_from_image(image_1)
    export_filesystem_from_image(image_2)

    get_hash_file_list(image_1)
    get_hash_file_list(image_2)

    df1 = load_list_to_dataframe(f"cache/{image_1}_list.txt")
    df2 = load_list_to_dataframe(f"cache/{image_2}_list.txt")

    common_rows, changed_files, only_in_df1, only_in_df2 = compare_file_lists(df1, df2)

    print("\n=== Filesystem Comparison Summary ===", flush=True)
    print(f"🔄 Common files (identical content): {len(common_rows)}", flush=True)
    print(f"📝 Modified files: {len(changed_files)}", flush=True)
    print(f"➖ Files unique to {image_1}: {len(only_in_df1)}", flush=True)
    print(f"➕ Files unique to {image_2}: {len(only_in_df2)}", flush=True)
    print("================================\n", flush=True)

    if len(only_in_df2) < NEW_FILE_PRINT_THRESHOLD:
        print(f"\nFiles only in {image_2}:", flush=True)
        for row in only_in_df2.iter_rows(named=True):
            print(f"  {row['path']}", flush=True)
        print("", flush=True)

    if len(changed_files) < UPDATED_FILE_TRESHOLD:
        analyze_changed_files(changed_files, image_1, image_2, export_dir)
    else:
        print(
            f"\nThere are too many files that are different between the images ({len(changed_files)}).",
            flush=True,
        )
        print("changes files are:")
        for row in changed_files.iter_rows(named=True):
            print(f"  {row['path']}", flush=True)


def main(
    image_1: str,
    image_2: str,
    output_dir: Annotated[
        str, typer.Option(help="Output directory for comparison results")
    ] = "temp_results",
):
    """
    Compare two Docker images' filesystems and generate detailed comparisons of changed files.
    """
    full_output_dir = f"{output_dir}/file_diff"
    compare_filesystem(image_1, image_2, full_output_dir)


if __name__ == "__main__":
    typer.run(main)
