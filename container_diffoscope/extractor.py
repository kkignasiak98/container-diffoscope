import subprocess

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

def extract_file_from_tar(file_path: str, image: str) -> None:
    """
    Extract a single file (based on the file path) from a Docker image tar archive.

    Args:
        file_path (str): Path of the file to extract from the tar archive
        image (str): Name of the Docker image whose tar archive contains the file
    """
    cmd = f'tar -xf cache/{image}.tar -C cache/{image} "{file_path}"'
    subprocess.run(cmd, shell=True)