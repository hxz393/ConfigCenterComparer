"""
此模块提供用于筛选和管理配置中心比较结果的类和方法。

它包含了`FilterBar`类，该类负责创建和管理过滤器界面，允许用户基于不同的条件（如服务名称、表格状态等）来筛选显示的配置数据。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QCheckBox, QFrame, QWidget, QSizePolicy

from ConfigCenterComparer import ConfigCenterComparer
from config.settings import COL_INFO, COLOR_HIGHLIGHT
from module.read_config import read_config

logger = logging.getLogger(__name__)


class FilterBar(QWidget):
    """
    用于在配置中心比较器界面中创建和管理过滤器的类。

    此类创建了一个工具栏，允许用户基于服务名称、表格状态和搜索条件来筛选显示的配置数据。

    :param main_window: 主窗口对象，用于获取和更新界面元素。
    :type main_window: ConfigCenterComparer
    :param parent: 父窗口，QWidget 的可选参数。
    :type parent: Optional[QWidget]
    """

    def __init__(self, main_window: ConfigCenterComparer, parent: Optional[QWidget] = None):
        """
        初始化过滤器工具栏。

        :param main_window: 配置中心比较器的主窗口对象。
        :type main_window: ConfigCenterComparer
        :param parent: 父窗口，QWidget 的可选参数。
        :type parent: Optional[QWidget]
        """
        super().__init__(parent)

        self.main_window = main_window
        self.table = self.main_window.get_elements('table')
        self.label_status = self.main_window.get_elements('label_status')
        self.lang = self.main_window.get_elements('lang')
        # 用于还原样式
        self.original_styles = {}

        self._setup_filters()

    def _setup_filters(self) -> None:
        """
        设置过滤器的布局和组件。

        此方法初始化整个过滤器工具栏的布局，包括各种过滤器组件的创建和排列。它负责调用创建不同过滤组件的内部方法，如服务过滤器、表格状态过滤器和搜索过滤器，并定义其在工具栏中的布局。
        """
        try:
            self.setStyleSheet("font-size: 14px;")
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
        except Exception:
            logger.exception("Failed to set up filters in FilterBar")
            self.label_status.setText(self.lang['label_status_error'])

    def _create_filter_app(self) -> None:
        """
        创建服务过滤组件。

        此方法初始化服务过滤下拉框，并设置其事件处理函数。
        """
        self.layout.addWidget(QLabel(self.lang['ui.filter_bar_1']))
        # 过滤服务下拉框
        self.filter_app_box = QComboBox()
        # 设置下拉框的尺寸策略和宽度
        self.filter_app_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filter_app_box.setMinimumWidth(100)
        self.filter_app_box.setMaximumWidth(300)
        # 设置下拉框的选项，通过函数填充
        self.filter_options_add()
        # 设置下拉框的事件处理
        self.filter_app_box.currentIndexChanged.connect(self.filter_table)
        self.layout.addWidget(self.filter_app_box)
        # 创建一个 QFrame 作为分割线
        self._create_separator()

    def _create_filter_table(self) -> None:
        """
        创建表格状态过滤组件。

        此方法初始化表格状态过滤下拉框和反向选择复选框，并设置它们的事件处理函数。
        """
        self.layout.addWidget(QLabel(self.lang['ui.filter_bar_2']))
        # 过滤列表下拉框
        self.filter_table_box = QComboBox()
        # 设置下拉框的选项
        self.filter_table_box.addItem(self.lang['ui.filter_bar_3'], "all")
        self.filter_table_box.addItem(self.lang['ui.filter_bar_4'], "fully")
        self.filter_table_box.addItem(self.lang['ui.filter_bar_5'], "partially")
        self.filter_table_box.addItem(self.lang['ui.filter_bar_6'], "skip")
        self.filter_table_box.addItem(f"{self.lang['ui.filter_bar_4']}+{self.lang['ui.filter_bar_6']}", "fully+skip")
        self.filter_table_box.addItem(f"{self.lang['ui.filter_bar_4']}+{self.lang['ui.filter_bar_5']}", "fully+partially")
        self.filter_table_box.addItem(f"{self.lang['ui.filter_bar_4']}+{self.lang['ui.filter_bar_5']}+{self.lang['ui.filter_bar_6']}", "fully+partially+skip")
        # 设置下拉框的事件处理
        self.filter_table_box.currentIndexChanged.connect(self.filter_table)
        self.layout.addWidget(self.filter_table_box)
        # 反向选择
        self.filter_table_check_box = QCheckBox(self.lang['ui.filter_bar_7'])
        self.filter_table_check_box.stateChanged.connect(self.filter_table)
        self.layout.addWidget(self.filter_table_check_box)
        # 创建一个 QFrame 作为分割线
        self._create_separator()

    def _create_filter_value(self) -> None:
        """
        创建搜索过滤组件。

        此方法初始化搜索框和相关按钮，并设置事件处理函数，以便用户可以根据特定文本过滤表格数据。
        """
        self.layout.addWidget(QLabel(self.lang['ui.filter_bar_8']))
        # 搜索输入框
        self.filter_value_box = QLineEdit()
        self.filter_value_box.returnPressed.connect(self.filter_table)
        # 设置下拉框的尺寸策略和最小宽度
        self.filter_value_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filter_value_box.setMinimumWidth(100)
        self.layout.addWidget(self.filter_value_box)
        # 搜索按钮
        self.filter_value_button = QPushButton(self.lang['ui.filter_bar_9'])
        self.filter_value_button.clicked.connect(self.filter_table)
        self.layout.addWidget(self.filter_value_button)
        # 重置按钮
        self.filter_reset_button = QPushButton(self.lang['ui.filter_bar_10'])
        self.filter_reset_button.clicked.connect(self.filter_reset)
        self.layout.addWidget(self.filter_reset_button)

    def _create_separator(self) -> None:
        """
        创建界面中的分隔线。

        此方法用于在过滤器工具栏中添加分隔线，以提高界面的视觉效果和用户体验。
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Raised)
        self.layout.addWidget(separator)

    def filter_options_add(self) -> None:
        """
        填充服务过滤下拉框选项。

        此方法从配置数据中提取所有唯一的服务名称，并将它们添加到服务过滤下拉框中。
        """
        try:
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
            self.label_status.setText(self.lang['label_status_error'])

    def filter_reset(self) -> None:
        """
        重置过滤条件。

        此方法将所有过滤组件重置为默认状态，以便用户可以重新开始过滤操作。
        """
        try:
            # 重置单元格颜色
            self.reset_styles()
            # 重置 QComboBox 为第一个项，通常是 "--显示所有--"
            self.filter_app_box.setCurrentIndex(0)
            self.filter_table_box.setCurrentIndex(0)
            # 清空搜索框 QLineEdit
            self.filter_value_box.clear()
            # 显示所有行
            [self.table.setRowHidden(row, False) for row in range(self.table.rowCount())]
            # 更新状态栏信息为过滤后的行数
            self.label_status.setText(f"{self.table.rowCount()} {self.lang['ui.filter_bar_11']}")
        except Exception:
            logger.exception("Error occurred while resetting filters")
            self.label_status.setText(self.lang['label_status_error'])

    def filter_table(self) -> None:
        """
        应用过滤条件到表格。

        此方法根据用户设置的过滤条件（服务名称、表格状态、搜索文本）来决定哪些行在表格中可见。
        """
        try:
            # 计算可见的行数
            visible_rows = 0
            # 在新的搜索开始之前，遍历 self.original_styles，恢复每个单元格的原始样式。
            self.reset_styles()

            for row in range(self.table.rowCount()):
                consistency_data = self.table.item(row, COL_INFO['consistency']['col']).data(Qt.UserRole)
                skip_data = self.table.item(row, COL_INFO['skip']['col']).data(Qt.UserRole)
                name_data = self.table.item(row, COL_INFO['name']['col']).text()

                # 匹配选择所有或者选择服务名时为True
                app_match = self._get_app_match(name_data)
                # 匹配过滤条件时为True
                table_match = self._get_table_match(consistency_data, skip_data)
                # 匹配搜索条件或不输入时为True
                search_match = self._get_search_match(row)
                # 仅当条件都匹配时才显示行
                is_visible = app_match and not table_match and search_match
                self.table.setRowHidden(row, not is_visible)
                if is_visible:
                    visible_rows += 1
            # 更新状态栏信息为过滤后的行数
            self.label_status.setText(f"{visible_rows} {self.lang['ui.filter_bar_11']}")
        except Exception:
            logger.exception("Exception in filter_table method")
            self.label_status.setText(self.lang['label_status_error'])

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

    def _get_table_match(self, consistency_data: str, skip_data: str) -> bool:
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
        fully_match = consistency_data == "fully"
        partially_match = consistency_data == "partially"
        skip_match = skip_data == "yes"

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
            return False

    def _get_search_match(self, row: int) -> bool:
        """
        检查当前行是否与搜索条件匹配。

        :param row: 表格中的行号。
        :type row: int
        :return: 如果当前行包含搜索框中的文本，则返回 True。
        :rtype: bool
        """
        self.config_main, self._ = read_config()
        search_value = self.filter_value_box.text().strip().lower()
        # 如果搜索值为空，则无需进行搜索
        if not search_value:
            return True

        row_text = ''
        for column in range(self.table.columnCount()):
            if not self.table.isColumnHidden(column):
                item = self.table.item(row, column)
                item_text = item.text().lower() if item else ''
                row_text += item_text + ' '

                if self.config_main.get('color_set', 'ON') == 'ON' and search_value in item_text:
                    if (row, column) not in self.original_styles:
                        # 存储颜色
                        self.original_styles[(row, column)] = item.background() if item else None
                    # 修改背景颜色
                    self.table.apply_color(row, COLOR_HIGHLIGHT, column)

        return search_value in row_text

    def reset_styles(self):
        """
        重置表格样式到原始状态。
        """
        try:
            for (row, column), color in self.original_styles.items():
                item = self.table.item(row, column)
                if item:  # 确保表格项存在
                    item.setBackground(color)
            self.original_styles.clear()
        except Exception:
            logger.exception("Error occurred while resetting styles")
