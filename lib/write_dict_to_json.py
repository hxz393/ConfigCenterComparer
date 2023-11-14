"""
这是一个Python文件，其中包含一个函数：`write_dict_to_json`。

`write_dict_to_json` 函数的主要目标是将字典数据写入到JSON格式的文件中。这个函数接受两个参数：`target_path` 和 `data`。 `target_path` 参数是将要写入的JSON文件的路径，它可以是字符串或 `pathlib.Path` 对象。 `data` 参数是要写入的字典数据。

在函数体中，首先将 `target_path` 转换为 `Path` 对象，并确保其父目录存在。然后，函数试图打开该路径，并使用 `json.dump` 函数将 `data` 写入到文件中。如果所有操作都成功，函数将返回 `True`。如果在过程中发生任何错误，函数将捕获异常，并使用 `logging` 模块记录错误信息，然后返回 `None`。

这个模块主要用于将数据以JSON格式写入到文件，是数据处理和存储的基础工具。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""
import json
import logging
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)


def write_dict_to_json(target_path: Union[str, Path], data: Dict[Any, Any]) -> Optional[bool]:
    """
    将字典数据写入到 JSON 格式文件。

    :param target_path: Json文件的路径，可以是字符串或 pathlib.Path 对象。
    :type target_path: Union[str, Path]
    :param data: 要写入的字典数据。
    :type data: Dict[Any, Any]
    :return: 成功时返回True，失败时返回None。
    :rtype: Optional[bool]
    """
    try:
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open('w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception:
        logger.exception(f"An error occurred while writing to the JSON file at '{target_path}'")
        return None
