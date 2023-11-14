"""
这是一个Python文件，主要包含一个函数：`write_dict_to_csv`。

`write_dict_to_csv` 函数的主要目标是将字典列表数据写入到CSV格式的文件中。这个函数接受两个参数：`target_path` 和 `data`。`target_path` 参数是将要写入的CSV文件的路径，它可以是字符串或 `os.PathLike` 对象。`data` 参数是要写入的字典列表数据。

在函数体中，首先将 `target_path` 标准化，并确保其父目录存在。然后，函数尝试打开该路径，并使用 `csv.DictWriter` 类将 `data` 写入到文件中。如果所有操作都成功，函数将返回 `True`。如果在过程中发生任何错误，函数将捕获异常，并使用 `logging` 模块记录错误信息，然后返回 `None`。

这个模块主要用于将数据以CSV格式写入到文件，是数据处理和存储的基础工具。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import csv
import logging
import os
import traceback
from typing import List, Dict, Union, Optional

logger = logging.getLogger(__name__)


def write_dict_to_csv(target_path: Union[str, os.PathLike], data: List[Dict[str, Union[str, int, float]]]) -> Optional[bool]:
    """
    将字典列表写入 CSV 文件。

    :param target_path: 目标 CSV 文件的路径。
    :type target_path: Union[str, os.PathLike]
    :param data: 要写入的数据，一个字典的列表。
    :type data: List[Dict[str, Union[str, int, float]]]
    :rtype: Optional[bool]
    :return: 操作成功则返回 True，否则返回 None。
    """
    try:
        target_path = os.path.normpath(target_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys() if data else [])
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        return True

    except Exception:
        logger.exception(f"An error occurred while writing to the CSV file at '{target_path}'")
        return None
