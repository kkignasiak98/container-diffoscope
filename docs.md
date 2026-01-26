<div align="center">

# 🐋 Container Diffoscope

<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/palette/macchiato.png" width="600"/>

### *Elegant Docker filesystem comparison, brewed with care* ☕

[![Catppuccin](https://img.shields.io/badge/Catppuccin-Macchiato-f5bde6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgdmlld0JveD0iMCAwIDY0IDY0Ij48cGF0aCBmaWxsPSIjZjViZGU2IiBkPSJNMzIgNEMxNi41MzYgNCA0IDE2LjUzNiA0IDMyYzAgMTUuNDY0IDEyLjUzNiAyOCAyOCAyOHMyOC0xMi41MzYgMjgtMjhDNjAgMTYuNTM2IDQ3LjQ2NCA0IDMyIDR6Ii8+PC9zdmc+)](https://github.com/catppuccin)
[![Python](https://img.shields.io/badge/Python-3.10+-a6da95?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Required-8aadf4?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-f5a97f?style=for-the-badge)](LICENSE)

---

*A powerful Docker filesystem comparison tool that analyzes differences between two Docker images at the file level.*

</div>

---

## 🌸 Overview

**Container Diffoscope** compares the filesystems of two Docker images through an elegant pipeline:

| Step | Description |
|:----:|-------------|
| 🗃️ | **Export** each image's filesystem to tar archives |
| 🔐 | **Generate** SHA256 hash lists for all files |
| 📊 | **Categorize** files as identical, modified, or unique |
| 🔍 | **Create** detailed comparisons using diffoscope |

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎯 Core Capabilities

- 📦 **Complete Filesystem Analysis**
  > Exports and analyzes entire Docker image filesystems

- 🔒 **Hash-based Comparison**
  > Uses SHA256 hashes for accurate change detection

- 📝 **Detailed Diff Reports**
  > Markdown reports with exact file differences

</td>
<td width="50%">

### 🛠️ Smart Features

- ⚡ **Configurable Thresholds**
  > Smart limits for detailed vs. summary comparisons

- 🧹 **Automatic Cleanup**
  > Removes temporary files after analysis

- 🎨 **Beautiful Output**
  > Clean, readable markdown reports

</td>
</tr>
</table>

---

## 🚀 Usage

```bash
# Basic usage
python -m container_diffoscope <image_1> <image_2>

# With custom output directory
python -m container_diffoscope <image_1> <image_2> --output-dir OUTPUT_DIR
```

### 📋 Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image_1` | Name or ID of the first Docker image | *required* |
| `image_2` | Name or ID of the second Docker image | *required* |
| `--output-dir` | Output directory for comparison results | `temp_results` |

### 💡 Example

```bash
# Compare Ubuntu versions
python -m container_diffoscope ubuntu:20.04 ubuntu:22.04 --output-dir comparison_results
```

---

## 📤 Output

<details>
<summary><b>🔹 Summary Statistics</b></summary>

> Count of identical, modified, and unique files across both images

</details>

<details>
<summary><b>🔹 File Lists</b></summary>

> Lists of files unique to each image (if under threshold)

</details>

<details>
<summary><b>🔹 Detailed Comparisons</b></summary>

> Markdown files with side-by-side diffs for modified files

</details>

---

## ⚙️ Configuration

| Variable | Value | Description |
|----------|:-----:|-------------|
| `NEW_FILE_PRINT_THRESHOLD` | `20` | Maximum new files to list individually |
| `UPDATED_FILE_THRESHOLD` | `15` | Maximum changed files to analyze in detail |

---

## 📦 Dependencies

<table>
<tr>
<td>

**🐳 System**
- Docker
- tar
- sha256sum

</td>
<td>

**🐍 Python**
- polars
- typer

</td>
<td>

**🔧 Tools**
- diffoscope

</td>
</tr>
</table>

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   📥 Export    →    🔐 Hash    →    📊 Analyze    →    🔍 Compare    →    🧹 Clean
│                                                                 │
│   Create temp       Generate        Compare hash      Generate        Remove
│   containers &      SHA256          lists to find     detailed        all temp
│   export to tar     hash lists      differences       diff reports    files
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 File Categories

| Category | Icon | Description |
|----------|:----:|-------------|
| **Common** | 🟢 | Identical files in both images (same path & hash) |
| **Modified** | 🟡 | Files in both images with different content |
| **Unique** | 🔵 | Files present in only one image |

---

## 🗂️ Cache Structure

```
cache/
│
├── 📦 image1.tar           # Exported filesystem
├── 📦 image2.tar           # Exported filesystem
│
├── 📋 image1_list.txt      # Hash and path list
├── 📋 image2_list.txt      # Hash and path list
│
├── 📂 image1/              # Extracted files for comparison
└── 📂 image2/              # Extracted files for comparison
```

---

<div align="center">

### 🌈 Color Palette

*Inspired by [Catppuccin Macchiato](https://github.com/catppuccin/catppuccin)*

| | Rosewater | Flamingo | Pink | Mauve | Red | Maroon | Peach | Yellow |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| | `#f4dbd6` | `#f0c6c6` | `#f5bde6` | `#c6a0f6` | `#ed8796` | `#ee99a0` | `#f5a97f` | `#eed49f` |

| | Green | Teal | Sky | Sapphire | Blue | Lavender | Text | Base |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| | `#a6da95` | `#8bd5ca` | `#91d7e3` | `#7dc4e4` | `#8aadf4` | `#b7bdf8` | `#cad3f5` | `#24273a` |

---

Made with 💜 and lots of ☕

</div>