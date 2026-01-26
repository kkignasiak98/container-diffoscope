
import subprocess
import os.path

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