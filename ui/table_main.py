"""
这是一个用于处理配置中心比较结果的Python模块，主要用于管理和展示配置中心数据的表格界面。

此模块定义了`TableMain`类，用于创建和管理配置中心比较结果的表格界面。它提供了丰富的功能，包括表格初始化、行列管理、右键菜单功能、以及颜色应用等。

此类的主要目的是提供一个交互式且用户友好的界面，用于展示和操作配置中心的数据比较结果。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import List, Union, Any, Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction, QHeaderView

from ConfigCenterComparer import ConfigCenterComparer
from config.settings import COL_INFO, COLOR_SKIP, COLOR_CONSISTENCY_FULLY, COLOR_CONSISTENCY_PARTIALLY, COLOR_DEFAULT, COLOR_EMPTY

logger = logging.getLogger(__name__)


class TableMain(QTableWidget):
    """
    创建和管理配置中心比较结果的表格界面。

    此类封装了配置中心数据比较结果表格的创建和管理逻辑，包括表格的初始化、行列的管理、右键菜单的功能实现，以及颜色的应用等。

    :param main_window: 配置中心比较器的主窗口对象。
    :type main_window: ConfigCenterComparer
    :param parent: 此表格的父对象。
    :type parent: QWidget, optional
    """

    def __init__(self, main_window: ConfigCenterComparer, parent=None):
        """
        初始化 `TableMain` 类的实例。

        此方法用于设置表格的初始配置，包括与主窗口的连接、状态标签、语言设置、列头配置、隐藏列和调整列的设置等。

        :param main_window: 配置中心比较器的主窗口对象，用于与主界面交互。
        :type main_window: ConfigCenterComparer
        :param parent: 此表格的父窗口对象，用于Qt的窗口继承和管理。
        :type parent: QWidget, optional
        """
        super().__init__(parent)

        self.main_window = main_window
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')

        self.column_headers = [
            self.lang['ui.table_main_1'],
            self.lang['ui.table_main_2'],
            self.lang['ui.table_main_3'],
            self.lang['ui.dialog_settings_connection_2'],
            f"{self.lang['ui.dialog_settings_connection_2']} {self.lang['ui.table_main_4']}",
            self.lang['ui.dialog_settings_connection_3'],
            f"{self.lang['ui.dialog_settings_connection_3']} {self.lang['ui.table_main_4']}",
            self.lang['ui.dialog_settings_connection_4'],
            f"{self.lang['ui.dialog_settings_connection_4']} {self.lang['ui.table_main_4']}",
            self.lang['ui.dialog_settings_connection_5'],
            f"{self.lang['ui.dialog_settings_connection_5']} {self.lang['ui.table_main_4']}",
            self.lang['ui.table_main_5'],
            self.lang['ui.table_main_6'],
        ]
        self.hidden_cols = ["pro_time", "pre_time", "test_time", "dev_time"]
        self.resize_cols = ["name", "group", "consistency", "skip"]

        self._setup_table()

    def _setup_table(self) -> None:
        """
        配置表格的基本属性和行为。

        此方法用于初始化表格的列数、表头、选择行为、上下文菜单等基本属性和行为。
        """
        try:
            # 配置表格基本属性
            self.setColumnCount(len(self.column_headers))
            self.setHorizontalHeaderLabels(self.column_headers)
            self.setEditTriggers(QTableWidget.NoEditTriggers)
            self.setSelectionBehavior(QTableWidget.SelectItems)
            # 隐藏垂直表头
            # self.verticalHeader().setVisible(False)
            # 启用自动换行，没生效
            self.setWordWrap(True)
            self.setTextElideMode(Qt.ElideNone)

            # 为表头视图设置上下文菜单事件
            self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
            self.horizontalHeader().customContextMenuRequested.connect(self._header_context_menu)
            # 为表单设置上下文菜单事件
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self._cell_context_menu)

            # 隐藏指定列
            [self.hideColumn(COL_INFO[i]['col']) for i in self.hidden_cols]
            # 初始化列宽
            self.set_header_resize()
        except Exception:
            logger.exception("Error occurred while setting up the table")

    def set_header_resize(self) -> None:
        """
        设置表头的默认列宽和列宽调整策略。

        此方法用于设置表格的列宽调整策略和默认列宽，以提供更好的用户体验。
        """
        try:
            # 设置默认列宽度，列宽调整策略，列可拖动
            self.horizontalHeader().setSectionsMovable(True)
            self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.horizontalHeader().setMinimumSectionSize(100)
            # 设置要自动调整宽度的列
            [self.horizontalHeader().setSectionResizeMode(COL_INFO[i]['col'], QHeaderView.ResizeToContents) for i in self.resize_cols]
        except Exception:
            logger.exception("Error occurred while resizing table headers")
            self.label_status.setText(self.lang['label_status_error'])

    def keyPressEvent(self, event) -> None:
        """
        处理键盘事件。

        此方法用于处理键盘事件，特别是复制功能的快捷键。如果按下 Ctrl+C，则复制选中的单元格内容。

        :param event: 键盘事件对象。
        :type event: QKeyEvent
        """
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.main_window.ActionCopy.copy_selected()
        else:
            super().keyPressEvent(event)

    def _cell_context_menu(self, pos: QPoint) -> None:
        """
        实现表格单元格的右键菜单功能。

        :param pos: 右键点击的位置。
        :type pos: QPoint
        """
        menu = QMenu(self)
        menu.addAction(self.main_window.ActionCopy.action_copy)
        separator = QAction(menu)
        separator.setSeparator(True)
        menu.addAction(separator)
        menu.addAction(self.main_window.ActionSkip.action_skip)
        menu.addAction(self.main_window.ActionUnskip.action_unskip)
        sep = QAction(menu)
        sep.setSeparator(True)
        menu.addAction(sep)
        menu.addAction(self.main_window.ActionSave.action_save)
        menu.exec_(self.viewport().mapToGlobal(pos))

    def _header_context_menu(self, pos: QPoint) -> None:
        """
        实现表头的右键菜单功能。

        :param pos: 右键点击的位置。
        :type pos: QPoint
        """
        menu = QMenu(self)
        # 动态创建一个菜单项，用于隐藏/显示列
        for index in range(self.columnCount()):
            column_name = self.horizontalHeaderItem(index).text()
            action = menu.addAction(f"{column_name}")
            action.setCheckable(True)
            action.setChecked(not self.isColumnHidden(index))
            action.setData(index)
            action.triggered.connect(self._toggle_column_visibility)
        # 在鼠标右键点击位置显示菜单
        menu.exec_(self.horizontalHeader().viewport().mapToGlobal(pos))

    def _toggle_column_visibility(self) -> None:
        """
        根据用户选择，切换列的可见性。

        此方法用于根据用户在上下文菜单中的选择，显示或隐藏特定的列。
        """
        action = self.sender()
        if isinstance(action, QAction):
            column_index = action.data()
            if action.isChecked():
                self.showColumn(column_index)
            else:
                self.hideColumn(column_index)

    def add_row(self, data: List[List[Union[str, Any]]]) -> None:
        """
        向表格中添加一行数据。

        :param data: 要添加的数据列表，每个元素代表一列的数据。
        :type data: List[str]
        """
        row_position = 0
        try:
            # 获取最后行数
            row_position = self.rowCount()
            # 插入最后一行
            self.insertRow(row_position)
            # 插入单元格数据
            for column, item_data in enumerate(data):
                # 默认设置显示字符串，也叫 Qt.DisplayRole。获取方法item.text() 或 item.data(Qt.DisplayRole)，设置方法
                item = QTableWidgetItem(str(item_data[0]))
                # 设置实际数据，也叫 Qt.UserRole。获取方法 item.data(Qt.UserRole)
                item.setData(Qt.UserRole, item_data[1])
                # 设置单元格不可编辑状态
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                # 正常表格插入方法
                self.setItem(row_position, column, item)
        except Exception:
            logger.exception("Error occurred while adding a new row")
            self.removeRow(row_position)

    def apply_color_to_table(self, rows: List[int]) -> None:
        """
        根据一致性和跳过状态给表格行应用颜色。

        :param rows: 要应用颜色的行号列表。
        :type rows: List[int]
        """
        check_none_value_column_list = [
            COL_INFO['pro_value']['col'],
            COL_INFO['pre_value']['col'],
            COL_INFO['test_value']['col'],
            COL_INFO['dev_value']['col'],
        ]
        try:
            for row in rows:
                consistency_data = self.item(row, COL_INFO['consistency']['col']).data(Qt.UserRole)
                skip_data = self.item(row, COL_INFO['skip']['col']).data(Qt.UserRole)

                # 忽略状态为是时设置颜色
                if skip_data == 'yes':
                    self.apply_color(row, COLOR_SKIP)
                    continue

                # 根据一致性值设置颜色
                if consistency_data == 'fully':
                    self.apply_color(row, COLOR_CONSISTENCY_FULLY)
                elif consistency_data == 'partially':
                    self.apply_color(row, COLOR_CONSISTENCY_PARTIALLY)
                else:
                    self.apply_color(row, COLOR_DEFAULT)

                # 遍历指定列检查空值
                for column in check_none_value_column_list:
                    if self.item(row, column).text() == 'None':
                        self.apply_color(row, COLOR_EMPTY, column)
        except Exception:
            logger.exception("Exception in apply_color_to_table method")
            self.label_status.setText(self.lang['label_status_error'])

    def apply_color(self, row: int, color: str, column: Optional[int] = None) -> None:
        """
        为指定的行或单元格应用颜色。

        :param row: 要着色的行索引。
        :type row: int
        :param color: 要应用的颜色。
        :type color: str
        :param column: 可选，指定要着色的列索引，如果未指定，则对整行应用颜色。
        :type column: int, optional
        """
        try:
            if column is not None:
                self._apply_color_to_cell(row, color, column)
            else:
                for col in range(self.columnCount()):
                    self._apply_color_to_cell(row, color, col)
        except Exception:
            logger.exception("Error occurred while applying color to a cell")
            self.label_status.setText(self.lang['label_status_error'])

    def _apply_color_to_cell(self, row: int, color: str, column: int) -> None:
        """
        为特定单元格应用颜色。

        此方法用于给指定行和列的单元格应用背景色。

        :param row: 行索引。
        :type row: int
        :param column: 列索引。
        :type column: int
        :param color: 要应用的颜色。
        :type color: str
        """
        if color:
            color_brush = QBrush(QColor(color))
            self.item(row, column).setBackground(color_brush)

    def clear(self) -> None:
        """
        清空表格中的所有行。

        此方法用于清除表格中的所有数据，通常在数据更新或重置时使用。
        """
        try:
            # 禁用更新以提高性能
            self.setUpdatesEnabled(False)
            # 首先清除所有单元格的内容
            self.clearContents()
            # 接着删除所有行
            while self.rowCount() > 0:
                self.removeRow(0)
            # 重新启用更新
            self.setUpdatesEnabled(True)
        except Exception as e:
            logger.exception("Error occurred while clearing the table: {}".format(str(e)))
            self.label_status.setText(self.lang['label_status_error'])
            # 确保即使发生错误也要重新启用更新
            self.setUpdatesEnabled(True)
