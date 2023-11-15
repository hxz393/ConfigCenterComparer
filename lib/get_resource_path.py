"""
这个Python文件包含一个名为 `get_resource_path` 的函数，它用于获取资源的绝对路径。此函数特别适用于用PyInstaller打包后的可执行文件。在给定资源的相对路径后，此函数将返回其绝对路径。

使用示例：

```python
resource_path = get_resource_path("resources/my_file.txt")
if resource_path:
    print(resource_path)
```

如果输入的相对路径不是字符串或`os.PathLike`对象，函数将记录错误信息并返回 None。另外，如果在尝试获取资源路径时发生任何错误，函数也会记录错误信息并返回 None。

函数还包含一段关于如何用PyInstaller打包和运行的注释。为了测试该函数，可以使用以下命令打包：

```bash
pyinstaller -F my_module/file_ops/get_resource_path.py
```

然后，运行打包后的可执行文件：

```bash
./dist/get_resource_path.exe
```

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393。保留所有权利。
"""
import logging
import os
import sys
from typing import Union, Optional

logger = logging.getLogger(__name__)


def get_resource_path(relative_path: Union[str, os.PathLike]) -> Optional[str]:
    """
    获取资源的绝对路径。这个函数适用于 PyInstaller 打包后的可执行文件。

    :type relative_path: Union[str, os.PathLike]
    :param relative_path: 相对路径，可以是字符串或 os.PathLike 对象。
    :rtype: Optional[str]
    :return: 资源的绝对路径，如果发生错误则返回 None。
    """

    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, os.path.normpath(relative_path))
    except Exception:
        logger.exception(f"An error occurred while retrieving resource path")
        return None
