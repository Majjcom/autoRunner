# autoRunner

一个简单的自动化工具。

## 介绍

该工具通过`opencv`、`aircv`库识别目标元素在屏幕上的位置，并利用`pyautogui`库进行鼠标操作，从而实现代替人类手动操作的需要。

## 简单使用

#### 使用二进制文件 (exe)

- 下载`Release`中最新版本二进制文件
- 编写`config.json`配置文件
  - 可以参考 `配置文件格式.md` 的实例json文件，配置文件内指令基本符合自然语义
- 截图提取目标特征，保存到固定位置，并在配置文件中指定文件位置
- 运行二进制文件

备注：二进制文件通过`pyinstaller`生成。

#### 使用Python脚本

### 环境准备方式

## 使用`uv`

在项目目录下输入以下命令即可：

```shell
$ uv run main.py
```

## 传统方式

- 首先，准备Python环境，基础环境Python版本应大于`3.8`
- 安装以下依赖：
  - `Pillow`
  - `opencv-python`
  - `aircv`
  - `pyautogui`


```shell
$ python --version
$ python -m pip install -U pip
$ pip install -r requirments.txt
```

### 配置文件

- 编写`config.json`配置文件
  - 可以参考 `配置文件格式.md` 的实例json文件，配置文件内指令基本符合自然语义

- 截图提取目标特征，保存到固定位置，并在配置文件中指定文件位置
- 运行Python脚本

```shell
$ python main.py
```

## 最后

本应用以`mit`许可证开源。
