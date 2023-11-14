"""
这是一个用于管理和检查软件更新的Python模块。

此模块包含两个主要类：`ActionUpdate` 和 `UpdateChecker`。`ActionUpdate` 类负责初始化更新动作，并提供用户界面交互功能，允许用户检查和显示更新信息。`UpdateChecker` 类作为一个线程，用于后台检查软件的最新版本。

本模块的主要目的是提供一个简洁有效的方式来处理软件更新的检查和通知。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path
from lib.request_url import request_url
from module.settings import VERSION_INFO, CHECK_UPDATE_URL
from .message_show import message_show

# 初始化日志记录器
logger = logging.getLogger(__name__)


class ActionUpdate:
    """
    表示一个处理软件更新动作的类。

    此类封装了更新检查的界面逻辑，包括初始化更新菜单项、绑定相关事件、以及展示更新信息。

    :param main_window: 配置中心比较器的主窗口对象。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化更新动作。

        :param main_window: 配置中心比较器的主窗口对象。
        :type main_window: ConfigCenterComparer
        """
        self.main_window = main_window
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_update = QAction(QIcon(get_resource_path('media/icons8-update-26.png')), self.lang['ui.action_update_1'], self.main_window)
        self.action_update.setStatusTip(self.lang['ui.action_update_2'])
        self.action_update.setShortcut('F2')
        self.action_update.triggered.connect(self.check_update)

    def check_update(self) -> None:
        """
        检查软件的更新。

        此方法触发更新检查的流程，并在状态栏显示相关信息。
        """
        self.action_update.setEnabled(False)
        self.label_status.setText(self.lang['ui.action_update_8'])

        self.update_checker = UpdateChecker()
        self.update_checker.signal.connect(self.show_update_message)
        self.update_checker.start()

    def show_update_message(self, latest_version: str) -> None:
        """
        显示软件更新的消息。

        :param latest_version: 最新版本号。
        :type latest_version: str
        """
        self.action_update.setEnabled(True)
        self.label_status.setText(self.lang['ui.action_update_9'])
        current_version = VERSION_INFO

        if latest_version is None:
            message_show('Warning', self.lang['ui.action_update_3'])
        elif latest_version == current_version:
            message_show('Information', f"{self.lang['ui.action_update_5']}\n\n{self.lang['ui.action_update_7']}{current_version}")
        elif latest_version != current_version:
            message_show('Information', f"{self.lang['ui.action_update_4']}\n\n{self.lang['ui.action_update_6']}{current_version}\n{self.lang['ui.action_update_7']}{latest_version}")


class UpdateChecker(QThread):
    """
    用于后台检查软件更新的线程类。

    此类继承自 QThread，并在后台执行更新检查操作。它会发出信号以通知主线程最新的版本信息。

    使用 PyQt 的信号-槽机制来进行线程间的通信。
    """
    signal = pyqtSignal(str)

    def __init__(self):
        """
        初始化更新检查器线程。
        """
        super().__init__()

    def run(self) -> None:
        """
        执行更新检查的主要逻辑。

        此方法在线程启动时被调用。它从指定的 URL 获取最新版本信息，并通过信号发送。
        """
        try:
            latest_version = request_url(CHECK_UPDATE_URL)
        except Exception as e:
            logger.exception(f"An error occurred while checking for updates: {e}")
            latest_version = None
        self.signal.emit(latest_version)
