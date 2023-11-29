"""
此模块提供用于管理和展示日志相关操作的用户界面组件。

此模块包含一个主要的类 `ActionLogs`，它负责初始化用户界面组件，管理日志查看操作，并且更新界面语言设置。该模块还与外部资源和多语言支持紧密结合，为用户提供一个直观、易用的界面来查看和管理日志。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from ui.dialog_logs import DialogLogs
from ui.lang_manager import LangManager
from ui.global_signals import global_signals

logger = logging.getLogger(__name__)


class ActionLogs(QObject):
    """
    提供日志相关的用户界面操作。

    此类负责创建日志查看的动作，包括初始化界面组件和处理日志查看相关的事件。它利用 `DialogLogs` 和 `LangManager` 来展示和管理日志信息。

    :param lang_manager: 语言管理器，用于更新动作的显示语言。
    :type lang_manager: LangManager
    :param lang_manager: 语言管理器，用于更新动作的显示语言。
    :type lang_manager: LangManager
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager):
        super().__init__()
        # 实例化语言管理类
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)

        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        self.action_logs = QAction(QIcon(get_resource_path('media/icons8-log-26.png')), 'View Logs')
        self.action_logs.setShortcut('F3')
        self.action_logs.triggered.connect(self.open_dialog)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_logs.setText(self.lang['ui.action_logs_1'])
        self.action_logs.setStatusTip(self.lang['ui.action_logs_2'])

    def open_dialog(self) -> None:
        """
        打开日志对话框。

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 实例化显示方式，非阻塞调用。exec_()为阻塞调用。
            self.dialog_logs = DialogLogs(self.lang_manager)
            self.dialog_logs.status_updated.connect(self.forward_status)
            self.dialog_logs.show()
            # 连接全局信号，主窗口关闭时一并关闭。
            global_signals.close_all.connect(self.close_dialog)
        except Exception:
            logger.exception("An error occurred while opening the logs dialog")
            self.status_updated.emit(self.lang['label_status_error'])

    def close_dialog(self) -> None:
        """
        关闭日志对话框。由主窗口发送信号调用，避免主窗口关闭后，日志窗口还运行。

        :rtype: None
        :return: 无返回值。
        """
        if self.dialog_logs is not None:
            self.dialog_logs.close()

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :type message: str

        :rtype: None
        :return: 无返回值。
        """
        self.status_updated.emit(message)
