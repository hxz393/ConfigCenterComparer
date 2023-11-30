"""
提供应用程序的主要功能，包括用户界面初始化、数据库查询执行、数据展示和处理。

本模块中包含的类负责应用程序的主要操作流程，如用户界面的初始化、按钮动作的处理、后台数据查询、数据展示等。主要类包括`ActionStart`和`StartWork`，分别负责处理用户界面动作和执行后台工作。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, List

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QHeaderView

from config.settings import COL_INFO
from lib.get_resource_path import get_resource_path
from module.execute_queries import execute_queries
from ui.config_manager import ConfigManager
from ui.filter_bar import FilterBar
from ui.lang_manager import LangManager
from ui.message_show import message_show
from ui.table_main import TableMain

logger = logging.getLogger(__name__)


class ActionStart(QObject):
    """
    负责处理用户界面动作，例如初始化界面、响应按钮点击等。

    此类包含了界面的主要动作逻辑，如开始按钮的点击处理、用户界面语言的更新、表格的数据填充等。它与后台线程`StartWork`协作，实现数据的查询和展示。

    :param lang_manager: 语言管理器，用于界面语言的加载和更新。
    :param config_manager: 配置管理器，提供应用程序的配置信息。
    :param table: 主表格界面，用于数据的展示。
    :param filter_bar: 过滤条，用于数据的筛选。
    :type lang_manager: LangManager
    :type config_manager: ConfigManager
    :type table: TableMain
    :type filter_bar: FilterBar
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager,
                 table: TableMain,
                 filter_bar: FilterBar):
        super().__init__()
        # 实例化组件
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.table = table
        self.filter_bar = filter_bar
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面。

        创建并配置界面中的开始动作按钮，包括图标、快捷键和触发事件。

        :rtype: None
        :return: 无返回值。
        """
        self.action_start = QAction(QIcon(get_resource_path('media/icons8-start-26.png')), 'Start')
        self.action_start.setShortcut('F10')
        self.action_start.triggered.connect(self.start)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_start.setText(self.lang['ui.action_start_1'])
        self.action_start.setStatusTip(self.lang['ui.action_start_2'])

    def start(self) -> None:
        """
        启动更新动作的处理流程。

        此方法负责初始化和启动一个后台线程 `StartWork`，该线程执行数据查询和表格更新。同时，该方法还负责连接信号和槽以进行 UI 更新。

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 初始化子线程，传入语言字典和配置
            self.start_work = StartWork(self.lang, self.config_manager)
            # 连接信号槽，都是 UI 操作，必须主线程中进行
            self.start_work.initialize_signal.connect(self.initialize)
            self.start_work.table_insert_signal.connect(self.table_insert)
            self.start_work.table_column_hide_signal.connect(self.table_column_hide)
            self.start_work.finalize_signal.connect(self.finalize)
            self.start_work.message.connect(self.show_result_message)
            # 开始运行
            self.start_work.start()
        except Exception:
            logger.exception('Failed to initiate start action.')
            self.status_updated.emit(self.lang['label_status_error'])

    def initialize(self) -> None:
        """
        初始化界面和状态，在开始操作前执行。

        此方法用于设置 UI 元素的初始状态，如禁用按钮、清空表格等。

        :rtype: None
        :return: 无返回值。
        """
        logger.info('Start running')
        # 状态栏发送提示消息
        self.status_updated.emit(self.lang['ui.action_start_3'])
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

    def table_insert(self, table_rows: List[List[List[str]]]) -> None:
        """
        将查询结果插入到主表格中。

        此方法接收查询结果作为输入，并将其格式化后插入到应用程序的主表格中。每个元素是一个三重列表，表示表格的一行数据。

        :param table_rows: 待插入的表格数据，每个元素代表一行数据。
        :type table_rows: List[List[List[str]]]

        :rtype: None
        :return: 无返回值。
        """
        for row in table_rows:
            self.table.add_row(row)
        logger.debug('Table filling finished.')

    def table_column_hide(self, query_statuses: Dict[str, bool]) -> None:
        """
        根据查询状态决定是否隐藏表格的某些列。

        :param query_statuses: 各查询状态的字典，键为环境名，值为布尔值指示是否开启。
        :type query_statuses: Dict[str, bool]

        :rtype: None
        :return: 无返回值。
        """
        # env_name类似'PRO_CONFIG'，COL_INFO中的键类似'pro_value'，env_switch是布尔值。
        for env_name, env_switch in query_statuses.items():
            # 建立env_name和COL_INFO中的键的映射
            column_name_mapping = {'PRO_CONFIG': 'pro_value', 'PRE_CONFIG': 'pre_value', 'TEST_CONFIG': 'test_value', 'DEV_CONFIG': 'dev_value'}
            # 获取列序号
            col = COL_INFO[column_name_mapping[env_name]]['col']
            # 根据环境开关，决定列是否隐藏。
            self.table.showColumn(col) if env_switch else self.table.hideColumn(col)

    def finalize(self) -> None:
        """
        完成查询后的收尾工作，包括重新启用表格排序和更新等。

        :rtype: None
        :return: 无返回值。
        """
        # 先应用颜色和过滤器
        self.table.apply_color_to_table()
        self.filter_bar.filter_table()
        # 启动排序
        self.table.setSortingEnabled(True)
        # 默认按第一列升序排序
        self.table.sortByColumn(0, Qt.AscendingOrder)
        # 允许用户调整列宽
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # 更新过滤器，过滤服务中插入值
        self.filter_bar.filter_options_add()
        # 调用过滤器
        self.filter_bar.highlight_rows.clear()
        self.filter_bar.filter_table()
        # 启用表格更新
        self.table.setUpdatesEnabled(True)
        # 启用过滤栏组件
        self.filter_bar.filter_app_box.setEnabled(True)
        self.filter_bar.filter_table_box.setEnabled(True)
        self.filter_bar.filter_table_check_box.setEnabled(True)
        self.filter_bar.filter_value_box.setEnabled(True)
        self.filter_bar.filter_value_button.setEnabled(True)
        self.filter_bar.filter_reset_button.setEnabled(True)

    def show_result_message(self, result: str) -> None:
        """
        显示结果消息。

        根据运行结果，显示不同的状态消息或错误信息。

        :param result: 运行结果的描述。
        :type result: str

        :rtype: None
        :return: 无返回值。
        """
        self.action_start.setEnabled(True)
        if result == 'done':
            logger.info('Run Completed')
        else:
            message = {
                'no query result': ('Warning', self.lang['ui.action_start_4']),
                'prepare table rows failed': ('Warning', self.lang['ui.action_start_6']),
                'run error': ('Critical', self.lang['ui.action_start_7'])
            }.get(result)
            if message:
                message_show(*message)
            self.status_updated.emit(self.lang['label_status_error'])


class StartWork(QThread):
    """
    在后台执行数据库查询和数据处理。

    此类作为一个后台线程，负责执行数据库查询和结果的初步处理。它接收来自`ActionStart`的指令，进行数据的查询和处理，并通过信号将结果返回给前端进行展示。

    :param lang: 当前的语言设置，用于在处理过程中的文本显示。
    :param config_manager: 配置管理器，提供数据库查询所需的配置信息。
    :type lang: Dict[str, str]
    :type config_manager: ConfigManager
    """
    initialize_signal = pyqtSignal()
    message = pyqtSignal(str)
    table_insert_signal = pyqtSignal(list)
    table_column_hide_signal = pyqtSignal(dict)
    finalize_signal = pyqtSignal()

    def __init__(self,
                 lang: Dict[str, str],
                 config_manager: ConfigManager) -> None:
        super().__init__()
        self.lang = lang
        self.config_manager = config_manager

    def run(self) -> None:
        """
        执行后台查询和数据处理的主要逻辑。

        此方法作为线程的入口点，负责执行应用程序的核心逻辑。它首先通过发出信号来初始化UI，然后从配置管理器读取配置信息，执行数据库查询，并根据查询结果准备表格数据。完成这些步骤后，它将通过信号与前端UI进行通信，进行数据展示和状态更新。

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 开始初始化准备工作
            self.initialize_signal.emit()

            # 读取配置信息，开始数据库查询
            config_main = self.config_manager.get_config_main()
            config_connection = self.config_manager.get_config_connection()
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
            self.finalize_signal.emit()
            self.message.emit('done')
        except Exception:
            logger.exception('Error occurred during execution')
            self.message.emit('run error')

    def prepare_table_rows(self, formatted_results: Dict[str, Dict[str, str]]) -> List[List[List[str]]]:
        """
        准备插入到表格中的数据行。

        此方法将查询结果格式化为表格可以接受的数据结构。

        :param formatted_results: 格式化后的查询结果。
        :type formatted_results: Dict[str, Dict[str, str]]

        :return: 准备好的表格数据行。
        :rtype: List[List[List[str]]]
        """
        # 一致性状态用户数据和显示文字映射关系。
        otherwise_unknown = self.lang['ui.action_start_13']
        consistency_status_mapping = {
            "inconsistent": self.lang['ui.action_start_8'],
            "fully": self.lang['ui.action_start_9'],
            "partially": self.lang['ui.action_start_10'],
            "unknown": otherwise_unknown,
        }
        # 忽略状态用户数据和显示文字映射关系。
        skip_status_mapping = {
            "no": self.lang['ui.action_start_11'],
            "yes": self.lang['ui.action_start_12'],
            "unknown": otherwise_unknown,
        }
        # 基本键列表，用户数据和显示文字一样。
        basic_keys = [
            'app_id', 'namespace_name', 'key',
            'PRO_CONFIG', 'PRO_CONFIG_modified_time',
            'PRE_CONFIG', 'PRE_CONFIG_modified_time',
            'TEST_CONFIG', 'TEST_CONFIG_modified_time',
            'DEV_CONFIG', 'DEV_CONFIG_modified_time'
        ]
        # 构建表数据
        return [
            [
                [result.get(key, 'None'), result.get(key, 'None')]
                for key in basic_keys
            ] + [
                [consistency_status_mapping.get(result['consistency_status'], otherwise_unknown), result['consistency_status']],
                [skip_status_mapping.get(result['skip_status'], otherwise_unknown), result['skip_status']],
            ]
            for result in formatted_results.values()
        ]
