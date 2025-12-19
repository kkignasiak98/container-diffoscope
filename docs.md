# DockFS-Diff

A powerful Docker filesystem comparison tool that analyzes differences between two Docker images at the file level.

**Source code**: `source_code/filesystem_comparison.py`

## Overview

DockFS-Diff compares the filesystems of two Docker images by:
1. Exporting each image's filesystem to tar archives
2. Generating SHA256 hash lists for all files
3. Categorizing files as identical, modified, or unique to each image
4. Creating detailed comparisons for modified files using diffoscope

## Features

- **Complete Filesystem Analysis**: Exports and analyzes entire Docker image filesystems
- **Hash-based Comparison**: Uses SHA256 hashes to detect file changes accurately
- **Detailed Diff Reports**: Generates markdown reports showing exact differences between modified files
- **Smart Thresholds**: Configurable limits for when to generate detailed comparisons vs. summary lists
- **Automatic Cleanup**: Removes temporary files after analysis

## Usage

```bash
python filesystem_comparison.py <image_1> <image_2> [--output-dir OUTPUT_DIR]
```

### Parameters

- `image_1`: Name or ID of the first Docker image
- `image_2`: Name or ID of the second Docker image
- `--output-dir`: Output directory for comparison results (default: "temp_results")

### Example

```bash
python filesystem_comparison.py ubuntu:20.04 ubuntu:22.04 --output-dir comparison_results
```

## Output

The tool provides:

1. **Summary Statistics**: Count of identical, modified, and unique files
2. **File Lists**: Lists of files unique to each image (if under threshold)
3. **Detailed Comparisons**: Markdown files with side-by-side diffs for modified files

## Configuration

- `NEW_FILE_PRINT_THRESHOLD = 20`: Maximum number of new files to list individually
- `UPDATED_FILE_TRESHOLD = 15`: Maximum number of changed files to analyze in detail

## Dependencies

- Docker (for image export)
- Python packages: polars, typer
- diffoscope (for detailed file comparisons)
- tar, sha256sum (system utilities)

## How It Works

1. **Export Phase**: Creates temporary containers and exports filesystems as tar archives
2. **Hashing Phase**: Extracts files and generates SHA256 hash lists
3. **Analysis Phase**: Compares hash lists to categorize file differences
4. **Comparison Phase**: Uses diffoscope to generate detailed diffs for modified files
5. **Cleanup Phase**: Removes all temporary files and containers

## File Categories

- **Common Files**: Identical files present in both images (same path and hash)
- **Modified Files**: Files present in both images but with different content
- **Unique Files**: Files present in only one of the images

## Cache Structure

```
cache/
├── image1.tar          # Exported filesystem
├── image2.tar          # Exported filesystem
├── image1_list.txt     # Hash and path list
├── image2_list.txt     # Hash and path list
├── image1/             # Extracted files for comparison
└── image2/             # Extracted files for comparison
```