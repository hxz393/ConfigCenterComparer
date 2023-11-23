"""
该模块主要负责处理与一致性状态更新相关的功能。包括更新各配置项的一致性状态，以及确定特定配置项的一致性。

本模块的核心功能是 `update_consistency_status` 函数，用于根据数据库查询结果和特定规则来更新配置项的一致性状态。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict

from module.determine_consistency_status import determine_consistency_status

logger = logging.getLogger(__name__)


def update_consistency_status(formatted_results: Dict[str, Dict[str, str]],
                              query_statuses: Dict[str, bool]) -> None:
    """
    根据数据库查询结果和一致性规则来更新配置项的一致性状态。

    此函数处理通过数据库查询得到的各配置项结果，并利用 determine_consistency_status 函数来确定每个配置项的一致性状态，最后更新这些状态。

    :param formatted_results: 格式化后的配置项结果，键为配置项名称，值为各环境的配置状态。
    :type formatted_results: Dict[str, Dict[str, str]]
    :param query_statuses: 各环境的查询状态，键为环境名称，值为布尔值，表示该环境的查询是否成功。
    :type query_statuses: Dict[str, bool]
    :return: 无返回值。
    :rtype: None

    :example:
    >>> results = {"config1": {"env1": "value1", "env2": "value1"}, "config2": {"env1": "value3", "env3": "value4"}}
    >>> statuses = {"env1": True, "env2": True, "env3": False}
    >>> update_consistency_status(results, statuses)
    >>> results["config1"]
    {'env1': 'value1', 'env2': 'value1', 'consistency_status': 'fully'}
    >>> results["config2"]
    {'env1': 'value3', 'env3': 'value4', 'consistency_status': 'unknown'}
    """
    try:
        # 将数据库查询成功的环境名加入列表
        valid_keys = [key for key, value in query_statuses.items() if value]

        for config in formatted_results.values():
            # 提取配置值，排除None
            values = [config[env] for env in valid_keys if env in config and config[env] is not None]

            # 检测并更新状态
            config['consistency_status'] = determine_consistency_status(values, config, valid_keys)
    except Exception:
        logger.exception("An error occurred while updating consistency status.")
