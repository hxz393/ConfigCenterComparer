"""
本模块提供了应用程序中与数据库连接设置相关的用户界面操作功能。

该模块定义了 `ActionSettingConnection` 类，用于处理与数据库连接设置相关的UI交互和功能。该类主要负责初始化用户界面组件、更新界面语言设置以及打开数据库连接设置对话框。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from ui.dialog_settings_connection import DialogSettingsConnection
from ui.lang_manager import LangManager
from ui.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class ActionSettingConnection(QObject):
    """
    数据库连接设置操作类，用于处理数据库连接设置相关的UI交互和功能。

    :param lang_manager: 语言管理器，用于设置和更新界面语言。
    :type lang_manager: LangManager
    """
    status_updated = pyqtSignal(str)

    def __init__(self, lang_manager: LangManager, config_manager: ConfigManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        self.action_setting = QAction(QIcon(get_resource_path('media/icons8-database-administrator-26.png')), 'Database Configuration')
        self.action_setting.setShortcut('F12')
        self.action_setting.triggered.connect(self.open_dialog)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_setting.setText(self.lang['ui.action_setting_connection_1'])
        self.action_setting.setStatusTip(self.lang['ui.action_setting_connection_2'])

    def open_dialog(self) -> None:
        """
        打开数据库连接设置对话框。

        :rtype: None
        :return: 无返回值。
        """
        try:
            self.dialog_settings_connection = DialogSettingsConnection(self.lang_manager, self.config_manager)
            self.dialog_settings_connection.status_updated.connect(self.forward_status)
            self.dialog_settings_connection.exec_()
        except Exception:
            logger.exception(f"An error occurred while opening the settings dialog")
            self.status_updated.emit(self.lang['label_status_error'])

    def forward_status(self, message: str) -> None:
        """
        用于转发日志对话框中的信号。

        :rtype: None
        :return: 无返回值。
        """
        self.status_updated.emit(message)
