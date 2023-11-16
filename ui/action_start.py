"""
这是一个用于管理配置中心比较过程的Python模块。

此模块包含了多个类，包括`ActionStart`、`StartWork`和`TableResultsManager`。这些类协同工作，提供界面交互、后台处理以及结果展示的功能。它们是配置中心比较器的核心组成部分。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, List, Tuple

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from ConfigCenterComparer import ConfigCenterComparer
from config.settings import COL_INFO
from lib.get_resource_path import get_resource_path
from module.config_init import config_init
from module.start_query import start_query
from .message_show import message_show

logger = logging.getLogger(__name__)


class ActionStart:
    """
    负责初始化和启动配置比较过程的类。

    此类负责创建启动操作的用户界面组件，并绑定相应的事件。它还负责启动`StartWork`线程，以开始配置的比较和处理过程。

    :param main_window: 主窗口对象，提供界面交互的入口。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化启动动作。

        :param main_window: 主窗口对象。
        :type main_window: ConfigCenterComparer
        """
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.filter_bar = self.main_window.get_elements('filter_bar')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.action_start = QAction(QIcon(get_resource_path('media/icons8-start-26.png')), self.lang['ui.action_start_1'], self.main_window)
        self.action_start.setShortcut('F10')
        self.action_start.setStatusTip(self.lang['ui.action_start_2'])
        self.action_start.triggered.connect(self.start)

    def start(self) -> None:
        """
        启动配置比较过程。

        此方法会禁用启动按钮，更新状态栏信息，并创建并启动 `StartWork` 线程以开始配置比较过程。

        通过 PyQt 的信号-槽机制，此方法还会处理线程完成时的回调，以更新用户界面和显示结果信息。
        """
        self.action_start.setEnabled(False)
        self.label_status.setText(self.lang['ui.action_start_3'])

        self.start_work = StartWork(self.table, self.filter_bar, self.lang)
        self.start_work.signal.connect(self.show_result_message)
        self.start_work.start()

    def show_result_message(self, result: int):
        """
        显示配置比较结果的消息。

        此方法根据配置比较的结果显示不同的消息提示。

        :param result: 配置比较的结果代码。
        :type result: int
        """
        self.action_start.setEnabled(True)
        self.label_status.setText(self.lang['label_status_error'] if result else '')
        message = {
            1: ('Warning', self.lang['ui.action_start_4']),
            2: ('Warning', self.lang['ui.action_start_5']),
            -1: ('Critical', self.lang['ui.action_start_7'])
        }.get(result, None)
        if message:
            message_show(*message)


class StartWork(QThread):
    """
    用于后台执行配置比较的线程类。

    此类继承自 QThread，并在后台执行配置比较操作。它会发出信号以通知主线程比较的结果。

    使用 PyQt 的信号-槽机制来进行线程间的通信。
    """
    signal = pyqtSignal(int)

    def __init__(self, table, filter_bar, lang):
        """
        初始化配置比较器线程。

        :param table: 表格对象，用于显示比较结果。
        :type table: QTableWidget
        :param filter_bar: 过滤栏对象，用于设置过滤条件。
        :type filter_bar: FilterBar
        :param lang: 语言字典。
        :type lang: Dict
        """
        super().__init__()
        self.table = table
        self.filter = filter_bar
        self.table_results_manager = TableResultsManager(table, lang)
        self.config_main, self.config_connection = None, None

    def run(self) -> None:
        """
        执行配置比较器线程的主要工作流程。

        此方法包括初始化配置、执行查询、处理查询结果以及处理异常情况等步骤。它在后台执行，不会阻塞主界面的响应。
        线程完成或出现异常时，会发出信号通知主线程。
        """
        try:
            self.initialize()
            if not self.perform_query():
                return
            self.finalize()
            self.signal.emit(0)
        except Exception:
            logger.exception('Error occurred during execution')
            self.signal.emit(-1)

    def initialize(self):
        """
        初始化配置比较器线程。

        此方法会清空表格数据，禁用表格排序，并加载配置信息。它是配置比较过程开始前的准备步骤。
        """
        # 清空表格数据
        self.table.clear()
        # 禁用表格排序，防止展示空数据
        self.table.setSortingEnabled(False)
        # 加载配置信息
        self.config_main, self.config_connection = config_init()

    def perform_query(self) -> bool:
        """
        执行配置查询操作。

        此方法会调用 `start_query` 函数，执行配置查询。如果查询成功，将结果添加到表格中；如果查询失败，发送相应的信号。
        :return: 查询是否成功。
        :rtype: bool
        """
        query_results = start_query(self.config_connection, self.config_main)
        if not query_results:
            self.signal.emit(1)
            return False

        add_to_table_result = self.table_results_manager.add_results_to_table(query_results)
        if not add_to_table_result:
            self.signal.emit(2)
            return False

        return True

    def finalize(self) -> None:
        """
        完成配置比较器线程的收尾工作。

        此方法在配置比较完成后执行，包括启动表格排序、更新过滤器等操作。它是配置比较过程结束后的整理步骤。
        """
        # 启动排序
        self.table.setSortingEnabled(True)
        # 默认按第一列升序排序
        self.table.sortByColumn(0, Qt.AscendingOrder)
        # 更新过滤器，过滤服务中插入值
        self.filter.filter_options_add()
        # 运行过滤器
        self.filter.filter_table()


class TableResultsManager:
    """
    用于管理和展示表格结果的类。

    此类提供了添加查询结果到表格、准备表格行数据、以及根据查询状态更新表格列显示或隐藏的功能。

    :param table: 用于显示结果的表格对象。
    :type table: Table
    :param lang: 用于国际化的语言字典。
    :type lang: Dict[str, str]
    """

    def __init__(self, table, lang):
        """
        初始化类。

        :param table: 表格对象，用于显示比较结果。
        :type table: QTableWidget
        :param lang: 语言字典。
        :type lang: Dict
        """
        self.table = table
        self.lang = lang

    def add_results_to_table(self, query_results: List) -> bool:
        """
        将查询结果添加到表格中。

        此方法处理格式化结果和查询状态，然后更新表格内容。

        :param query_results: 包含格式化结果和查询状态的元组。
        :type query_results: Tuple[Dict, Dict]
        :return: 是否成功添加到表格。
        :rtype: bool
        """
        try:
            formatted_results, query_statuses = query_results
            table_rows = self.prepare_table_rows(formatted_results)
            self.add_rows_to_table(table_rows)
            self.update_table_column_hide(query_statuses)
            return True
        except Exception:
            logger.exception('Error occurred during adding results to table')
            return False

    def prepare_table_rows(self, formatted_results: Dict) -> List[List]:
        """
        准备要添加到表格的行数据。

        根据提供的格式化结果，此方法生成表格所需的行数据列表。

        :param formatted_results: 格式化后的查询结果。
        :type formatted_results: Dict
        :return: 表格行数据列表。
        :rtype: List[List]
        """
        # 定义状态映射
        consistency_status_mapping = {
            "0": self.lang['ui.action_start_8'],
            "1": self.lang['ui.action_start_9'],
            "2": self.lang['ui.action_start_10']
        }
        skip_status_mapping = {
            "0": self.lang['ui.action_start_11'],
            "1": self.lang['ui.action_start_12']
        }

        # 基本键列表
        basic_keys = [
            'app_id', 'namespace_name', 'key',
            'PRO_CONFIG', 'PRO_CONFIG_modified_time',
            'PRE_CONFIG', 'PRE_CONFIG_modified_time',
            'TEST_CONFIG', 'TEST_CONFIG_modified_time',
            'DEV_CONFIG', 'DEV_CONFIG_modified_time'
        ]
        return [
            [
                [result.get(key, 'None'), result.get(key, 'None')]
                for key in basic_keys
            ] + [
                [consistency_status_mapping.get(result['consistency_status'], self.lang['ui.action_start_13']), result['consistency_status']],
                [skip_status_mapping.get(result['skip_status'], self.lang['ui.action_start_13']), result['skip_status']],
            ]
            for result in formatted_results.values()
        ]

    def add_rows_to_table(self, table_rows: List[List]):
        """
        将行数据添加到表格中。

        遍历提供的行数据列表，将每行数据添加到表格中。

        :param table_rows: 表格行数据列表。
        :type table_rows: List[List]
        """
        for row in table_rows:
            self.table.add_row(row)

    def update_table_column_hide(self, query_statuses: Dict):
        """
        根据查询状态更新表格列的显示或隐藏。

        根据查询状态字典，决定每列的显示或隐藏。

        :param query_statuses: 包含列名称和状态的字典。
        :type query_statuses: Dict
        """
        column_name_mapping = {'PRO_CONFIG': 'pro_value', 'PRE_CONFIG': 'pre_value', 'TEST_CONFIG': 'test_value', 'DEV_CONFIG': 'dev_value'}
        for k, v in query_statuses.items():
            action = self.table.showColumn if v else self.table.hideColumn
            action(COL_INFO[column_name_mapping[k]]['col'])
