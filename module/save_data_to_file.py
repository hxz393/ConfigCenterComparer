"""
这是一个用于数据保存的Python模块。

本模块提供了将数据以不同格式保存到文件的功能。主要包括保存为CSV和JSON格式。提供了一个通用的`save_data_to_file`函数，根据不同的文件类型参数，调用相应的保存方法。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional

from lib.write_dict_to_csv import write_dict_to_csv
from lib.write_dict_to_json import write_dict_to_json

logger = logging.getLogger(__name__)


def save_data_to_file(file_name: str, file_type: str, data: dict) -> Optional[bool]:
    """
    将数据保存到指定类型的文件中。

    根据提供的文件类型（CSV或JSON），此函数将数据保存到相应格式的文件中。支持的文件类型包括CSV和JSON。

    :param file_name: 文件名，包含完整的路径。
    :type file_name: str
    :param file_type: 文件类型，可以是 'csv' 或 'json'。
    :type file_type: str
    :param data: 要保存的数据，为字典格式。
    :type data: dict
    :return: 保存成功返回True，否则返回None。
    :rtype: Optional[bool]
    """
    try:
        if "csv" in file_type.lower():
            return write_dict_to_csv(file_name, list(data.values()))
        elif "json" in file_type.lower():
            return write_dict_to_json(file_name, data)
        else:
            logger.error(f"Unsupported file type: {file_type}")
            return None
    except Exception:
        logger.exception("Unexpected error while saving data")
        return None
