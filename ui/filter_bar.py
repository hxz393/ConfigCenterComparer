"""
本模块提供了一个用于过滤和搜索表格数据的用户界面组件。

此组件允许用户通过服务名、表格状态和搜索值来过滤表格中的数据。用户可以选择特定的服务，查看特定状态的行（如完全一致、部分一致或跳过的行），以及根据特定文本搜索行数据。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import List, Optional, Dict

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox, QFrame, QWidget, QSizePolicy, QTableWidget

from config.settings import COL_INFO, COLOR_HIGHLIGHT, COLOR_DEFAULT
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager
from lib.log_time import log_time

logger = logging.getLogger(__name__)


class FilterBar(QWidget):
    """
    过滤栏类，用于在用户界面中提供过滤和搜索功能。

    此类创建了一个包含服务过滤、表格状态过滤和搜索框的组件，使用户能够根据不同条件过滤表格数据。

    :param lang_manager: 语言管理器，用于处理界面语言的更新。
    :type lang_manager: LangManager
    :param config_manager: 配置管理器，用于获取和更新配置信息。
    :type config_manager: ConfigManager
    :param table: 要应用过滤的表格。
    :type table: QTableWidget
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager,
                 table: QTableWidget):
        super().__init__()
        # 实例化组件。
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.lang = self.lang_manager.get_lang()
        self.config_manager = config_manager
        self.table = table
        # 用于还原样式的字典
        self.style_rows = {}
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面。

        创建并布局过滤栏中的所有组件，包括服务过滤、表格状态过滤和搜索值输入框。

        :rtype: None
        :return: 无返回值。
        """
        # 修改字体大小
        self.setStyleSheet("font-size: 14px;")
        # 建立横向主布局
        self.layout = QHBoxLayout(self)
        # 创建过滤服务组件
        self._create_filter_app()
        # 创建过滤列表组件
        self._create_filter_table()
        # 创建搜索过滤值组件
        self._create_filter_value()
        # # 添加弹簧以推动所有小部件靠左
        # self.layout.addItem(QSpacerItem(401, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # 设置布局的内容边距
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        # 重新获取语言字典
        self.lang = self.lang_manager.get_lang()
        # 遍历filter_table下拉框中的所有项
        for index in range(self.filter_table_box.count()):
            # 检查数据值是否匹配
            if self.filter_table_box.itemData(index) == "all":
                # 更新显示值
                self.filter_table_box.setItemText(index, self.lang['ui.filter_bar_3'])
            elif self.filter_table_box.itemData(index) == "fully":
                self.filter_table_box.setItemText(index, self.lang['ui.filter_bar_4'])
            elif self.filter_table_box.itemData(index) == "partially":
                self.filter_table_box.setItemText(index, self.lang['ui.filter_bar_5'])
            elif self.filter_table_box.itemData(index) == "skip":
                self.filter_table_box.setItemText(index, self.lang['ui.filter_bar_6'])
            elif self.filter_table_box.itemData(index) == "fully+skip":
                self.filter_table_box.setItemText(index, f"{self.lang['ui.filter_bar_4']}+{self.lang['ui.filter_bar_6']}")
            elif self.filter_table_box.itemData(index) == "fully+partially":
                self.filter_table_box.setItemText(index, f"{self.lang['ui.filter_bar_4']}+{self.lang['ui.filter_bar_5']}")
            elif self.filter_table_box.itemData(index) == "fully+partially+skip":
                self.filter_table_box.setItemText(index, f"{self.lang['ui.filter_bar_4']}+{self.lang['ui.filter_bar_5']}+{self.lang['ui.filter_bar_6']}")
        # 直接更新服务名过滤默认选项文字
        self.filter_app_box.setItemText(0, self.lang['ui.filter_bar_3'])
        # 更新其他文字
        self.filter_app_label.setText(self.lang['ui.filter_bar_1'])
        self.filter_table_label.setText(self.lang['ui.filter_bar_2'])
        self.filter_table_check_box.setText(self.lang['ui.filter_bar_7'])
        self.filter_value_label.setText(self.lang['ui.filter_bar_8'])
        self.filter_value_button.setText(self.lang['ui.filter_bar_9'])
        self.filter_reset_button.setText(self.lang['ui.filter_bar_10'])

    def _create_filter_app(self) -> None:
        """
        创建服务过滤组件。

        此方法初始化服务过滤下拉框，并设置其事件处理函数。

        :rtype: None
        :return: 无返回值。
        """
        # 建立标签，加入主布局
        self.filter_app_label = QLabel()
        self.layout.addWidget(self.filter_app_label)
        # 过滤服务下拉框
        self.filter_app_box = QComboBox()
        # 设置下拉框的尺寸策略和宽度
        self.filter_app_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # 设置最大宽度，以免拉伸太长
        self.filter_app_box.setMinimumWidth(100)
        self.filter_app_box.setMaximumWidth(300)
        # 设置下拉框的事件处理
        self.filter_app_box.currentIndexChanged.connect(self.filter_table)
        # 设置下拉框的选项，通过函数填充
        self.filter_options_add()
        self.layout.addWidget(self.filter_app_box)
        # 创建一个 QFrame 作为分割线
        self._create_separator()

    def _create_filter_table(self) -> None:
        """
        创建表格状态过滤组件。

        此方法初始化表格状态过滤下拉框和反向选择复选框，并设置它们的事件处理函数。

        :rtype: None
        :return: 无返回值。
        """
        # 建立标签，加入主布局
        self.filter_table_label = QLabel()
        self.layout.addWidget(self.filter_table_label)
        # 过滤列表下拉框
        self.filter_table_box = QComboBox()
        # 设置最小宽度，以免文字放不下
        self.filter_table_box.setMinimumWidth(270)
        # 设置下拉框的选项
        self.filter_table_box.addItem("", "all")
        self.filter_table_box.addItem("", "fully")
        self.filter_table_box.addItem("", "partially")
        self.filter_table_box.addItem("", "skip")
        self.filter_table_box.addItem("", "fully+skip")
        self.filter_table_box.addItem("", "fully+partially")
        self.filter_table_box.addItem("", "fully+partially+skip")
        # 设置下拉框的事件处理
        self.filter_table_box.currentIndexChanged.connect(self.filter_table)
        self.layout.addWidget(self.filter_table_box)
        # 反向选择
        self.filter_table_check_box = QCheckBox()
        self.filter_table_check_box.stateChanged.connect(self.filter_table)
        self.layout.addWidget(self.filter_table_check_box)
        # 创建一个 QFrame 作为分割线
        self._create_separator()

    def _create_filter_value(self) -> None:
        """
        创建搜索过滤组件。

        此方法初始化搜索框和相关按钮，并设置事件处理函数，以便用户可以根据特定文本过滤表格数据。

        :rtype: None
        :return: 无返回值。
        """
        # 建立标签，加入主布局
        self.filter_value_label = QLabel()
        self.layout.addWidget(self.filter_value_label)
        # 搜索输入框
        self.filter_value_box = QLineEdit()
        self.filter_value_box.returnPressed.connect(self.filter_table)
        # 设置下拉框的尺寸策略和最小宽度
        self.filter_value_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filter_value_box.setMinimumWidth(100)
        self.layout.addWidget(self.filter_value_box)
        # 搜索按钮
        self.filter_value_button = QPushButton()
        self.filter_value_button.clicked.connect(self.filter_table)
        self.layout.addWidget(self.filter_value_button)
        # 重置按钮
        self.filter_reset_button = QPushButton()
        self.filter_reset_button.clicked.connect(self.filter_reset)
        self.layout.addWidget(self.filter_reset_button)

    def _create_separator(self) -> None:
        """
        创建界面中的分隔线。

        此方法用于在过滤器工具栏中添加分隔线。

        :rtype: None
        :return: 无返回值。
        """
        # 建好之后，直接加入主布局
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Raised)
        self.layout.addWidget(separator)

    def filter_options_add(self) -> None:
        """
        填充服务过滤下拉框选项。

        此方法从配置数据中提取所有唯一的服务名称，并将它们添加到服务过滤下拉框中。

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 先断开信号
            self.filter_app_box.currentIndexChanged.disconnect(self.filter_table)
            self.filter_app_box.setEnabled(False)
            # 清空过滤器并添加显示所有行的选项
            self.filter_app_box.clear()
            self.filter_app_box.addItem(self.lang['ui.filter_bar_3'], "all")
            self.filter_app_box.setCurrentIndex(0)
            # 使用集合和列表推导式去重并获取所有唯一项
            unique_items = {self.table.item(row, COL_INFO['name']['col']).text()
                            for row in range(self.table.rowCount())
                            if self.table.item(row, COL_INFO['name']['col'])}
            # 添加唯一项到下拉框
            [self.filter_app_box.addItem(item, item) for item in unique_items]
            # 对下拉框进行排序
            model = self.filter_app_box.model()
            model.sort(0)
        except Exception:
            logger.exception("Exception occurred in adding filter options")
            self.status_updated.emit(self.lang['label_status_error'])
        finally:
            # 重新连接信号
            self.filter_app_box.currentIndexChanged.connect(self.filter_table)
            self.filter_app_box.setEnabled(True)

    def filter_reset(self) -> None:
        """
        重置过滤条件。

        此方法将所有过滤组件重置为默认状态，以便用户可以重新开始过滤操作。

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 禁更新
            self.table.setUpdatesEnabled(False)
            # 断开信号连接
            self.filter_app_box.currentIndexChanged.disconnect(self.filter_table)
            self.filter_table_box.currentIndexChanged.disconnect(self.filter_table)
            self.filter_table_check_box.stateChanged.disconnect(self.filter_table)
            # 重置 QComboBox 为第一个项，通常是 "--显示所有--"，
            self.filter_app_box.setCurrentIndex(0)
            self.filter_table_box.setCurrentIndex(0)
            # 还原反选框状态
            self.filter_table_check_box.setChecked(False)
            # 清空搜索框 QLineEdit
            self.filter_value_box.clear()
            # 重置单元格颜色
            self._reset_styles()
            # 手动调用过略器
            self.filter_table()
        except Exception:
            logger.exception("Error occurred while resetting filters")
            self.status_updated.emit(self.lang['label_status_error'])
        finally:
            # 开启更新，重新连接信号
            self.table.setUpdatesEnabled(True)
            self.filter_app_box.currentIndexChanged.connect(self.filter_table)
            self.filter_table_box.currentIndexChanged.connect(self.filter_table)
            self.filter_table_check_box.stateChanged.connect(self.filter_table)

    @log_time
    def filter_table(self, rows: Optional[List[int]] = None) -> None:
        """
        应用过滤条件到表格。带有时间记录用于调试。

        此方法根据用户设置的过滤条件（服务名称、表格状态、搜索文本）来决定哪些行在表格中可见。

        :param rows: 要应用过滤器的行号列表。如果为空则应用到整表。
        :type rows: Optional[List[int]]

        :rtype: None
        :return: 无返回值。
        """
        try:
            # 获取颜色开关
            color_switch = self.config_manager.get_config_main().get('color_set', 'ON')
            # 计算可见的行数
            visible_rows = 0
            # 搜索框输入内容
            search_value = self.filter_value_box.text().strip().lower()
            # 在新的搜索开始之前，恢复每个单元格的原始样式。
            self._reset_styles()
            # 如果没有传入行列表，则应用到整个列表
            for row in rows if rows and isinstance(rows, list) else range(self.table.rowCount()):
                consistency_data = self.table.item(row, COL_INFO['consistency']['col']).data(Qt.UserRole)
                skip_data = self.table.item(row, COL_INFO['skip']['col']).data(Qt.UserRole)
                name_data = self.table.item(row, COL_INFO['name']['col']).text()
                index_key = self._generate_index_key(row)

                # 先匹配快速过滤，匹配过滤条件时为True
                table_match = self._get_table_match(consistency_data, skip_data)
                # 满足快速过滤条件才进行服务名过滤，匹配选择所有或者选择服务名时为True
                app_match = self._get_app_match(name_data) if not table_match else False
                # 满足服务名过滤条件的行才进行搜索，匹配搜索条件或不输入时为True
                search_match = self._get_search_match(row, search_value, index_key, color_switch) if app_match else False

                # 仅当条件都匹配时才显示行
                is_visible = app_match and not table_match and search_match
                self.table.setRowHidden(row, not is_visible)
                visible_rows += 1 if is_visible else 0
            # 更新状态栏信息展示过滤后的行数
            self.status_updated.emit(f"{visible_rows} {self.lang['ui.filter_bar_11']}")
        except Exception:
            logger.exception("Exception in filtering table")
            self.status_updated.emit(self.lang['label_status_error'])

    def _get_app_match(self, name_data: str) -> bool:
        """
        检查当前行是否与选定的应用服务匹配。

        :param name_data: 行中的应用服务名称。
        :type name_data: str

        :return: 如果当前行与选定的应用服务匹配，则返回 True。
        :rtype: bool
        """
        selected_app = self.filter_app_box.currentData()
        return True if selected_app == "all" or selected_app == name_data else False

    def _get_table_match(self,
                         consistency_data: str,
                         skip_data: str) -> bool:
        """
        根据表格状态过滤条件检查当前行是否匹配。

        :param consistency_data: 一致性状态数据。
        :type consistency_data: str
        :param skip_data: 跳过状态数据。
        :type skip_data: str

        :return: 如果当前行符合表格状态过滤条件，则返回 True。
        :rtype: bool
        """
        selected_table = self.filter_table_box.currentData()
        reverse_checked = self.filter_table_check_box.isChecked()
        # 直接对比较结果赋值bool，相等则为True
        fully_match = consistency_data == "fully"
        partially_match = consistency_data == "partially"
        skip_match = skip_data == "yes"
        # 根据快速过滤条件，返回组合比较结果。
        if selected_table == "fully":
            return fully_match if not reverse_checked else not fully_match
        elif selected_table == "partially":
            return partially_match if not reverse_checked else not partially_match
        elif selected_table == 'skip':
            return skip_match if not reverse_checked else not skip_match
        elif selected_table == "fully+partially":
            return (fully_match or partially_match) if not reverse_checked else not (fully_match or partially_match)
        elif selected_table == "fully+skip":
            return (fully_match or skip_match) if not reverse_checked else not (fully_match or skip_match)
        elif selected_table == "fully+partially+skip":
            return (fully_match or partially_match or skip_match) if not reverse_checked else not (fully_match or partially_match or skip_match)
        else:
            return False if not reverse_checked else True

    def _get_search_match(self,
                          row: int,
                          search_value: str,
                          index_key: str,
                          color_switch: str) -> bool:
        """
        检查当前行是否与搜索条件匹配。

        :param row: 表格中的行号。
        :type row: int
        :param search_value: 需要搜索的值。
        :type search_value: str
        :param index_key: 行索引值。
        :type index_key: str
        :param color_switch: 颜色开关。
        :type color_switch: str

        :return: 如果当前行包含搜索框中的文本，则返回 True。
        :rtype: bool
        """
        # 如果搜索值为空，则无需进行搜索
        if not search_value:
            return True
        # 禁止更新。主要着色时操作太多。
        self.table.setUpdatesEnabled(False)
        row_texts = []
        # 遍历每列的内容
        for column in range(self.table.columnCount()):
            # 不搜索隐藏的列
            if self.table.isColumnHidden(column):
                continue

            # 拼接一行全部数据到临时列表
            item = self.table.item(row, column)
            item_text = item.text().lower() if item else ''
            row_texts.append(item_text)

            # 应用颜色方案，只有有搜索结果的单元格会应用。
            if search_value in item_text and color_switch == 'ON':
                # 如果不在还原字典，则新增新索引键和空列表值。行数会随着排序变化，所以才引入index_key索引键作为依据。
                self.style_rows[index_key] = [] if index_key not in self.style_rows else self.style_rows[index_key]
                # 在还原字典更新索引键对应的列表值，插入列数作为键，颜色为值。如果没有颜色，设置默认白色。
                self.style_rows[index_key].append({column: item.background().color() if item.background() != QBrush() else QColor(COLOR_DEFAULT)})
                # 对单元格应用高亮色。
                item.setBackground(QBrush(QColor(COLOR_HIGHLIGHT)))
        # 启用更新
        self.table.setUpdatesEnabled(True)
        # 把row_texts转为字符串，返回搜索值在其中搜索的结果。
        return search_value in ' '.join(row_texts)

    def _reset_styles(self) -> None:
        """
        重置表格样式到记录的状态。

        此方法遍历表格中的所有行，对于每一行，恢复其单元格的背景颜色到初始状态。这通常在过滤条件发生变化或重置时调用。

        :rtype: None
        :return: 无返回值。
        """
        try:
            self.table.setUpdatesEnabled(False)
            # 还原字典为空则跳过
            if not self.style_rows:
                return
            # 遍历每行，但跳过隐藏行，因为隐藏行必然没有被更改颜色。
            # 反过来遍历还原字典并不可行，因为索引键并不储存在表格中，
            # 而且索引键和行号并不能形成牢固对应关系（行号可变），
            # 所以遍历所有行，但只操作匹配的单元格，最大程度减少对单元格的操作。
            for row in range(self.table.rowCount()):
                if self.table.isRowHidden(row):
                    continue
                # 生成当行索引键，并检测是否在还原字典中。
                index_key = self._generate_index_key(row)
                if index_key not in self.style_rows:
                    continue
                # 索引键在还原字典中找到时，根据行、列和单元格颜色数据，还原单元格本来颜色。
                self._apply_style_to_row(row, self.style_rows[index_key])
            # 完成后，清空还原字典。
            self.style_rows.clear()
        except Exception:
            logger.exception("Error occurred while resetting styles")
        finally:
            self.table.setUpdatesEnabled(True)

    def _generate_index_key(self, row: int) -> str:
        """
        生成索引键。

        此方法根据给定的行号生成一个唯一的索引键。索引键由行中特定列的值组合而成，用于标识表格中的唯一行。

        :param row: 表格中的行号。
        :type row: int

        :return: 生成的索引键。
        :rtype: str
        """
        name = self.table.item(row, COL_INFO['name']['col']).text()
        group = self.table.item(row, COL_INFO['group']['col']).text()
        key = self.table.item(row, COL_INFO['key']['col']).text()
        return f"{name}+{group}+{key}"

    def _apply_style_to_row(self,
                            row: int,
                            column_colors: list[Dict[int, QColor]]):
        """
        应用样式到每一行。

        此方法根据提供的颜色信息为指定行中的单元格设置背景颜色。

        :param row: 表格中的行号。
        :type row: int
        :param column_colors: 每一列的颜色信息，格式为列号到颜色的映射。
        :type column_colors: List[Dict[int, QColor]]

        :rtype: None
        :return: 无返回值。
        """
        for column_color in column_colors:
            for column, color in column_color.items():
                # 解析列表获取得到行、列和颜色信息后，应用到单元格背景颜色。
                self.table.item(row, column).setBackground(color)


