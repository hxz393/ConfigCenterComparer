"""
本模块提供用于处理配置跳过状态的功能。

主要功能是 `update_skip_status` 函数，它根据指定的忽略列表更新给定结果的跳过状态。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import Dict

from config.settings import CONFIG_SKIP_PATH
from lib.read_file_to_list import read_file_to_list

logger = logging.getLogger(__name__)


def update_skip_status(formatted_results: Dict[str, Dict[str, str]]) -> None:
    """
    根据忽略列表更新 formatted_results 中各个配置项的跳过状态。

    此函数接收一个字典，其中包含配置项及其相关属性。它读取预定义的忽略列表，并根据此列表更新配置项的跳过状态。

    :param formatted_results: 包含配置项及其属性的字典。
    :type formatted_results: Dict[str, Dict[str, str]]
    :return: 无返回值。
    :rtype: None

    :example:
    >>> os.chdir(os.path.dirname(os.getcwd()))
    >>> results = {"config1": {"name": "configA", "value": "123"},
    ...            "ere3-netty-customer+application+spring.redis.pool.min-idle": {"name": "configB", "value": "456"}}
    >>> update_skip_status(results)
    >>> results["config1"]
    {'name': 'configA', 'value': '123', 'skip_status': 'no'}
    >>> results["ere3-netty-customer+application+spring.redis.pool.min-idle"]["skip_status"]
    'yes'
    """
    try:
        # 读取忽略列表，转换为集合，用于快速检索
        skip_set = set(read_file_to_list(CONFIG_SKIP_PATH) or [])

        # 遍历 formatted_results，更新每个条目的跳过状态
        for index_key, config in formatted_results.items():
            config['skip_status'] = 'yes' if index_key in skip_set else 'no'
    except Exception:
        logger.exception("Error occurred in updating skip status")
