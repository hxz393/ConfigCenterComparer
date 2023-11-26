"""
本文件包含用于处理和比较配置数据的类和函数。

该模块主要包含 `ActionCompare` 类，用于在用户界面中处理数据比较的逻辑。该类提供了对比配置数据、更新界面语言、重组数据等功能，方便用户进行环境配置的对比分析。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Optional, List

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from lib.log_time import log_time
from ui.config_manager import ConfigManager
from ui.dialog_comparison import DialogComparison
from ui.global_signals import global_signals
from ui.lang_manager import LangManager
from ui.message_show import message_show
from ui.table_main import TableMain

logger = logging.getLogger(__name__)


class ActionCompare(QObject):
    """
    提供数据比较功能的类。

    该类负责处理用户界面中的数据对比逻辑，包括初始化UI组件、更新语言设置、执行数据对比等功能。它还负责处理各种事件和信号，并更新用户界面状态。

    :param lang_manager: 语言管理器实例，用于处理界面语言更新。
    :type lang_manager: LangManager
    :param config_manager: 配置管理器，用于获取网络测试相关配置。
    :type config_manager: ConfigManager
    :param table: 主界面表格实例，提供数据获取和显示功能。
    :type table: TableMain
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager,
                 table: TableMain):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.table = table
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        self.action_compare = QAction(QIcon(get_resource_path('media/icons8-diff-files-26')), 'Compare')
        self.action_compare.setShortcut('F8')
        # 为了记录运行时间，使用匿名函数
        self.action_compare.triggered.connect(lambda checked=False: self.compare())
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_compare.setText(self.lang['ui.action_compare_1'])
        self.action_compare.setStatusTip(self.lang['ui.action_compare_2'])

    @log_time
    def compare(self) -> None:
        """
        执行数据对比操作。

        该方法首先从表格获取原始数据，然后对数据进行重组和对比分析。最终，它将对比结果展示在对话框中。

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 获取原表格数据到字典。
            original_data = self.table.get_table_data()
            if not original_data:
                logger.warning("No data available in the table for comparison.")
                message_show('Information', self.lang['ui.action_compare_4'])
                return

            # 对原表格数据进行重新整理分组。
            new_data = self._reorganize_data(original_data)
            if not new_data:
                logger.error("Data reorganization failed.")
                self.status_updated.emit(self.lang['label_status_error'])
                return

            # 对整理分组后的数据进行对比。
            result = self._compare_environments(new_data)
            if not result:
                logger.error("Environment comparison failed.")
                self.status_updated.emit(self.lang['label_status_error'])
                return

            # 打开带表格组件的对话框，展示结果。
            self.dialog_comparison = DialogComparison(self.lang_manager, self.config_manager, result)
            self.dialog_comparison.status_updated.connect(self.forward_status)
            self.dialog_comparison.show()
            # 连接全局信号，主窗口关闭时一并关闭。
            global_signals.close_all.connect(self.close_dialog)
        except Exception:
            logger.exception("An error occurred during data comparison.")
            self.status_updated.emit(self.lang['label_status_error'])

    def _reorganize_data(self, original_data: Dict[int, Dict[str, str]]) -> Optional[Dict[str, List[Dict[str, str]]]]:
        """
        将原始数据根据特定的规则进行重组。

        此方法接收原始数据字典，并按照预设的环境键进行重组，最终返回一个新的数据结构。

        :param original_data: 原始数据字典，键为行数，值对应一行数据。
        :type original_data: Dict[int, Dict[str, str]]
        :return: 重组后的数据字典。类似于：{'生产环境': [{'服务': 'service', '分组': 'application'}], '预览环境': [{'服务': 'service', '分组': 'application'}]}
        :rtype: Optional[Dict[str, List[Dict[str, str]]]]
        """
        try:
            # 先初始化字典结构，每个环境key对应一个值列表，列表内容为每行的数据
            env_keys = [
                self.lang['ui.dialog_settings_connection_2'],
                self.lang['ui.dialog_settings_connection_3'],
                self.lang['ui.dialog_settings_connection_4'],
                self.lang['ui.dialog_settings_connection_5']
            ]
            new_data = {env: [] for env in env_keys}

            # 获取每行的数据字典entry，类似于：{'服务': 'web', '分组': 'application'}
            for entry in original_data.values():
                # 表头中显示的环境名称，可直接在entry中作为key取值
                for env in env_keys:
                    # 只获取服务、分组、配置键和值四个元素
                    env_data = {
                        self.lang['ui.table_main_1']: entry[self.lang['ui.table_main_1']],
                        self.lang['ui.table_main_2']: entry[self.lang['ui.table_main_2']],
                        self.lang['ui.table_main_3']: entry[self.lang['ui.table_main_3']],
                        self.lang['ui.action_compare_3']: entry[env]
                    }
                    # 将数据插入到new_data字典中
                    new_data[env].append(env_data)

            return new_data
        except Exception:
            logger.exception("Failed to reorganize data.")
            return None

    def _compare_environments(self, new_data: Dict[str, List[Dict[str, str]]]) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
        """
        对不同环境的配置数据进行对比。

        此函数接收一个字典，字典的键是环境名称，值是对应该环境的配置项列表。它将每个环境的配置数据通过 filter_and_group_items 方法进行处理和分组。

        :param new_data: 各环境的配置数据。
        :type new_data: Dict[str, List[Dict[str, str]]]

        :return: 经过筛选和分组的环境配置数据。例如：{'生产环境': {'server.port+8088': [{'服务': 'service', '分组': 'application'}, {'服务': 'web', '分组': 'application'}],...},'预览环境': {},...}
        :rtype: Dict[str, Dict[str, List[Dict[str, str]]]]
        """
        # 按环境解包，items中有所有当前环境的配置
        return {env: self._filter_and_group_items(items) for env, items in new_data.items()}

    def _filter_and_group_items(self, items: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        """
        对给定的数据项进行筛选和分组。

        此函数接收一个列表，列表中的每个元素是字典，代表一行数据。它首先过滤掉值为'None'的项，然后根据特定的键值对数据进行分组。

        :param items: 要筛选和分组的数据列表。
        :type items: List[Dict[str, str]]

        :return: 分组后的数据字典。
        :rtype: Dict[str, List[Dict[str, str]]]
        """
        grouped = {}
        # 一个item是筛选后的一行数据
        for item in items:
            # 跳过None值，不加入对比
            if item.get(self.lang['ui.action_compare_3']) == 'None':
                continue
            # 拼接索引用的key
            key = f"{item[self.lang['ui.table_main_3']]}+{item[self.lang['ui.action_compare_3']]}"
            # 将行数据插入到列表中
            grouped.setdefault(key, []).append(item)
        # 筛选掉列表长度小于2的键值对
        return {k: v for k, v in grouped.items() if len(v) > 1}

    def close_dialog(self) -> None:
        """
        关闭展示对话框。由主窗口发送信号调用，避免主窗口关闭后，结果展示窗口还运行。

        :rtype: None
        :return: 无返回值。
        """
        if self.dialog_comparison is not None:
            self.dialog_comparison.close()

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :type message: str

        :rtype: None
        :return: 无返回值。
        """
        self.status_updated.emit(message)
