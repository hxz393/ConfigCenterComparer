"""
这个模块提供了数据保存功能，允许用户将数据以CSV或JSON格式保存到文件中。

主要功能是 `save_data_to_file` 函数，它接受文件名、文件类型和要保存的数据，根据文件类型将数据保存为CSV或JSON格式。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
import tempfile
from typing import Optional, Dict

from lib.write_dict_to_csv import write_dict_to_csv
from lib.write_dict_to_json import write_dict_to_json

logger = logging.getLogger(__name__)


def save_data_to_file(file_name: str, file_type: str, data: Dict[int, Dict[str, str]]) -> Optional[bool]:
    """
    将字典格式的数据保存到CSV或JSON文件中。

    该函数根据指定的文件名、文件类型和数据字典，将数据保存到对应格式的文件中。支持的文件类型包括CSV和JSON。当保存成功时返回True，如果遇到错误则返回False，异常情况下返回None。

    :param file_name: 文件名，包含路径。
    :type file_name: str
    :param file_type: 文件类型，'csv' 或 'json'。
    :type file_type: str
    :param data: 要保存的数据，字典格式。
    :type data: Dict[int, Dict[str, str]]
    :return: 成功保存返回True，失败返回False，异常返回None。
    :rtype: Optional[bool]

    :example:
    >>> data_dict = {1: {'name': 'Alice', 'age': '30'}, 2: {'name': 'Bob', 'age': '25'}}
    >>> with tempfile.TemporaryDirectory() as temp_dir:
    ...     temp_csv_file = os.path.join(temp_dir, 'data_dict.csv')
    ...     save_data_to_file(temp_csv_file, 'csv', data_dict)
    ...     temp_json_file = os.path.join(temp_dir, 'data_dict.json')
    ...     save_data_to_file(temp_json_file, 'json', data_dict)
    True
    True
    """
    try:
        if "csv" in file_type.lower():
            return write_dict_to_csv(file_name, list(data.values()))
        elif "json" in file_type.lower():
            return write_dict_to_json(file_name, data)
        else:
            logger.error(f"Unsupported file type: {file_type}")
            return False
    except Exception:
        logger.exception("Unexpected error while saving data")
        return None
