"""
此模块包含语言管理相关功能，用于处理多语言环境下的语言字典的获取和更新。

本模块主要包含 `LangManager` 类，该类负责语言的获取和更新。通过使用 PyQt5 的信号和槽机制，可以在语言更新时及时通知UI组件。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import copy
import logging
from typing import Dict, Optional

from PyQt5.QtCore import QObject, pyqtSignal

from config.lang_dict_all import LANG_DICTS
from module.get_lang_dict import get_lang_dict

logger = logging.getLogger(__name__)


class LangManager(QObject):
    """
    语言管理类，用于管理和更新应用程序的语言字典。

    此类继承自 QObject，可发出语言更新的信号。它通过 `get_lang_dict` 函数获取当前语言字典，并提供了更新语言的功能。

    :ivar _lang_dict: 当前使用的语言字典。
    :vartype _lang_dict: dict
    """
    lang_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._lang_dict = get_lang_dict()

    def get_lang(self) -> Optional[Dict[str, str]]:
        """
        获取当前使用的语言字典的副本。

        :return: 当前语言字典的深拷贝。
        :rtype: Optional[Dict[str, str]]
        """
        try:
            return copy.deepcopy(self._lang_dict)
        except Exception:
            logger.exception("Failed to retrieve language dictionary.")
            return None

    def update_lang(self, new_lang: str) -> None:
        """
        更新当前使用的语言字典。

        :param new_lang: 新语言的标识符。
        :type new_lang: str

        :rtype: None
        :return: 无返回值。
        """
        try:
            self._lang_dict = LANG_DICTS.get(new_lang, "English")
            self.lang_updated.emit()
            logger.info(f"Language changed to {new_lang}")
        except Exception:
            logger.exception(f"Failed to changed language to {new_lang}")
