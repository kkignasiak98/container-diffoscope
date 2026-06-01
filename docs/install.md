<div align="center">

# 📦 Installation Guide

### *Three ways to install Container Diffoscope*

</div>

---

## 🎯 Installation Options

| Method | Best For | Requirements |
|--------|----------|--------------|
| [🍺 Homebrew](#-homebrew-macos--linux) | macOS & Linux users | Homebrew |
| [❄️ Nix Flake](#️-nix-flake-recommended) | Reproducible installs | Nix with flakes |
| [📦 Classic Nix](#-classic-nix-package) | Traditional Nix users | Nix |

---

## 🍺 Homebrew (macOS & Linux)

Install Container Diffoscope using Homebrew from the `repro-tools` tap:

```bash
# Add the tap
brew tap kkignasiak98/repro-tools

# Install container-diffoscope
brew install container-diffoscope
```

Or install directly in one command:

```bash
brew install kkignasiak98/repro-tools/container-diffoscope
```

### Updating

```bash
brew update
brew upgrade container-diffoscope
```

> 📦 **Tap Repository:** [github.com/kkignasiak98/homebrew-repro-tools](https://github.com/kkignasiak98/homebrew-repro-tools)

---

## ❄️ Nix Flake (Recommended)

For users with Nix flakes enabled, this is the recommended installation method as it provides reproducible builds with locked dependencies.

### Run directly without installing

```bash
nix run github:kkignasiak98/container-diffoscope
```

### Install to your profile

```bash
nix profile install github:kkignasiak98/container-diffoscope
```

### Use in another flake

Add to your `flake.nix` inputs:

```nix
{
  inputs = {
    container-diffoscope.url = "github:kkignasiak98/container-diffoscope";
  };
  
  outputs = { self, nixpkgs, container-diffoscope, ... }: {
    # Use container-diffoscope.packages.${system}.default
  };
}
```

### Development shell

```bash
# Clone the repository
git clone https://github.com/kkignasiak98/container-diffoscope.git
cd container-diffoscope

# Enter development environment
nix develop
```

---

## 📦 Classic Nix Package

For traditional Nix users who prefer the classic approach without flakes.

### Using nix-build

```bash
# Clone the repository
git clone https://github.com/kkignasiak98/container-diffoscope.git
cd container-diffoscope

# Build the package
nix-build default.nix

# Run the built package
./result/bin/container-diffoscope --help
```

### Using nix-shell for development

```bash
nix-shell -p "import ./default.nix {}"
```

### Adding to your configuration

You can add Container Diffoscope to your NixOS or home-manager configuration by importing `default.nix`:

```nix
{ pkgs, ... }:

let
  container-diffoscope = pkgs.callPackage /path/to/container-diffoscope/default.nix {};
in
{
  environment.systemPackages = [ container-diffoscope ];
}
```

---

## ✅ Verify Installation

After installing, verify the installation:

```bash
container-diffoscope --help
```

You should see the help output with available commands and options.

---

## 📋 Requirements

Regardless of installation method, you'll need:

| Requirement | Purpose |
|-------------|---------|
| **Docker** | Required for comparing container images |

---

<div align="center">

*Need help? [Open an issue](https://github.com/kkignasiak98/container-diffoscope/issues)*

</div>
