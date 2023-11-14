"""
这是一个Python文件，其中包含一个函数：`write_list_to_file`。

`write_list_to_file` 函数的主要目标是将列表或元祖的元素写入文件，每个元素占据文件的一行。该函数接受两个参数：`target_path` 和 `content`。 `target_path` 参数是将要写入的文本文件的路径，可以是字符串或 `pathlib.Path` 对象。 `content` 参数是要写入的列表。

在函数体中，首先将 `target_path` 转换为 `Path` 对象，并确保其父目录存在。然后，函数试图打开该路径，并将 `content` 的每个元素转换为字符串，并以换行符连接这些字符串，然后写入到文件中。如果所有操作都成功，函数将返回 `True`。如果在过程中发生任何错误，函数将捕获异常，并使用 `logging` 模块记录错误信息，然后返回 `None`。

这个模块主要用于将数据以文本格式写入到文件，是数据处理和存储的基础工具。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""
import logging
import traceback
from pathlib import Path
from typing import List, Any, Optional, Union, Set

logger = logging.getLogger(__name__)


def write_list_to_file(target_path: Union[str, Path], content: Union[List[Any], Set[Any]]) -> Optional[bool]:
    """
    将列表的元素写入文件，每个元素占据文件的一行。

    :param target_path: 文本文件的路径，可以是字符串或 pathlib.Path 对象。
    :type target_path: Union[str, Path]
    :param content: 要写入的列表或元祖。
    :type content: Union[List[Any], Set[Any]]
    :return: 成功时返回True，失败时返回None。
    :rtype: Optional[bool]
    """
    try:
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open('w', encoding="utf-8") as file:
            file.write("\n".join(str(element) for element in content))
        return True
    except Exception as e:
        logger.exception(f"An error occurred while writing to the file at '{target_path}': {e}")
        return None
