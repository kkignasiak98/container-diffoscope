<div align="center">

# 🔧 Setup Guide

### *Choose your adventure*

</div>

---

## 🎯 Setup Options

There are **three ways** to set up the development environment for Container Diffoscope:

| Option | Best For | Requirements |
|--------|----------|--------------|
| [☁️ Cloud IDE](#️-option-1-cloud-ide-easiest) | Quick start, no local setup | GitHub account |
| [🐳 Local + Containers](#-option-2-local-with-dev-containers-recommended) | Full local development | Docker, VS Code |
| [💻 Local Native](#-option-3-local-without-containers) | No Docker needed | Devbox or Nix |

---

## ☁️ Option 1: Cloud IDE (Easiest)

Simply open the repository in any online IDE that supports Dev Containers. **Zero local setup required!**

### Supported Platforms

| Platform | Link |
|----------|------|
| **GitHub Codespaces** | [github.com/features/codespaces](https://github.com/features/codespaces) |
| **Ona (previously Gitpod)** | [https://ona.com/](https://ona.com/) |
| **CodeSandbox** | [codesandbox.io](https://codesandbox.io) |

> ⏱️ First launch takes ~3-5 minutes while the container builds. Subsequent launches are instant.

---

## 🐳 Option 2: Local with Dev Containers (Recommended)

Run the containerized development environment on your local machine.

### Prerequisites

| Tool | Purpose | Installation |
|------|---------|--------------|
| **Docker Desktop** | Container runtime | [Get Docker](https://docs.docker.com/get-docker/) |
| **VS Code** | Editor | [Download](https://code.visualstudio.com/) |
| **Dev Containers Extension** | Container integration | [Install](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) |

### Setup Steps

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/kkignasiak98/container-diffoscope.git
cd container-diffoscope
```

#### 2️⃣ Open in VS Code

```bash
code .
```

#### 3️⃣ Reopen in Container

VS Code will detect the Dev Container configuration and show a prompt:

> 📦 **"Folder contains a Dev Container configuration file. Reopen folder to develop in a container?"**

Click **"Reopen in Container"**

Alternatively: `Ctrl+Shift+P` → `Dev Containers: Reopen in Container`

#### 4️⃣ Wait for build

```
🐳 Building container...
   ├── 📦 Installing Nix
   ├── 📋 Setting up Devbox
   ├── 🐍 Installing Python 3.12
   ├── 📚 Installing Poetry
   └── ✅ Ready!
```

> ⏱️ First build takes ~5-10 minutes. Rebuilds are cached and much faster.

### What You Get

The container includes everything pre-configured:

- ❄️ **Nix** - Reproducible package manager
- 📋 **Devbox** - Nix made simple
- 🐍 **Python 3.12** + Poetry
- 🐳 **Docker CLI** (Docker-in-Docker)
- 🔧 **Dev tools**: hadolint, ruff, pyright
- 📝 **VS Code extensions** pre-installed

---

## 💻 Option 3: Local Without Containers

Run directly on your machine without Docker. Good for systems where Docker isn't available.

### Prerequisites

| Tool | Purpose |
|------|---------|
| **Nix + Devbox** | Package management (installed via script) |
| **Docker** | Required for running the tool (comparing images) |

### Setup Steps

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/kkignasiak98/container-diffoscope.git
cd container-diffoscope
```

#### 2️⃣ Run the install script

Simply run the provided install script to set up the correct versions of Nix and Devbox:

```bash
./install.sh
```

This script will automatically install:
- ❄️ **Nix** (Determinate Systems Installer v3.2.1)
- 📋 **Devbox** (v0.14.2)

> 💡 After installation, you may need to restart your shell or run:
> ```bash
> . /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
> ```

#### 3️⃣ Start Devbox shell

```bash
devbox shell
```

This will:
- Download and install all required packages via Nix
- Set up the correct Python version
- Configure the shell environment

#### 4️⃣ Install Python dependencies

```bash
poetry install
```

#### 5️⃣ Verify installation

```bash
python --version  # Should show Python 3.12.x
poetry run python -m container_diffoscope --help
```

## 🎯 Available Scripts

Once your environment is set up, use these Devbox scripts:

```bash
# 📦 Sync all dependencies
devbox run sync_dependencies

# 🧪 Run unit tests
devbox run unit_tests

# 🧪 Run meta tests
devbox run meta_tests

# 🎨 Format Python code
devbox run format_python

# 🔍 Lint Python code
devbox run lint_python

# 📊 Type check with Pyright
devbox run type_check_python

# 📦 Build the package
devbox run build_package
```

---

<div align="center">

*Need help? [Open an issue](https://github.com/kkignasiak98/container-diffoscope/issues)*


</div>
