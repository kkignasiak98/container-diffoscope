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

## 🐳 Option 2: Local with Dev Containers

Run the containerized development environment on your local machine using any IDE that supports Dev Containers.

### Option A: IDE with Native Dev Container Support

Use any IDE with built-in Dev Container support:

| IDE | Dev Containers Extension |
|-----|-------------------------|
| **VS Code** |[Dev Containers extension |
| **JetBrains IDEs** | Built-in support in Gateway |
| **Cursor** | Dev Containers extension |

Simply open the cloned repository and your IDE will prompt to reopen in the container.

### Option B: DevPod for Any IDE

Use [DevPod](https://devpod.sh) to run Dev Containers with any IDE or editor:

### Option C: Build Docker Image Directly

You can also build and use the Docker image directly:

```bash
docker build -t container-diffoscope-dev .

# Run interactively
docker run -it -v $(pwd):/workspace container-diffoscope-dev
```

If you prefer to use podman run:

```bash
podman build--format docker --network=host -t container-diffoscope-dev .
```


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
uv sync
```

#### 5️⃣ Verify installation

```bash
python --version  # Should show Python 3.12.x
uv run python -m container_diffoscope --help
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
