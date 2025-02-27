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
   # please install pipx first if you don't have it
   pipx install <Release package>
   ```

Download address: [Releases](https://github.com/tokyo2006/k8st/releases)

### Basic Usage

> The namespace default values is `default` if you do not use `--namespace/-n` parameter

#### ctx

`ctx` - Kubernetes Context Switching

**Usage**:  
`ctx`

```shell
k8st ctx
```

---

#### debug

`debug` - bash into a pod through debug container

**Usage**:  
`debug [-i IMAGE]`

**Arguments**:

| Parameter | Short | Description                   | Default                     | Required |
|-----------|-------|-------------------------------|-----------------------------|----------|
| `image`   | `-i`  | Image to use for debug container | tokyo2006/dev-tools:latest | No       |

```bash
k8st -n argocd debug
```

---

#### exec

`exec` - bash into a pod's container

**Usage**:  
`exec`

```bash
k8st -n argocd debug
```

---

#### copy

`copy` - Copy files from pod

**Usage**:  
`copy -l LOCAL_PATH -r REMOTE_PATH`

**Arguments**:

| Parameter | Short | Description                     | Required |
|-----------|-------|---------------------------------|----------|
| `local`   | `-l`  | Local path to copy to           | Yes      |
| `remote`  | `-r`  | Remote path to copy from        | Yes      |

```bash
k8st --debug -n argocd copy -l <LOCAL FILE>  -r <REMOTE FILE>
```

---

#### secret

`secret` - Get secret values from a secret

**Usage**:  
`secret`

```bash
k8st -n argocd secret
```

---

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

Running tests:

```shell
poetry run pytest
```

Running tests and coverage:

```shell
poetry run pytest --cov=k8st --cov-report=html
```

Run the tool:

```shell
poetry run k8st --debug help
```
