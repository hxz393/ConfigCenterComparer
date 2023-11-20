"""
这是一个用于网络连接测试和状态显示的Python模块。

此模块包含两个主要类：`ActionTest` 和 `TestRun`。`ActionTest` 类负责初始化测试动作，并提供用户界面交互功能，允许用户检查和显示网络连接状态。`TestRun` 类作为一个线程，用于后台检查网络连接状态。

本模块的主要目的是提供一个简洁有效的方式来处理网络连接测试和状态显示。

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
from module.read_config import read_config
from module.test_connection import test_connection
from .message_show import message_show

logger = logging.getLogger(__name__)


class ActionTest:
    """
    负责处理网络连接测试的类。

    此类封装了网络测试的界面逻辑，包括初始化测试菜单项、绑定相关事件以及展示测试结果。

    :param main_window: 主窗口对象，提供界面元素和语言设置。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化网络连接测试动作。

        :param main_window: 主窗口对象，用于访问界面元素和语言设置。
        :type main_window: ConfigCenterComparer
        """
        self.main_window = main_window
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_test = QAction(QIcon(get_resource_path('media/icons8-computers-connecting-26.png')), self.lang['ui.action_test_1'], self.main_window)
        self.action_test.setShortcut('F9')
        self.action_test.setStatusTip(self.lang['ui.action_test_2'])
        self.action_test.triggered.connect(self.test)

    def test(self) -> None:
        """
        触发网络连接测试。

        此方法将禁用测试动作，并在状态栏显示正在测试的信息。
        """
        self.action_test.setEnabled(False)
        self.label_status.setText(self.lang['ui.action_test_7'])

        self.test_run = TestRun()
        self.test_run.signal.connect(self.show_result_message)

        self.test_run.start()

    def show_result_message(self, test_result) -> None:
        """
        显示网络连接测试结果。

        :param test_result: 测试结果列表，每个元素包含环境名称、SSH测试结果和MySQL测试结果。
        :type test_result: list
        """
        self.action_test.setEnabled(True)
        self.label_status.setText(self.lang['ui.action_test_8'])

        if not test_result:
            message_show('Warning', self.lang['ui.action_test_3'])
            return

        message_info = ''.join(
            f'<b>{result["env_name"]}</b> {self.lang["ui.action_test_4"]}<br>'
            f'<span style="color: {"green" if result["ssh_test_result"] else "red"};">'
            f'{"SSH " + self.lang["ui.action_test_5"] if result["ssh_test_result"] else "SSH " + self.lang["ui.action_test_6"]}</span> '
            f'<span style="color: {"green" if result["mysql_test_result"] else "red"};">'
            f'{"MySQL " + self.lang["ui.action_test_5"] if result["mysql_test_result"] else "MySQL " + self.lang["ui.action_test_6"]}</span><br>'
            for result in test_result
        )
        message_show('Information', message_info)


class TestRun(QThread):
    """
    用于后台执行网络连接测试的线程类。

    此类继承自 QThread，在后台执行网络连接测试。测试完成后，它会发出信号以通知主线程测试结果。

    使用 PyQt 的信号-槽机制来进行线程间的通信。
    """
    signal = pyqtSignal(list)

    def __init__(self):
        """
        初始化网络连接测试线程。
        """
        super().__init__()

    def run(self) -> None:
        """
        执行网络连接测试的主要逻辑。

        此方法在线程启动时被调用。它执行网络连接测试，并通过信号发送测试结果。
        """
        try:
            logger.info(f'Start running test')
            _, config_connection = read_config()
            test_result = test_connection(config_connection)
            logger.info(f'Test Completed')
        except Exception:
            logger.exception(f'Error during testing')
            test_result = None
        self.signal.emit(test_result)
