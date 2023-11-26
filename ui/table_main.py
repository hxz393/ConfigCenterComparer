"""
此文件定义了 TableMain 类，一个基于 PyQt5 的 QTableWidget 的高级实现。

TableMain 类主要用于显示和管理表格数据，提供了多种扩展功能，包括语言国际化支持、动态配置管理、右键菜单操作等。
该类与多个辅助类（如 LangManager 和 ConfigManager）集成，实现了复杂的功能逻辑。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import List, Union, Optional, Dict

from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QKeyEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMenu, QAction, QHeaderView

from config.settings import COL_INFO, COLOR_SKIP, COLOR_CONSISTENCY_FULLY, COLOR_CONSISTENCY_PARTIALLY, COLOR_EMPTY
from lib.log_time import log_time
from ui.action_copy import ActionCopy
from ui.action_save import ActionSave
from ui.action_skip import ActionSkip
from ui.action_unskip import ActionUnskip
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class TableMain(QTableWidget):
    """
    主表格类，用于展示和管理数据行。

    此类继承自 PyQt5 的 QTableWidget，提供了丰富的数据展示和管理功能。包括但不限于数据的展示、行的颜色标记、右键菜单功能以及快捷键支持。
    通过与 LangManager 和 ConfigManager 的集成，支持动态语言切换和配置管理。

    :param lang_manager: 用于管理界面语言的 LangManager 实例。
    :type lang_manager: LangManager
    :param config_manager: 用于管理配置的 ConfigManager 实例。
    :type config_manager: ConfigManager

    :author: assassing
    :contact: https://github.com/hxz393
    :copyright: Copyright 2023, hxz393. 保留所有权利。
    """
    status_updated = pyqtSignal(str)
    filter_updated = pyqtSignal(list)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        # 实例化用到的组件
        self.actionCopy = ActionCopy(self.lang_manager, self)
        self.actionSave = ActionSave(self.lang_manager, self)
        self.actionSkip = ActionSkip(self.lang_manager, self.config_manager, self)
        self.actionUnskip = ActionUnskip(self.lang_manager, self.config_manager, self)
        # 手动连接实例化的组件信号到转发函数
        self.actionCopy.status_updated.connect(self.forward_status)
        self.actionSave.status_updated.connect(self.forward_status)
        self.actionSkip.status_updated.connect(self.forward_status)
        self.actionSkip.filter_updated.connect(self.forward_filter)
        self.actionSkip.color_updated.connect(self.apply_color_to_table)
        self.actionUnskip.status_updated.connect(self.forward_status)
        self.actionUnskip.filter_updated.connect(self.forward_filter)
        self.actionUnskip.color_updated.connect(self.apply_color_to_table)
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面。

        此方法负责设置表格的基本属性，如列数、表头标签、选择行为等。还包括对特定列的隐藏和宽度调整策略的设置。

        :rtype: None
        :return: 无返回值。
        """
        # 先运行语言更新，里面有表头定义
        self.update_lang()
        self.hidden_cols = ["pro_time", "pre_time", "test_time", "dev_time"]
        self.resize_cols = ["name", "group", "consistency", "skip"]
        # 配置表格基本属性
        self.setColumnCount(len(self.column_headers))
        self.setHorizontalHeaderLabels(self.column_headers)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectItems)
        # 隐藏垂直表头
        self.verticalHeader().setVisible(False)
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
        # 设置表宽度策略
        self.set_header_resize()

    def set_header_resize(self):
        """
        设置表头的列宽度和调整策略。

        此方法负责定义表头列的宽度调整策略和其他相关属性。它设置了表头列的默认宽度、是否可拖动以及列的自动调整策略。
        例如，某些列被设置为根据内容自动调整宽度，而其他列则被设置为可伸缩以适应表格的大小。

        :rtype: None
        :return: 无返回值。
        """
        # 设置默认列宽度，列宽调整策略，列可拖动
        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setMinimumSectionSize(100)
        # 设置要自动调整宽度的列
        [self.horizontalHeader().setSectionResizeMode(COL_INFO[i]['col'], QHeaderView.ResizeToContents) for i in self.resize_cols]

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
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
        # 重新应用到表头
        self.setHorizontalHeaderLabels(self.column_headers)
        # 定义数据和显示映射的字典
        consistency_status_mapping = {
            "inconsistent": self.lang['ui.action_start_8'],
            "fully": self.lang['ui.action_start_9'],
            "partially": self.lang['ui.action_start_10'],
            "unknown": self.lang['ui.action_start_13'],
        }
        skip_status_mapping = {
            "no": self.lang['ui.action_start_11'],
            "yes": self.lang['ui.action_start_12'],
            "unknown": self.lang['ui.action_start_13'],
        }
        for row in range(self.rowCount()):
            # 更新忽略状态文字
            self._update_item_text(row, "skip", skip_status_mapping)
            # 更新一致性状态文字
            self._update_item_text(row, "consistency", consistency_status_mapping)

    def _update_item_text(self,
                          row: int,
                          user_data_key: str,
                          text_mapping: Dict[str, str]) -> None:
        """
        根据提供的文本映射更新指定行的项文本。

        此方法用于更新表格或列表中特定行的文本。它根据用户数据键（user_data_key）获取对应行的项，然后根据提供的文本映射（text_mapping）更新该项的文本。

        :param row: 要更新的行索引。
        :type row: int
        :param user_data_key: 用于获取项的用户数据键。
        :type user_data_key: str
        :param text_mapping: 用户数据到文本的映射字典。
        :type text_mapping: Dict[str, str]

        :return: 无返回值。
        :rtype: None
        """
        item = self.item(row, COL_INFO[user_data_key]['col'])
        if item is not None:
            user_data = item.data(Qt.UserRole)
            if user_data in text_mapping:
                item.setText(text_mapping[user_data])

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        处理键盘事件。

        此方法用于处理键盘事件，特别是复制功能的快捷键。如果按下 Ctrl+C，则复制选中的单元格内容。

        :param event: 键盘事件对象。
        :type event: QKeyEvent

        :rtype: None
        :return: 无返回值。
        """
        if event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            self.actionCopy.action_copy()
        else:
            super().keyPressEvent(event)

    def _cell_context_menu(self, pos: QPoint) -> None:
        """
        实现表格单元格的右键菜单功能。

        :param pos: 右键点击的位置。
        :type pos: QPoint

        :rtype: None
        :return: 无返回值。
        """
        menu = QMenu(self)
        menu.addAction(self.actionCopy.action_copy)
        separator = QAction(menu)
        separator.setSeparator(True)
        menu.addAction(separator)
        menu.addAction(self.actionSkip.action_skip)
        menu.addAction(self.actionUnskip.action_unskip)
        sep = QAction(menu)
        sep.setSeparator(True)
        menu.addAction(sep)
        menu.addAction(self.actionSave.action_save)
        menu.exec_(self.viewport().mapToGlobal(pos))

    def _header_context_menu(self, pos: QPoint) -> None:
        """
        实现表头的右键菜单功能。

        :param pos: 右键点击的位置。
        :type pos: QPoint

        :rtype: None
        :return: 无返回值。
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

        :rtype: None
        :return: 无返回值。
        """
        action = self.sender()
        if isinstance(action, QAction):
            column_index = action.data()
            if action.isChecked():
                self.showColumn(column_index)
            else:
                self.hideColumn(column_index)

    def add_row(self, data: List[List[str]]) -> None:
        """
        向表格中添加一行数据。

        :param data: 要添加的数据列表，每个元素是一个列表，第一个元素代表显示的字符串，第二个元素代表附加数据。
        :type data: List[List[str]]

        :rtype: None
        :return: 无返回值。
        """
        row_position = 0
        try:
            # 获取最后行数
            row_position = self.rowCount()
            # 插入最后一行
            self.insertRow(row_position)
            # 插入单元格数据
            self._fill_row_data(row_position, data)
        except Exception:
            logger.exception(f"Error occurred while adding a new row at position {row_position}")
            self.removeRow(row_position)

    def _fill_row_data(self,
                       row_position: int,
                       data: List[List[str]]) -> None:
        """
        填充指定行的数据。

        :param row_position: 行位置
        :param data: 行数据
        :type row_position: int
        :type data: List[List[str]]

        :rtype: None
        :return: 无返回值。
        """
        for column, (display_text, user_data) in enumerate(data):
            # 默认设置显示字符串，也叫 Qt.DisplayRole。获取方法item.text() 或 item.data(Qt.DisplayRole)
            item = QTableWidgetItem(str(display_text))
            # 设置实际数据，也叫 Qt.UserRole。获取方法 item.data(Qt.UserRole)
            item.setData(Qt.UserRole, user_data)
            # 设置单元格不可编辑状态
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            # 正常表格插入方法
            self.setItem(row_position, column, item)

    @log_time
    def apply_color_to_table(self,
                             rows: Optional[List[int]],
                             config_connection: Dict[str, Dict[str, Union[Dict[str, str], bool]]]) -> None:
        """
        根据一致性和跳过状态给表格行应用颜色。

        :param config_connection: 数据库连接配置字典。
        :type config_connection: Dict[str, Dict[str, Union[Dict[str, str], bool]]]
        :param rows: 要应用颜色的行号列表。
        :type rows: Optional[List[int]]

        :rtype: None
        :return: 无返回值。
        """
        environments = ['PRO', 'PRE', 'TEST', 'DEV']
        try:
            check_none_value_column_status = {
                COL_INFO[f'{env.lower()}_value']['col']: config_connection[f'{env}_CONFIG']['mysql_on']
                for env in environments
            }
            check_none_value_column_list = [column for column, status in check_none_value_column_status.items() if status]
            for row in rows if rows and isinstance(rows, list) else range(self.rowCount()):
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

                # 遍历指定列检查空值
                # for column in range(self.columnCount()):
                for column in check_none_value_column_list:
                    if self.item(row, column).text() == 'None':
                        self.apply_color(row, COLOR_EMPTY, column)
        except Exception:
            logger.exception("Exception in apply_color_to_table method")
            self.status_updated.emit(self.lang['label_status_error'])

    def apply_color(self,
                    row: int,
                    color: str,
                    column: Optional[int] = None) -> None:
        """
        为指定的行或单元格应用颜色。

        :param row: 要着色的行索引。
        :type row: int
        :param color: 要应用的颜色。
        :type color: str
        :param column: 可选，指定要着色的列索引，如果未指定，则对整行应用颜色。
        :type column: int, optional

        :rtype: None
        :return: 无返回值。
        """
        try:
            color_brush = QBrush(QColor(color))
            if column:
                self.item(row, column).setBackground(color_brush)
            else:
                for col in range(self.columnCount()):
                    self.item(row, col).setBackground(color_brush)
        except Exception:
            logger.exception("Error occurred while applying color to a cell")
            self.status_updated.emit(self.lang['label_status_error'])

    def clear(self) -> None:
        """
        清空表格中的所有行。

        此方法用于清除表格中的所有数据，通常在数据更新或重置时使用。

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 禁用更新以提高性能
            self.setUpdatesEnabled(False)
            # 首先清除所有单元格的内容
            self.clearContents()
            # 将行数设置为0，从而删除所有行
            self.setRowCount(0)
        except Exception:
            logger.exception("Error occurred while clearing the table.")
            self.status_updated.emit(self.lang['label_status_error'])
        finally:
            # 确保即使发生错误也要重新启用更新
            self.setUpdatesEnabled(True)

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :type message: str

        :rtype: None
        :return: 无返回值。
        """
        self.status_updated.emit(message)

    def forward_filter(self, rows: List[int]) -> None:
        """
        用于转发过滤信号。

        :param rows: 要转发的行列表。
        :type rows: List[int]

        :rtype: None
        :return: 无返回值。
        """
        self.filter_updated.emit(rows)
