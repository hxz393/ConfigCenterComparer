"""
此模块用于创建和管理调试操作界面，主要包括 ActionDebug 类。

ActionDebug 类提供了一个调试操作的接口，里面可以输入要调试的代码。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.filter_bar import FilterBar
from ui.lang_manager import LangManager
from ui.table_main import TableMain

logger = logging.getLogger(__name__)


class ActionDebug(QObject):
    """
    调试操作类，提供调试操作的界面和功能。

    :param lang_manager: 语言管理器实例，用于处理语言相关设置。
    :type lang_manager: LangManager
    :param config_manager: 配置管理器实例，用于管理配置。
    :type config_manager: ConfigManager
    :param table: 主表格界面实例。
    :type table: TableMain
    :param filter_bar: 过滤栏界面实例。
    :type filter_bar: FilterBar
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager,
                 table: TableMain,
                 filter_bar: FilterBar):
        super().__init__()
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.table = table
        self.filter_bar = filter_bar
        self.config_window = None
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        self.action_debug = QAction(QIcon(get_resource_path('media/icons8-debug-26.png')), 'Debug')
        self.action_debug.setShortcut('F6')
        self.action_debug.triggered.connect(self.debug)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_debug.setText(self.lang['ui.action_debug_1'])
        self.action_debug.setStatusTip(self.lang['ui.action_debug_2'])

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :type message: str

        :rtype: None
        :return: 无返回值。
        """
        self.status_updated.emit(message)

    def debug(self) -> None:
        """
        执行调试代码。

        :rtype: None
        :return: 无返回值。
        """
        self.status_updated.emit('Hello World!')
