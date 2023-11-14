"""
这是一个用于配置中心比较和管理的Python模块。

此模块包含用于启动、运行和管理配置比较过程的类，其中包括`ActionStart`和`StartWork`。这些类协同工作，用于处理配置数据的获取、比较和展示。

本模块的主要目的是为用户提供一个界面来对比和管理不同环境中的配置数据。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path
from module.config_init import config_init
from module.start_query import start_query
from module.start_update_duplicate import start_update_duplicate
from module.start_update_filter import start_update_filter
from .message_show import message_show

# 初始化日志记录器
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
        启动配置比较的过程。

        此方法触发配置比较的流程，并在界面上展示相关状态信息。
        """
        self.action_start.setEnabled(False)
        self.label_status.setText(self.lang['ui.action_start_3'])

        self.start_work = StartWork(self.table, self.filter_bar, self.label_status)
        self.start_work.signal.connect(self.show_result_message)
        self.start_work.start()

    def show_result_message(self, result: int):
        """
        显示配置比较的结果信息。

        :param result: 配置比较的结果代码。
        :type result: int
        """
        self.action_start.setEnabled(True)
        if result == 0:
            return

        self.label_status.setText(self.lang['label_status_error'])
        if result == 1:
            message_show('Warning', self.lang['ui.action_start_4'])
        elif result == 2:
            message_show('Critical', self.lang['ui.action_start_5'])
        elif result == 3:
            message_show('Critical', self.lang['ui.action_start_6'])
        else:
            message_show('Critical', self.lang['ui.action_start_7'])


class StartWork(QThread):
    """
    用于后台执行配置比较的线程类。

    此类继承自 QThread，并在后台执行配置比较操作。它会发出信号以通知主线程比较的结果。

    使用 PyQt 的信号-槽机制来进行线程间的通信。
    """
    signal = pyqtSignal(int)

    def __init__(self, table, filter_bar, label_status):
        """
        初始化配置比较器线程。

        :param table: 表格对象，用于显示比较结果。
        :type table: QTableWidget
        :param filter_bar: 过滤栏对象，用于设置过滤条件。
        :type filter_bar: FilterBar
        :param label_status: 状态标签，用于展示状态信息。
        :type label_status: QLabel
        """
        super().__init__()

        self.table = table
        self.filter = filter_bar
        self.label_status = label_status

    def run(self) -> None:
        """
        执行配置比较的主要逻辑。

        此方法在线程启动时被调用。它处理配置数据的获取、比较，并将结果通过信号发送。
        """
        try:
            self.initialize()

            result = self.process_data()
            if result is not None:
                self.signal.emit(result)
                return

            self.finalize()

            self.signal.emit(0)

        except Exception:
            logger.exception(f'{e}')
            self.signal.emit(-1)

    def initialize(self):
        """
        初始化所需配置。

        此方法负责清空表格数据，禁用排序，并加载配置信息。
        """
        # 清空表格数据
        self.table.clear()
        # 禁用表格排序，防止展示空数据
        self.table.setSortingEnabled(False)
        # 加载配置信息
        self.config_main, self.config_connection = config_init()

    def process_data(self) -> Optional[int]:
        """
        处理并比较配置数据。

        此方法执行数据查询、比较和处理。根据比较结果返回不同的状态码。

        :return: 操作结果状态码。
        :rtype: Optional[int]
        """
        # 开始查询数据库
        result_dict = start_query(self.config_connection, self.config_main)
        if not result_dict:
            return 1

        # 根据各配置环境的值，得到一致性信息，加入到配置字典
        result_update_duplicate = start_update_duplicate(result_dict)
        if not result_update_duplicate:
            return 2

        # 通过对比过滤列表，得到是否过滤信息，加入到配置字典
        result_update_filter = start_update_filter(result_update_duplicate)
        if not result_update_filter:
            return 3

        # 将最后得到的字典插入表格中
        for one_row in result_update_filter.values():
            row = [one_row['app_id'], one_row['namespace_name'], one_row['key'],
                   one_row.get('PRO_CONFIG'), one_row.get('PRE_CONFIG'), one_row.get('TEST_CONFIG'), one_row.get('DEV_CONFIG'),
                   one_row['equal'], one_row['filter']]
            self.table.add_row(row)
        return

    def finalize(self) -> None:
        """
        完成配置比较后的收尾工作。

        此方法执行比较后的清理工作，如启用表格排序、更新过滤器等。
        """
        # 启动排序
        self.table.setSortingEnabled(True)
        # 默认按第一列升序排序
        self.table.sortByColumn(0, Qt.AscendingOrder)
        # 更新过滤器，过滤服务中插入值
        self.filter.filter_options_add()
        # 运行过滤器
        self.filter.filter_table()
