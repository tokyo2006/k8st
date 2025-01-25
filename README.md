# k8st

[中文](README.md)
[English](README_EN.md)

k8st 是一个简化 Kubernetes 服务操作的命令行工具。

## 快速开始

### 安装

您可以通过以下两种方式之一安装 k8st：

1. 从源码构建（参见[构建指南](#如何构建)）
2. 直接安装发布包：

   ```shell
   pip install <Release package>
   ```

   下载地址：[最新版本](https://github.com/tokyo2006/k8st/releases/tag/latest)

### 基本使用

#### Kubernetes 上下文切换

```shell
k8st ctx
```

更多命令说明请使用帮助命令：

```shell
k8st --help
```

## 如何构建

### 环境要求

1. Python >= 3.12

   推荐使用 pyenv 安装 Python：

   ```shell
   brew update
   brew install pyenv
   ```

   配置 Zsh：

   ```shell
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   ```

   安装 Python 3.12.4：

   ```shell
   cd k8st
   pyenv install 3.12.4
   ```

2. Poetry 包管理工具

   首先安装 pipx：

   ```shell
   brew install pipx
   pipx ensurepath
   ```

   可选：允许在全局范围内使用 pipx

   ```shell
   sudo pipx ensurepath --global
   ```

   然后安装 Poetry：

   ```shell
   pipx install poetry
   ```

### 构建与运行

构建项目：

```shell
poetry build
```

运行工具：

```shell
poetry run k8st --debug help
```
