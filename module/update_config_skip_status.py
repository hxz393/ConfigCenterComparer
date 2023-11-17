"""
这是一个用于处理配置文件过滤状态的Python模块。

此模块包含一个主要函数：`update_config_skip_status`，用于更新配置文件的过滤状态。该函数读取预设的过滤列表，根据列表内容决定哪些配置项应被标记为跳过状态。

主要目的是为了自动识别和标记那些在某些情况下需要被忽略的配置项，从而提高配置管理的效率和准确性。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict

from config.settings import CONFIG_SKIP_PATH
from lib.read_file_to_list import read_file_to_list

logger = logging.getLogger(__name__)


def update_config_skip_status(results: Dict[str, Dict[str, str]]) -> None:
    """
    更新配置项的过滤状态。

    此函数通过读取预设的过滤列表，检查传入的配置结果字典中的每个配置项。若配置项在过滤列表中，则标记为跳过状态。

    :param results: 包含配置项的字典，每个配置项包含一个内部字典。
    :type results: Dict[str, Dict[str, str]]
    """
    try:
        # 读取过滤列表
        skip_list = read_file_to_list(CONFIG_SKIP_PATH) or []

        # 更新结果字典
        for index_key in results:
            results[index_key]['skip_status'] = 'yes' if index_key in skip_list else 'no'
    except Exception:
        logger.exception("Error occurred while applying skip status to results")
