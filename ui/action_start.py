"""
这是一个用于配置中心比较器的 PyQt 应用程序模块。

该模块包含 `ActionStart` 和 `StartWork` 两个主要类。`ActionStart` 类负责初始化并处理用户界面的交互功能，如开始操作、显示状态信息等。`StartWork` 类则作为一个后台线程，处理数据查询和表格更新操作。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""


import logging
from typing import Dict, List, Tuple, Any

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QHeaderView

from ConfigCenterComparer import ConfigCenterComparer
from config.settings import COL_INFO
from lib.get_resource_path import get_resource_path
from module.read_config import read_config
from module.execute_queries import execute_queries
from .message_show import message_show

logger = logging.getLogger(__name__)


class ActionStart:
    """
    处理开始动作的类，负责用户界面交互和子线程的初始化。

    此类封装了与软件启动相关的逻辑，包括初始化动作按钮、绑定事件和更新界面状态。

    :param main_window: 主窗口对象，用于界面元素的交互和更新。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化 `ActionStart` 类的实例。

        :param main_window: 主窗口对象，提供界面交互功能。
        :type main_window: ConfigCenterComparer
        """
        # 获取需要交互的主界面组件
        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.filter_bar = self.main_window.get_elements('filter_bar')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')
        # 惯例动作属性配置
        self.action_start = QAction(QIcon(get_resource_path('media/icons8-start-26.png')), self.lang['ui.action_start_1'], self.main_window)
        self.action_start.setShortcut('F10')
        self.action_start.setStatusTip(self.lang['ui.action_start_2'])
        self.action_start.triggered.connect(self.start)

    def start(self) -> None:
        """
        启动更新动作的处理流程。

        此方法负责初始化和启动一个后台线程 `StartWork`，该线程执行数据查询和表格更新。同时，该方法还负责连接信号和槽以进行 UI 更新。

        :return: None
        """
        # 初始化子线程，传入语言字典
        self.start_work = StartWork(self.lang)
        # 连接信号槽，都是 UI 操作，必须主线程中进行
        self.start_work.initialize_signal.connect(self.initialize)
        self.start_work.table_insert_signal.connect(self.table_insert)
        self.start_work.table_column_hide_signal.connect(self.table_column_hide)
        self.start_work.finalize_signal.connect(self.finalize)
        self.start_work.message.connect(self.show_result_message)
        # 开始运行
        self.start_work.start()

    def initialize(self) -> None:
        """
        初始化界面和状态，在开始操作前执行。

        此方法用于设置 UI 元素的初始状态，如禁用按钮、清空表格等。

        :return: None
        """
        logger.info(f'Start running')
        # 状态栏发送提示消息
        self.label_status.setText(self.lang['ui.action_start_3'])
        # 开始按钮不可点击
        self.action_start.setEnabled(False)
        # 禁用表格排序
        self.table.setSortingEnabled(False)
        # 禁用表格更新
        self.table.setUpdatesEnabled(False)
        # 禁用过滤栏组件
        self.filter_bar.filter_app_box.setEnabled(False)
        self.filter_bar.filter_table_box.setEnabled(False)
        self.filter_bar.filter_table_check_box.setEnabled(False)
        self.filter_bar.filter_value_box.setEnabled(False)
        self.filter_bar.filter_value_button.setEnabled(False)
        self.filter_bar.filter_reset_button.setEnabled(False)
        # 清空表格数据
        self.table.clear()
        # 初始化表宽
        self.table.set_header_resize()
        logger.debug('Initialization finished')

    def table_insert(self, table_rows: List[Tuple]) -> None:
        """
        向表格中插入行。

        :param table_rows: 要插入的行数据，每行是一个元组。
        :type table_rows: List[Tuple]
        :return: None
        """
        [self.table.add_row(row) for row in table_rows]

    def table_column_hide(self, query_statuses: Dict[str, bool]) -> None:
        """
        根据查询状态决定是否隐藏表格的某些列。

        :param query_statuses: 各查询状态的字典，键为状态名，值为布尔值指示是否显示列。
        :type query_statuses: Dict[str, bool]
        :return: None
        """
        for k, v in query_statuses.items():
            column_name_mapping = {'PRO_CONFIG': 'pro_value', 'PRE_CONFIG': 'pre_value', 'TEST_CONFIG': 'test_value', 'DEV_CONFIG': 'dev_value'}
            action = self.table.showColumn if v else self.table.hideColumn
            action(COL_INFO[column_name_mapping[k]]['col'])
        logger.debug('Insert to Table Finished.')

    # def finalize(self, config_connection: Dict[str, Any], config_main: Dict[str, Any]) -> None:
    def finalize(self, configs: Tuple[Dict[str, Any], Dict[str, Any]]) -> None:
        """
        完成查询后的收尾工作，包括重新启用表格排序和更新。

        :param configs: 配置元祖。
        :type configs: Tuple[Dict[str, Any], Dict[str, Any]]

        :return: None
        """
        config_connection, config_main = configs
        # 启动排序
        self.table.setSortingEnabled(True)
        # 默认按第一列升序排序
        self.table.sortByColumn(0, Qt.AscendingOrder)
        # 允许用户调整列宽
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # 更新过滤器，过滤服务中插入值
        self.filter_bar.filter_options_add()
        # 初始化表格颜色
        if config_main.get('color_set', 'ON') == 'ON':
            self.table.apply_color_to_table(range(self.table.rowCount()), config_connection)
            logger.debug('Apply color to table finished')
        # 启用表格更新
        self.table.setUpdatesEnabled(True)
        # 启用过滤栏组件
        self.filter_bar.filter_app_box.setEnabled(True)
        self.filter_bar.filter_table_box.setEnabled(True)
        self.filter_bar.filter_table_check_box.setEnabled(True)
        self.filter_bar.filter_value_box.setEnabled(True)
        self.filter_bar.filter_value_button.setEnabled(True)
        self.filter_bar.filter_reset_button.setEnabled(True)
        # 最后调用过滤器
        self.filter_bar.filter_table()

    def show_result_message(self, result: str) -> None:
        """
        显示结果消息。

        根据运行结果，显示不同的状态消息或错误信息。

        :param result: 运行结果的描述。
        :type result: str
        :return: None
        """
        self.action_start.setEnabled(True)
        if result == 'done':
            logger.info(f'Run Complete')
            return
        else:
            self.label_status.setText(self.lang['label_status_error'])
            message = {
                'no query result': ('Warning', self.lang['ui.action_start_4']),
                'prepare table rows failed': ('Warning', self.lang['ui.action_start_6']),
                'run error': ('Critical', self.lang['ui.action_start_7'])
            }.get(result)
            if message:
                message_show(*message)


class StartWork(QThread):
    """
    后台线程类，用于执行数据查询和更新 UI 操作。

    该类继承自 `QThread`，在后台执行数据查询和处理任务。通过发射信号与主 UI 线程通信，实现数据的加载和界面的更新。

    :param lang: 提供多语言支持，用于在 UI 上显示不同语言的文本。
    :type lang: dict
    """
    initialize_signal = pyqtSignal()
    message = pyqtSignal(str)
    table_insert_signal = pyqtSignal(list)
    table_column_hide_signal = pyqtSignal(dict)
    finalize_signal = pyqtSignal(tuple)

    def __init__(self, lang: dict) -> None:
        """
        初始化 `StartWork` 类的实例。

        设置线程的语言参数，用于在后台处理过程中的多语言支持。

        :param lang: 用于多语言支持的语言字典。
        :type lang: dict
        :return: None
        """
        super().__init__()
        self.lang = lang

    def run(self) -> None:
        """
        线程执行的主要方法。

        在此方法中，执行所有必要查询操作，并发送信号以更新 UI。

        :return: None
        """
        try:
            # 开始初始化准备工作
            self.initialize_signal.emit()

            # 读取配置信息，开始数据库查询
            config_main, config_connection = read_config()
            formatted_results, query_statuses = execute_queries(config_connection, config_main)
            if not formatted_results:
                self.message.emit('no query result')
                return

            # 合成要插入表格的数据
            table_rows = self.prepare_table_rows(formatted_results)
            if not table_rows:
                self.message.emit('prepare table rows failed')
                return

            # 将数据插入到主表格
            self.table_insert_signal.emit(table_rows)
            # 隐藏主表格不必要的列
            self.table_column_hide_signal.emit(query_statuses)

            # 收尾工作
            self.finalize_signal.emit((config_connection, config_main))
            self.message.emit('done')
        except Exception:
            logger.exception('Error occurred during execution')
            self.message.emit('run error')

    def prepare_table_rows(self, formatted_results: Dict[str, Any]) -> List[List]:
        """
        准备插入到表格中的数据行。

        此方法将查询结果格式化为表格可以接受的数据结构。

        :param formatted_results: 格式化后的查询结果。
        :type formatted_results: Dict[str, Any]
        :return: 准备好的表格数据行。
        :rtype: List[List]
        """
        consistency_status_mapping = {
            "inconsistent": self.lang['ui.action_start_8'],
            "fully": self.lang['ui.action_start_9'],
            "partially": self.lang['ui.action_start_10']
        }
        skip_status_mapping = {
            "no": self.lang['ui.action_start_11'],
            "yes": self.lang['ui.action_start_12']
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
