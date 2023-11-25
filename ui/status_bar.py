"""
此模块提供了一个状态栏类，用于在用户界面中展示状态信息。

主要包含 `StatusBar` 类，负责创建和管理状态栏。此类通过 `LangManager` 接收语言更新，并相应地更新状态栏的显示信息。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from PyQt5.QtWidgets import QStatusBar, QLabel
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class StatusBar(QStatusBar):
    """
    状态栏类，用于在用户界面显示状态信息。

    :param lang_manager: 语言管理器，用于处理语言更新。
    :type lang_manager: LangManager
    """

    def __init__(self, lang_manager: LangManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面。

        :rtype: None
        :return: 无返回值。
        """
        self.label = QLabel()
        self.addPermanentWidget(self.label)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.show_message(self.lang['main_1'])

    def show_message(self, message: str) -> None:
        """
        在状态栏显示指定的消息。

        :param message: 要在状态栏显示的消息。
        :type message: str
        :rtype: None
        :return: 无返回值。
        """
        try:
            if not isinstance(message, str):
                logger.warning("Message must be a string.")
                return
            self.label.setText(message)
        except Exception:
            logger.exception("Error while displaying message on status bar.")
