
"""
Container-Diffoscope: Docker Filesystem Comparison Tool

For detailed documentation, see: source_code/docs.md
"""

import polars as pl
import atexit
import shutil
import typer
from .extractor import *
from .diffoscope_runner import *
from .comparator import *

NEW_FILE_PRINT_THRESHOLD = 20  # Number of files that can be different between the images and the list will be printed
UPDATED_FILE_TRESHOLD = 15

app = typer.Typer()


def _analyze_changed_files(
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


def __cleanup_cache(cache_dir: str) -> None:
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
    atexit.register(__cleanup_cache, cache_dir)

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
        _analyze_changed_files(changed_files, image_1, image_2, export_dir)
    else:
        print(
            f"\nThere are too many files that are different between the images ({len(changed_files)}).",
            flush=True,
        )
        print("changes files are:")
        for row in changed_files.iter_rows(named=True):
            print(f"  {row['path']}", flush=True)


@app.command()
def main(
    image_1: str = typer.Argument(..., help="First Docker image to compare"),
    image_2: str = typer.Argument(..., help="Second Docker image to compare"),
    output_dir: str = typer.Option("temp_results", help="Output directory for comparison results"),
):
    """
    Compare two Docker images' filesystems and generate detailed comparisons of changed files.
    """
    full_output_dir = f"{output_dir}/file_diff"
    compare_filesystem(image_1, image_2, full_output_dir)


def cli():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    cli()
