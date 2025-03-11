# autopip

一键安装当前目录及子目录的py包

## 功能介绍

`autopip.py` 是一个用于自动安装Python项目依赖的脚本。它可以自动扫描当前目录及子目录下的所有Python文件，提取其中的导入包名，并检查这些包是否已经安装。如果有未安装的包，脚本会自动使用指定的pip镜像源进行安装。

## 使用方法

1. 确保你已经安装了Python环境。
2. 将 `autopip.py` 文件放置在你的项目根目录下。
3. 打开命令行工具，进入项目根目录。
4. 运行以下命令：

```bash
python autopip.py
```

## 示例

假设你的项目目录结构如下：

```
project/
├── main.py
├── module1.py
└── autopip.py
```

`main.py` 文件内容如下：

```python
import requests
import pandas as pd

# 代码逻辑
```

`module1.py` 文件内容如下：

```python
import numpy as np

# 代码逻辑
```

运行 `python autopip.py` 后，脚本会自动检查 `requests`、`pandas` 和 `numpy` 是否已经安装，如果未安装，则会自动使用镜像源进行安装。

## 配置说明

- `PIP_MIRROR`：pip镜像源地址，默认使用阿里云镜像源。
- `INSTALL_DIRECTORY`：扫描目录，默认使用当前目录。

## 注意事项

- 请确保你的网络连接正常，以便能够正常访问pip镜像源。
- 如果遇到安装失败的情况，请检查网络连接或手动安装相应的包。
