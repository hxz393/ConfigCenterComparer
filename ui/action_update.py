"""
此文件提供了软件更新检查和提示功能的实现。

主要包含两个类：`ActionUpdate` 和 `UpdateChecker`。`ActionUpdate` 负责初始化更新相关的 UI 组件，并触发更新检查。`UpdateChecker` 作为一个线程，负责在后台检查软件的最新版本并返回结果。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from config.settings import VERSION_INFO, CHECK_UPDATE_URL
from lib.get_resource_path import get_resource_path
from lib.request_url import request_url
from ui.lang_manager import LangManager
from ui.message_show import message_show

logger = logging.getLogger(__name__)


class ActionUpdate(QObject):
    """
    负责处理软件更新相关的用户界面操作。

    此类负责创建更新操作相关的动作，绑定必要的信号和槽，以及触发更新检查。

    :param lang_manager: 语言管理器实例，用于更新界面语言。
    :type lang_manager: LangManager
    """
    status_updated = pyqtSignal(str)

    def __init__(self, lang_manager: LangManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.initUI()

    def initUI(self) -> None:
        """
        初始化更新操作的用户界面组件。

        创建一个更新操作的 QAction 对象，并设置其图标、快捷键和触发方法。同时调用 `update_lang` 方法更新界面语言。

        :rtype: None
        :return: 无返回值。
        """
        self.action_update = QAction(QIcon(get_resource_path('media/icons8-update-26.png')), 'Update')
        self.action_update.setShortcut('F2')
        self.action_update.triggered.connect(self.check_update)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_update.setText(self.lang['ui.action_update_1'])
        self.action_update.setStatusTip(self.lang['ui.action_update_2'])

    def check_update(self) -> None:
        """
        检查软件的更新。

        此方法触发更新检查的流程，并在状态栏显示相关信息。创建 `UpdateChecker` 实例并启动线程。

        :rtype: None
        :return: 无返回值。
        """
        self.action_update.setEnabled(False)
        self.status_updated.emit(self.lang['ui.action_update_8'])

        self.update_checker = UpdateChecker()
        self.update_checker.signal.connect(self.show_update_message)
        self.update_checker.start()

    def show_update_message(self, latest_version: str) -> None:
        """
        显示软件更新的消息。

        :param latest_version: 最新版本号。
        :type latest_version: str

        :rtype: None
        :return: 无返回值。
        """
        self.action_update.setEnabled(True)
        self.status_updated.emit(self.lang['ui.action_update_9'])
        current_version = VERSION_INFO

        if latest_version is None:
            message_show('Warning', self.lang['ui.action_update_3'])
        elif latest_version == current_version:
            message_show('Information', f"{self.lang['ui.action_update_5']}\n\n{self.lang['ui.action_update_7']}{current_version}")
        else:
            message_show('Information', f"{self.lang['ui.action_update_4']}\n\n{self.lang['ui.action_update_6']}{current_version}\n{self.lang['ui.action_update_7']}{latest_version}")


class UpdateChecker(QThread):
    """
    用于后台检查软件更新的线程类。

    此类继承自 QThread，并在后台执行更新检查操作。它会发出信号以通知主线程最新的版本信息。

    使用 PyQt 的信号-槽机制来进行线程间的通信。
    """
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        """
        执行更新检查的主要逻辑。

        此方法在线程启动时被调用。它从指定的 URL 获取最新版本信息，并通过信号发送。

        :rtype: None
        :return: 无返回值。
        """
        try:
            latest_version = request_url(CHECK_UPDATE_URL)
            logger.info(f"The latest version: {latest_version}")
        except Exception:
            logger.exception("An error occurred while checking for updates")
            latest_version = None
        self.signal.emit(latest_version)
