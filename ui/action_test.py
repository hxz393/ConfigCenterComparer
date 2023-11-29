"""
本模块提供了网络连接测试的功能，包括界面的交互元素以及后台的连接测试逻辑。

本模块定义了 `ActionTest` 类用于处理用户界面中的网络测试操作，以及 `TestRun` 类用于在后台线程中执行实际的网络连接测试。
这些类支持通过图形界面对网络连接进行测试，并显示相应的测试结果。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from module.test_connection import test_connection
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager
from ui.message_show import message_show

logger = logging.getLogger(__name__)


class ActionTest(QObject):
    """
    界面操作类，用于处理网络连接测试的界面交互。

    此类通过图形界面提供网络测试功能，包括测试操作的触发和结果展示。

    :param lang_manager: 语言管理器，用于多语言支持。
    :type lang_manager: LangManager
    :param config_manager: 配置管理器，用于获取网络测试相关配置。
    :type config_manager: ConfigManager
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.config_manager = config_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面。

        创建并配置界面中的测试动作按钮，包括图标、快捷键和触发事件。

        :rtype: None
        :return: 无返回值。
        """
        self.action_test = QAction(QIcon(get_resource_path('media/icons8-computers-connecting-26.png')), 'Test')
        self.action_test.setShortcut('F9')
        self.action_test.triggered.connect(self.test)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_test.setText(self.lang['ui.action_test_1'])
        self.action_test.setStatusTip(self.lang['ui.action_test_2'])

    def test(self) -> None:
        """
        触发网络连接测试。

        此方法将禁用测试动作，并在状态栏显示正在测试的信息。

        :rtype: None
        :return: 无返回值。
        """
        self.action_test.setEnabled(False)
        self.status_updated.emit(self.lang['ui.action_test_7'])

        self.test_run = TestRun(self.config_manager)
        self.test_run.signal.connect(self.show_result_message)
        self.test_run.start()

    def show_result_message(self, test_result) -> None:
        """
        显示网络连接测试结果。

        :param test_result: 测试结果列表，每个元素包含环境名称、SSH测试结果和MySQL测试结果。
        :type test_result: list

        :rtype: None
        :return: 无返回值。
        """
        self.action_test.setEnabled(True)
        self.status_updated.emit(self.lang['ui.action_test_8'])

        if not test_result:
            message_show('Critical', self.lang['ui.action_test_3'])
            return

        message_info = ''.join(
            f'<b>{result["env_name"]}</b> {self.lang["ui.action_test_4"]}<br>'
            f'{self.format_test_result(result, "SSH")} '
            f'{self.format_test_result(result, "MySQL")}<br>'
            for result in test_result
        )
        message_show('Information', message_info)

    def format_test_result(self,
                           result: Dict[str, any],
                           test_type: str) -> str:
        """
        根据测试结果和测试类型格式化消息字符串。

        此方法会检查指定测试类型的结果，并根据结果的状态（成功、失败、未知）返回不同颜色的消息字符串。

        :param result: 包含测试类型和其对应结果的字典。
        :type result: Dict[str, any]
        :param test_type: 要检查的测试类型。
        :type test_type: str

        :return: 格式化后的带颜色的消息字符串。
        :rtype: str
        """
        if result[test_type] is True:
            color = "green"
            message = f'<b>{self.lang["ui.action_test_5"]}</b>'
        elif result[test_type] is False:
            color = "red"
            message = f'<b>{self.lang["ui.action_test_6"]}</b>'
        else:
            color = "gray"
            message = f'<b>{self.lang["ui.action_test_9"]}</b>'

        return f'{test_type} {self.lang["ui.action_test_10"]}<span style="color: {color};">{message}</span><br>'


class TestRun(QThread):
    """
    后台测试运行类，用于在单独的线程中执行网络连接测试。

    此类创建一个线程，用于运行网络连接测试，并将测试结果通过信号发送回界面。

    :param config_manager: 配置管理器，用于获取网络测试的配置。
    :type config_manager: ConfigManager
    """
    signal = pyqtSignal(list)

    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.config_connection = self.config_manager.get_config_connection()

    def run(self) -> None:
        """
        线程执行方法，用于运行网络连接测试。

        在线程启动时被调用，执行网络连接测试，并通过信号发送测试结果。

        :rtype: None
        :return: 无返回值。
        """
        try:
            logger.info('Testing Run')
            test_result = test_connection(self.config_connection)
            logger.info('Test Completed')
        except Exception:
            logger.exception('Error during testing')
            test_result = None
        self.signal.emit(test_result)
