"""
这是一个包含类 ActionExit 的 Python 文件，用于在 PyQt5 应用程序中处理退出操作。

ActionExit 类定义了应用程序的退出动作。它主要用于创建一个 QAction，当触发时，会执行应用程序的退出操作。这个类接收一个 ConfigCenterComparer 实例作为主窗口，以便于访问和操作界面元素。它定义了退出操作的具体逻辑，并在执行过程中处理可能出现的异常。

类的 `__init__` 方法初始化 ActionExit 实例，设置动作的属性，并连接到退出操作。`exit` 方法定义了退出操作的具体实现，它尝试退出应用程序，并在出现异常时记录错误信息。

这个模块主要用于在基于 PyQt5 的界面中集成和处理退出动作，是界面用户交互的重要组成部分。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path

# 初始化日志记录器
logger = logging.getLogger(__name__)


class ActionExit:
    """
    定义一个退出动作的类，用于处理程序的退出操作。

    :type main_window: ConfigCenterComparer
    :param main_window: 主窗口对象，用于访问和操作界面元素。
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化 ActionExit 类的实例。

        :param main_window: 主窗口对象。
        """
        self.main_window = main_window
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_exit = QAction(QIcon(get_resource_path('media/icons8-exit-26.png')), self.lang['ui.action_exit_1'], main_window)
        self.action_exit.setShortcut('Ctrl+Q')
        self.action_exit.setStatusTip(self.lang['ui.action_exit_2'])
        self.action_exit.triggered.connect(self.exit)

    def exit(self) -> None:
        """
        执行退出操作。

        :rtype: None
        :return: 无返回值。
        """
        try:
            QCoreApplication.quit()
        except Exception:
            logger.exception(f"Exiting application error")
            self.label_status.setText(self.lang['label_status_error'])
