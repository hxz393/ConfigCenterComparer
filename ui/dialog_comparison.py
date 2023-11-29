"""
此模块用于创建和管理对话框界面，主要包括 DialogComparison 类。

DialogComparison 类提供了一个对话框界面，用于展示不同环境下配置项的比较结果。类中包含多个方法，用于初始化界面、更新语言设置、创建标签页和表格，并处理表格数据。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, List, Optional

from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QDialog, QHBoxLayout, QLabel, QFrame, QLineEdit, QSizePolicy, QPushButton, QMenu

from config.settings import COLOR_SKIP
from lib.get_resource_path import get_resource_path
from ui.lang_manager import LangManager
from ui.config_manager import ConfigManager
from ui.action_save import ActionSave
from ui.action_copy import ActionCopy

logger = logging.getLogger(__name__)


class DialogComparison(QDialog):
    """
    对话框类，用于展示不同环境下配置的自我比较结果。

    :param lang_manager: 语言管理器实例，用于处理语言相关设置。
    :type lang_manager: LangManager
    :param config_manager: 配置管理器实例，用于管理配置。
    :type config_manager: ConfigManager
    :param data: 包含环境配置比较结果的字典。
    :type data: Dict[str, Dict[str, List[Dict[str, str]]]]
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager,
                 data: Dict[str, Dict[str, List[Dict[str, str]]]]):
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.lang = self.lang_manager.get_lang()
        self.data = data

        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面组件。

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 运行语言配置和设置窗口
            self.setWindowIcon(QIcon(get_resource_path('media/icons8-diff-files-26.png')))
            self.setMinimumSize(1000, 480)
            self.setStyleSheet("font-size: 14px;")
            # 设置主布局
            self.layout = QVBoxLayout(self)
            self.layout.setContentsMargins(0, 0, 0, 0)
            # 创建过滤栏
            filter_bar = self._create_filter_bar()
            self.layout.addWidget(filter_bar)
            # 加入横向分割线
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            self.layout.addWidget(separator)
            # 运行语言配置，创建表格要用到
            self.update_lang()
            # 创建标签页
            tab_widget = QTabWidget()
            self.layout.addWidget(tab_widget)
            for env in self.env_keys:
                tab_widget.addTab(self._create_tab(env), env)
        except Exception:
            logger.exception("Failed to initialize DialogComparison UI components")
            self.status_updated.emit(self.lang['label_status_error'])

    def _create_filter_bar(self) -> QWidget:
        """
        创建过滤栏组件。包含公共配置标记和搜索功能。

        :rtype: QWidget
        :return: 返回过滤栏组件。
        """
        # 建立横向过滤器布局
        filter_bar = QWidget()
        layout = QHBoxLayout(filter_bar)
        layout.setContentsMargins(10, 10, 10, 0)
        filter_bar.setLayout(layout)

        # 建立标签，加入布局
        self.public_label = QLabel()
        layout.addWidget(self.public_label)
        # 设置输入框
        self.public_box = QLineEdit()
        self.public_box.returnPressed.connect(self.set_public)
        self.public_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.public_box.setMinimumWidth(100)
        self.public_box.setMaximumWidth(200)
        layout.addWidget(self.public_box)
        # 设置按钮
        self.public_button = QPushButton()
        self.public_button.clicked.connect(self.set_public)
        layout.addWidget(self.public_button)

        # 加入分割线
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Raised)
        layout.addWidget(separator)

        # 建立标签，加入布局
        self.search_label = QLabel()
        layout.addWidget(self.search_label)
        # 设置输入框
        self.search_box = QLineEdit()
        self.search_box.returnPressed.connect(self.search_value)
        self.search_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.search_box.setMinimumWidth(100)
        layout.addWidget(self.search_box)
        # 设置按钮
        self.search_button = QPushButton()
        self.search_button.clicked.connect(self.search_value)
        layout.addWidget(self.search_button)

        return filter_bar

    def _create_tab(self, env: str) -> QWidget:
        """
        创建一个标签页。

        :param env: 环境名。
        :type env: str

        :rtype: QWidget
        :return: 返回标签页。
        """
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        table = self._create_table(self.data.get(env, {}))
        tab_layout.addWidget(table)

        # 为每个 table 实例化 ActionCopy 和 ActionSave
        table.actionCopy = ActionCopy(self.lang_manager, table)
        table.actionCopy.status_updated.connect(self.forward_status)
        table.actionSave = ActionSave(self.lang_manager, table)
        table.actionSave.status_updated.connect(self.forward_status)
        # 为每个 table 创建右键菜单
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self._cell_context_menu)

        return tab

    def _cell_context_menu(self, pos: QPoint) -> None:
        """
        实现表格单元格的右键菜单功能。

        :param pos: 右键点击的位置。
        :type pos: QPoint

        :rtype: None
        :return: 无返回值。
        """
        sender = self.sender()
        # 确定sender是QTableWidget，且拥有actionCopy和actionSave属性
        if isinstance(sender, QTableWidget):
            if hasattr(sender, 'actionCopy') and hasattr(sender, 'actionSave'):
                copy = getattr(sender, 'actionCopy')
                save = getattr(sender, 'actionSave')
                menu = QMenu(sender)
                menu.addAction(copy.action_copy)
                menu.addAction(save.action_save)
                menu.exec_(sender.viewport().mapToGlobal(pos))

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.setWindowTitle(self.lang['ui.dialog_comparison_1'])
        # 更新标签页
        self.env_keys = [
            self.lang['ui.dialog_settings_connection_2'],
            self.lang['ui.dialog_settings_connection_3'],
            self.lang['ui.dialog_settings_connection_4'],
            self.lang['ui.dialog_settings_connection_5']
        ]
        self._update_tab_titles(self.env_keys)
        # 更新表头
        self.column_headers = [
            self.lang['ui.table_main_1'],
            self.lang['ui.table_main_2'],
            self.lang['ui.table_main_3'],
            self.lang['ui.action_compare_3'],
        ]
        self._update_all_table_headers(self.column_headers)
        # 更新其他文字
        self.public_label.setText(self.lang['ui.dialog_comparison_2'])
        self.public_button.setText(self.lang['ui.dialog_comparison_3'])
        self.public_box.setToolTip(self.lang['ui.dialog_comparison_5'])
        self.search_label.setText(self.lang['ui.dialog_comparison_4'])
        self.search_button.setText(self.lang['ui.filter_bar_9'])
        self.search_box.setToolTip(self.lang['ui.dialog_comparison_6'])

    def _update_tab_titles(self, new_titles: List[str]) -> None:
        """
        更新标签页标题。

        :param new_titles: 包含新标题的列表。
        :type new_titles: List[str]

        :rtype: None
        :return: 无返回值。
        """
        tab_widget = self.findChild(QTabWidget)
        # 确定标签页存在，且标签数量与新标题数量相等
        if tab_widget is not None and len(new_titles) == tab_widget.count():
            for index, title in enumerate(new_titles):
                tab_widget.setTabText(index, title)

    def _update_all_table_headers(self, new_headers: List[str]) -> None:
        """
        更新所有标签页中表格的表头。

        :param new_headers: 包含新表头的列表。
        :type new_headers: List[str]

        :rtype: None
        :return: 无返回值。
        """
        tab_widget = self.findChild(QTabWidget)
        if tab_widget is None:
            return
        # 循环设置每个标签页中的表格表头
        for i in range(tab_widget.count()):
            table = tab_widget.widget(i).findChild(QTableWidget)
            for j, header in enumerate(new_headers):
                table.setHorizontalHeaderItem(j, QTableWidgetItem(header))

    def _create_table(self, items: Dict[str, List[Dict[str, str]]]) -> QTableWidget:
        """
        建立表格并插入数据。

        :param items: 包含单个环境配置比较结果。
        :type items: List[Dict[str, str]]]

        :rtype: QTableWidget
        :return: 返回建好的表格组件。
        """
        table = QTableWidget()
        # 配置表格基本属性
        table.setColumnCount(len(self.column_headers))
        table.setHorizontalHeaderLabels(self.column_headers)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectItems)
        table.setTextElideMode(Qt.ElideNone)
        table.horizontalHeader().setMinimumSectionSize(220)

        # 向表格插入数据。先计算总行数，禁用更新，优化性能。
        table.setUpdatesEnabled(False)
        table.setRowCount(sum(len(group) for group in items.values()))
        self._insert_data_to_table(table, items)
        table.setUpdatesEnabled(True)

        return table

    def _insert_data_to_table(self,
                              table: QTableWidget,
                              items: Dict[str, List[Dict[str, str]]]) -> None:
        """
        向表格插入特定格式的数据。

        :param table: 展示结果表格。
        :type table: QTableWidget
        :param items: 包含单个环境配置比较结果。
        :type items: Dict[str, List[Dict[str, str]]]

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 如果没数据，直接返回
            if not items:
                return

            # 两种颜色：白色和灰色
            color_palette = [Qt.white, QColor(COLOR_SKIP)]
            # 开始行数
            row_count = 0

            # 索引键不需要，直接获取对结果分好组的列表
            for group_number, item_group in enumerate(items.values(), start=1):
                # 要单元格设置的背景颜色
                group_color = color_palette[group_number % len(color_palette)]
                # 对包含多组配置字典的列表进行处理
                for item_index, item in enumerate(item_group, start=1):
                    # 为每行设置组号
                    table.setVerticalHeaderItem(row_count, QTableWidgetItem(f"{group_number}.{item_index}"))
                    # 对表头处理，col_index为列号，key为列标题
                    for col_index, key in enumerate(self.column_headers):
                        # 避免 KeyError
                        value = item.get(key, "")
                        # 设置单元格数据
                        table_item = QTableWidgetItem(str(value))
                        # 为单元格设置背景颜色
                        table_item.setBackground(group_color)
                        # 通过行号、列号和数据信息插入到表格
                        table.setItem(row_count, col_index, table_item)
                    # 插入完一行后，行号加一
                    row_count += 1
        except Exception:
            logger.exception("Failed to insert data into table")
            self.status_updated.emit(self.lang['label_status_error'])

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :type message: str

        :rtype: None
        :return: 无返回值。
        """
        self.status_updated.emit(message)

    def _get_current_table(self) -> Optional[QTableWidget]:
        """
        获取当前选中标签页中的表格。

        :rtype: Optional[QTableWidget]
        :return: 返回当前选中标签页中的 QTableWidget 实例。没获取到则返回 None。
        """
        tab_widget = self.findChild(QTabWidget)
        if tab_widget is None:
            return None

        current_tab = tab_widget.currentWidget()
        if current_tab is None:
            return None

        table = current_tab.findChild(QTableWidget)
        return table

    def set_public(self) -> None:
        """
        根据用户输入公共配置的名称，设置表格中对应行的字体颜色。

        :rtype: None
        :return: 无返回值。
        """
        # 如果关闭颜色设置，直接返回。
        color_switch = self.config_manager.get_config_main().get('color_set', 'ON')
        if color_switch == 'OFF':
            return

        # 获取输入值和表格。表格为空则返回。
        public_value = self.public_box.text().strip()
        table = self._get_current_table()
        if table is None:
            return

        # 无论输入值是否为空，都先重置表格字体颜色
        self._reset_table_font_color(table)

        # 输入值为空，直接返回。
        if not public_value:
            return

        # 遍历表格设置匹配行的字体颜色
        for row in range(table.rowCount()):
            cell_item = table.item(row, 0)
            if cell_item and public_value == cell_item.text():
                self._set_row_font_color(table, row, Qt.red)

    @staticmethod
    def _set_row_font_color(table: QTableWidget,
                            row: int,
                            color: str) -> None:
        """
        设置特定行的字体颜色。

        :param table: 要操作的表格对象。
        :type table: QTableWidget
        :param row: 行号。
        :type row: int
        :param color: 字体颜色。
        :type color: str

        :rtype: None
        :return: 无返回值。
        """
        for column in range(table.columnCount()):
            cell_item = table.item(row, column)
            if cell_item:
                cell_item.setForeground(QColor(color))

    @staticmethod
    def _reset_table_font_color(table: QTableWidget) -> None:
        """
        重置表格所有单元格的字体颜色为黑色。

        :param table: 要操作的表格对象。
        :type table: QTableWidget

        :rtype: None
        :return: 无返回值。
        """
        for row in range(table.rowCount()):
            for column in range(table.columnCount()):
                cell_item = table.item(row, column)
                if cell_item:
                    cell_item.setForeground(Qt.black)

    def search_value(self) -> None:
        """
        根据用户输入的搜索字段，去表格中所有配置键和配置值中去搜索匹配。

        :rtype: None
        :return: 无返回值。
        """
        # 获取用户输入的搜索文本和表格。
        search_text = self.search_box.text().strip().lower()
        table = self._get_current_table()

        # 如果没有找到表格，直接返回
        if table is None:
            return

        # 如果输入框为空，重置所有行为可见
        if not search_text:
            self._reset_row_hidden_status(table)
            return

        # 逐行匹配搜索值
        for row in range(table.rowCount()):
            self._search_process(table, row, search_text)

    @staticmethod
    def _search_process(table: QTableWidget,
                        row: int,
                        search_text: str) -> None:
        """
        作用于单行，根据搜索文本设置可见性。

        :param table: 表格对象。
        :type table: QTableWidget
        :param row: 当前行号。
        :type row: int
        :param search_text: 搜索文本。
        :type search_text: str

        :rtype: None
        :return: 无返回值。
        """
        # 变量和实际显示匹配。先设为False为不显示
        row_contains_search_text = False
        # 只搜索键和值列
        for column in [2, 3]:
            # 获取单元格文本，并小写化，匹配搜索文本，让搜索不区分大小写
            cell_text = table.item(row, column).text().lower()
            # 找到匹配项，跳出内层循环
            if search_text in cell_text:
                row_contains_search_text = True
                break

        table.setRowHidden(row, not row_contains_search_text)

    @staticmethod
    def _reset_row_hidden_status(table: QTableWidget) -> None:
        """
        重置表格行的隐藏状态。

        :param table: 表格对象。
        :type table: QTableWidget

        :rtype: None
        :return: 无返回值。
        """
        if table is not None:
            for row in range(table.rowCount()):
                table.setRowHidden(row, False)
