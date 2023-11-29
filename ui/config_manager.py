"""
这个模块提供了配置管理功能，主要用于处理和更新应用程序的配置信息。

包含一个核心类 `ConfigManager`，负责读取、更新和管理配置。该类提供了获取主配置、连接配置和跳过列表的方法，并允许更新这些配置信息。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import copy
import logging
from typing import Dict, Optional, Union, List

from PyQt5.QtCore import QObject, pyqtSignal

from config.settings import CONFIG_SKIP_PATH, CONFIG_MAIN_PATH, CONFIG_APOLLO_PATH, CONFIG_NACOS_PATH
from lib.read_file_to_list import read_file_to_list
from lib.write_dict_to_json import write_dict_to_json
from lib.write_list_to_file import write_list_to_file
from module.read_config_all import read_config_all

logger = logging.getLogger(__name__)


class ConfigManager(QObject):
    """
    配置管理器类，负责管理和更新应用程序的配置信息。

    该类包括获取和设置主配置、连接配置和跳过列表的方法，同时提供信号以通知配置更新。

    :ivar config_main_updated: 当主配置更新时发出的信号。
    :ivar config_connection_updated: 当连接配置更新时发出的信号。
    :ivar skip_list_updated: 当跳过列表更新时发出的信号。
    """
    config_main_updated = pyqtSignal()
    config_connection_updated = pyqtSignal()
    skip_list_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._config_main, self._config_apollo, self._config_nacos = read_config_all()
        self._skip_list = read_file_to_list(CONFIG_SKIP_PATH) or []

    def get_config_main(self) -> Optional[Dict[str, str]]:
        """
        获取主配置的副本。

        :return: 包含主配置的字典，如果出现错误则返回 None。
        :rtype: Optional[Dict[str, str]]
        """
        try:
            return copy.deepcopy(self._config_main)
        except Exception:
            logger.exception("Failed to get config_main.")
            return None

    def get_config_connection(self) -> Optional[Dict[str, Dict[str, Union[Dict[str, str], bool]]]]:
        """
        根据当前配置中心获取连接配置的副本。

        :return: 包含连接配置的字典，如果出现错误则返回 None。
        :rtype: Optional[Dict[str, Dict[str, Union[Dict[str, str], bool]]]]
        """
        try:
            if self._config_main['config_center'] == 'Apollo':
                return copy.deepcopy(self._config_apollo)
            else:
                return copy.deepcopy(self._config_nacos)
        except Exception:
            logger.exception("Failed to get config_connection.")
            return None

    def get_skip_list(self) -> Optional[List[str]]:
        """
        获取忽略列表的副本。

        :return: 包含跳过项的列表，如果出现错误则返回 None。
        :rtype: Optional[List[str]]
        """
        try:
            return copy.deepcopy(self._skip_list)
        except Exception:
            logger.exception("Failed to get skip_list.")
            return None

    def update_config_main(self, new_config: Dict[str, str]) -> None:
        """
        更新主配置。

        :param new_config: 新的主配置。
        :type new_config: Dict[str, str]
        """
        try:
            self._config_main = new_config
            self.config_main_updated.emit()
            write_dict_to_json(CONFIG_MAIN_PATH, new_config)
            logger.info("Config updated: config_main")
        except Exception:
            logger.exception("Failed to update config: config_main")

    def update_config_connection(self, new_config: Dict[str, Dict[str, Union[Dict[str, str], bool]]]) -> None:
        """
        更新连接配置。

        :param new_config: 新的连接配置。
        :type new_config: Dict[str, Dict[str, Union[Dict[str, str], bool]]]
        """
        try:
            if self._config_main['config_center'] == 'Apollo':
                self._config_apollo = new_config
                write_dict_to_json(CONFIG_APOLLO_PATH, new_config)
            else:
                self._config_nacos = new_config
                write_dict_to_json(CONFIG_NACOS_PATH, new_config)
            self.config_connection_updated.emit()
            logger.info("Config updated: config_connection")
        except Exception:
            logger.exception("Failed to update config: config_connection")

    def update_skip_list(self, new_config: List[str]) -> None:
        """
        更新忽略列表。

        :param new_config: 新忽略列表。
        :type new_config: List[str]
        """
        try:
            self._skip_list = new_config
            # 写入到配置文件
            self.skip_list_updated.emit()
            write_list_to_file(CONFIG_SKIP_PATH, new_config)
            logger.info("Config updated: skip_list")
        except Exception:
            logger.exception("Failed to update config: skip_list")
