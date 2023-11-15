"""
这是一个Python文件，包含了一个名为`read_file_to_list`的函数。此函数从指定的文本文件中读取内容，并将其内容按行分割成列表。函数返回读取到的文本内容列表，如果遇到错误，则返回None。

函数接受一个名为`target_path`的参数，该参数是你想要读取的文本文件的路径，可以是字符串或`os.PathLike`对象。在读取文件之前，函数会检查该路径是否存在，以及该路径是否指向一个有效的文件。

在读取文件内容时，函数会尝试以"UTF-8"编码打开和读取文件。读取的内容将被分割成行，并存储在一个列表中，这个列表最后会被返回。函数在读取文件时可能会遇到一些错误，如无法访问文件，文件编码不是"UTF-8"，或者在读取文件时遇到其他问题。在遇到这些错误时，函数会记录相应的错误信息，并返回None。

这个函数主要可以用于处理需要按行读取并处理的文本文件，比如配置文件、数据文件等。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393。保留所有权利。
"""
import logging
import os
from typing import List, Union, Optional

logger = logging.getLogger(__name__)


def read_file_to_list(target_path: Union[str, os.PathLike]) -> Optional[List[str]]:
    """
    读取文本文件中的内容，并将其存储成列表。

    :param target_path: 文本文件的路径，可以是字符串或 os.PathLike 对象。
    :type target_path: Union[str, os.PathLike]
    :return: 成功时返回文本内容列表，如果遇到错误则返回None。
    :rtype: Optional[List[str]]
    """
    try:
        with open(target_path, 'r', encoding="utf-8") as file:
            return [line.strip() for line in file]
    except Exception:
        logger.exception(f"An error occurred while reading the file '{target_path}'")
        return None
