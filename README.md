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
   # 如果没有pipx请先安装
   pipx install <Release package>
   ```

下载地址：[发布地址](https://github.com/tokyo2006/k8st/releases)

### 基本使用

> 如果你不设置`--namespace/-n`参数的时候默认namespace是`default`

#### ctx

`ctx` - Kubernetes上下文切换

**用法**:  
`ctx`

```shell
k8st ctx
```

---

#### debug

![debug](https://res.cloudinary.com/xinta/image/upload/v1740646891/k8st/debug.gif)

`debug` - 通过工具容器进入指定Pod的指定容器bash环境

**用法**:  
`debug [-i IMAGE]`

**参数**:

| 参数 | 短名 | 描述                   | 默认值                     | 必要 |
|-----------|-------|-------------------------------|-----------------------------|----------|
| `--image`   | `-i`  | Image to use for debug container | tokyo2006/dev-tools:latest | No       |

```bash
k8st -n argocd debug
```

---

#### exec

![exec](https://res.cloudinary.com/xinta/image/upload/v1740647240/k8st/exec.gif)

`exec` - bash into a pod's container

**用法**:  
`exec`

```bash
k8st -n argocd exec
```

---

#### copy

![copy](https://res.cloudinary.com/xinta/image/upload/v1740648566/k8st/copy.gif)

`copy` - Copy files from pod

**用法**:  
`copy -l LOCAL_PATH -r REMOTE_PATH`

**参数**:

| 参数 | 短名 | 描述                     | 必要 |
|-----------|-------|---------------------------------|----------|
| `--local`   | `-l`  | 存储到本地的文件路径           | Yes      |
| `--remote`  | `-r`  | 容器中的文件路径        | Yes      |

```bash
k8st -n argocd copy -l <LOCAL FILE>  -r <REMOTE FILE>
```

---

#### secret

![secret](https://res.cloudinary.com/xinta/image/upload/v1740647908/k8st/secret.gif)

`secret` - 从secret中获取秘钥明文（仅限于明文秘钥）

**用法**:  
`secret`

```bash
k8st -n argocd secret
```

---

更多命令可以通过help命令查看:

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

运行测试（可选）:

```shell
poetry run pytest
```

运行测试和生成覆盖率报告（可选）:

```shell
poetry run pytest --cov=k8st --cov-report=html
```

运行工具：

```shell
poetry run k8st --debug help
```
