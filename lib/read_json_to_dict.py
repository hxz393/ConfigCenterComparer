"""
这是一个Python文件，包含一个名为`read_json_to_dict`的函数。此函数从指定的JSON文件中读取内容，并将其转换为字典。函数返回读取和转换后的字典，如果遇到错误，则返回None。

函数接受一个名为`target_path`的参数，该参数是你想要读取的JSON文件的路径，可以是字符串或`os.PathLike`对象。在读取文件之前，函数会检查该路径是否存在，以及该路径是否指向一个有效的文件。

在读取文件内容时，函数会尝试以"UTF-8"编码打开和读取文件，然后使用`json.load()`函数将文件内容转换为字典。函数在读取文件时可能会遇到一些错误，如无法访问文件，文件不是有效的JSON格式，或者在读取文件时遇到其他问题。在遇到这些错误时，函数会记录相应的错误信息，并返回None。

这个函数主要可以用于处理需要读取并转换为字典的JSON文件，例如配置文件、数据文件等。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393。保留所有权利。
"""
import json
import logging
import traceback
import os
from typing import Dict, Any, Union, Optional

logger = logging.getLogger(__name__)


def read_json_to_dict(target_path: Union[str, os.PathLike]) -> Optional[Dict[str, Any]]:
    """
    读取 JSON 文件内容，储存到字典。

    :param target_path: Json 文件的路径，可以是字符串或 os.PathLike 对象。
    :type target_path: Union[str, os.PathLike]
    :return: 成功时返回内容字典，如果遇到错误则返回None。
    :rtype: Optional[Dict[str, Any]]
    """
    if not os.path.exists(target_path):
        logger.error(f"The file '{target_path}' does not exist.")
        return None
    if not os.path.isfile(target_path):
        logger.error(f"'{target_path}' is not a valid file.")
        return None

    try:
        with open(target_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        logger.exception(f"An error occurred while reading the JSON file '{target_path}'")
        return None
