<div align="center">

# 🐋 Container Diffoscope

<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/palette/macchiato.png" width="600"/>

### Elegant Container filesystem comparison ☕

[![Alpha](https://img.shields.io/badge/Status-Alpha-ed8796?style=for-the-badge)](https://github.com/kkignasiak98/container-diffoscope)
[![Python](https://img.shields.io/badge/Python-3.12-a6da95?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Required-8aadf4?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Nix](https://img.shields.io/badge/Nix-Devbox-7dc4e4?style=for-the-badge&logo=nixos&logoColor=white)](https://www.jetify.com/devbox)

</div>

---

## ⚠️ Alpha Notice

> **This project is currently in alpha stage.**
> 
> APIs may change, features may be incomplete, and there are no guarantees of stability.
> Use at your own risk in production environments.

---

## 🌸 What is Container Diffoscope?

**Container Diffoscope** is a powerful tool that compares the filesystems of two Docker images at the file level. It helps you understand exactly what changed between image versions by:

- 🔍 **Detecting** identical, modified, and unique files
- 🔐 **Using** SHA256 hashes for accurate comparison
- 📝 **Generating** beautiful markdown diff reports

Perfect for auditing image changes, debugging build differences, or understanding what an update actually modifies.

📖 **[Full Documentation →](docs/docs.md)**

---

## 🚀 Quick Start

```bash
# Compare two Docker images
python -m container_diffoscope ubuntu:20.04 ubuntu:22.04

# With custom output directory
python -m container_diffoscope image1:tag image2:tag --output-dir results
```

---

## 🛠️ Development Environment

This project uses a modern, reproducible development setup:

<table>
<tr>
<td align="center" width="25%">

**🐳 Docker**

Container runtime

</td>
<td align="center" width="25%">

**📦 Devcontainers**

Devcontainers integration

</td>
<td align="center" width="25%">

**❄️ Nix**

Reproducible builds

</td>
<td align="center" width="25%">

**📋 Devbox**

Nix made easy

</td>
</tr>
</table>

> The development environment is fully containerized and reproducible. No "works on my machine" problems!

🔧 **[Setup Instructions →](docs/Setup.md)**

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [docs/docs.md](docs/docs.md) | Full documentation with features, usage, and internals |
| [docs/Setup.md](docs/Setup.md) | Development environment setup guide |
| [docs/install.md](docs/install.md) | Installation guide (Homebrew, Nix Flake, Classic Nix) |
| [tests/README.md](tests/README.md) | Testing documentation |

---

<div align="center">

*Styled with [Catppuccin](https://github.com/catppuccin/catppuccin) 🌈*

</div>

