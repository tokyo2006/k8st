# k8st

[Chinese](README.md)
[English](README_EN.md)

k8st is a command-line tool designed to simplify Kubernetes service operations.

## Quick Start

### Installation

You can install k8st in one of two ways:

1. Build from source (see [Build Guide](#how-to-build))
2. Install from release package:

   ```shell
   pip install <Release package>
   ```

   Download from: [Latest Release](https://github.com/tokyo2006/k8st/releases/tag/latest)

### Basic Usage

#### Kubernetes Context Switching

```shell
k8st ctx
```

For more command details, use the help command:

```shell
k8st --help
```

## How to Build

### Prerequisites

1. Python >= 3.12

   Recommended installation using pyenv:

   ```shell
   brew update
   brew install pyenv
   ```

   Configure Zsh:

   ```shell
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   ```

   Install Python 3.12.4:

   ```shell
   cd k8st
   pyenv install 3.12.4
   ```

2. Poetry Package Manager

   First, install pipx:

   ```shell
   brew install pipx
   pipx ensurepath
   ```

   Optional: Enable pipx in global scope

   ```shell
   sudo pipx ensurepath --global
   ```

   Then install Poetry:

   ```shell
   pipx install poetry
   ```

### Build and Run

Build the project:

```shell
poetry build
```

Run the tool:

```shell
poetry run k8st --debug help
```
