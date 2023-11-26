"""
此模块提供了一个对话框界面，用于处理应用程序的主要设置。

包括语言设置、配置中心类型选择、服务名替换规则等功能。用户可以通过此对话框修改各项设置，并将其保存到配置文件中。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import List, Tuple

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QComboBox

from config.lang_dict_all import LANG_DICTS
from config.settings import CONFIG_CENTER_LIST, APOLLO_NAME_LIST, COLOR_SET_LIST
from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class DialogSettingsMain(QDialog):
    """
    主设置对话框类。

    此类提供了一个对话框界面，供用户修改应用程序的主要设置，例如语言、配置中心类型、服务名替换规则等。
    它允许用户对这些设置进行更改，并通过按下确定按钮来保存这些更改。

    :param lang_manager: 语言管理器实例。
    :type lang_manager: LangManager
    :param config_manager: 配置管理器实例。
    :type config_manager: ConfigManager
    :ivar status_updated: 用于发出状态更新信号的pyqtSignal实例。
    :vartype status_updated: pyqtSignal
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager):
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        # 初始化两个管理器
        self.lang_manager = lang_manager
        self.config_manager = config_manager
        # 获取管理器中的配置
        self.config_main = self.config_manager.get_config_main()
        # 获取语言字典
        self.lang = self.lang_manager.get_lang()
        self.initUI()

    def initUI(self) -> None:
        """
        初始化用户界面。

        此方法设置对话框的标题、图标、样式和大小，并创建主布局。在主布局中，它添加了主要设置组和额外设置组的布局，并在两者之间添加了弹性空间。最后，添加了按钮布局。

        主要设置组包括语言选择、配置中心类型选择等，而额外设置组包括服务名替换规则的设置。此方法利用私有方法 `_create_main_group` 和 `_create_extra_group` 来创建这些组。

        :return: 无返回值。
        :rtype: None
        """
        # 主窗口
        self.setWindowTitle(self.lang['ui.dialog_settings_main_1'])
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-setting-26')))
        self.setStyleSheet("font-size: 14px;")
        self.setMinimumSize(370, 490)

        # 主布局
        layout = QVBoxLayout()
        # 上层布局
        layout.addWidget(self._create_main_group())
        # 下层布局
        layout.addWidget(self._create_extra_group())
        # 在两个组件之间添加弹性空间
        layout.addStretch()
        # 按钮布局
        layout.addLayout(self._create_buttons())

        self.setLayout(layout)

    def _create_main_group(self) -> QGroupBox:
        """
        创建并返回主要设置组的布局。

        此私有方法用于构建对话框中的主要设置组，包括语言选择、配置中心类型选择等。

        :return: 配置好的主要设置组。
        :rtype: QGroupBox
        """
        main_layout = QVBoxLayout()
        # 下拉框：选择语言
        self.language_combo_box = self._create_combo_box(main_layout, LANG_DICTS.keys(), self.lang['ui.dialog_settings_main_2'], self.config_main.get('lang', 'English'))
        # 下拉框：选择配置中心类型
        self.config_center_combo_box = self._create_combo_box(main_layout, CONFIG_CENTER_LIST, self.lang['ui.dialog_settings_main_3'], self.config_main.get('config_center', 'Apollo'))
        # 下拉框：选择 Apollo 配置服务名字段
        self.apollo_name_combo_box = self._create_combo_box(main_layout, APOLLO_NAME_LIST, self.lang['ui.dialog_settings_main_4'], self.config_main.get('apollo_name', 'AppId'))
        # 下拉框：选择颜色开关
        self.color_set_combo_box = self._create_combo_box(main_layout, COLOR_SET_LIST, self.lang['ui.dialog_settings_main_16'], self.config_main.get('color_set', 'ON'))
        # 分组
        main_group = QGroupBox(self.lang['ui.dialog_settings_main_5'])
        main_group.setStyleSheet("QGroupBox { font-weight: bold; text-align: center; }")
        main_group.setLayout(main_layout)
        return main_group

    def _create_extra_group(self) -> QGroupBox:
        """
        创建并返回额外设置组的布局。

        此私有方法用于构建对话框中的额外设置组，包括服务名替换规则的设置。

        :return: 配置好的额外设置组。
        :rtype: QGroupBox
        """
        extra_layout = QVBoxLayout()
        # 输入框：替换原服务名
        self.fix_name_before = self._create_line_edit(extra_layout, self.lang['ui.dialog_settings_main_6'], self.config_main.get('fix_name_before', ''))
        # 输入框：替换新服务名
        self.fix_name_after = self._create_line_edit(extra_layout, self.lang['ui.dialog_settings_main_7'], self.config_main.get('fix_name_after', ''))
        # 输入框：裁剪服务名前缀
        self.fix_name_left = self._create_line_edit(extra_layout, self.lang['ui.dialog_settings_main_8'], self.config_main.get('fix_name_left', ''))
        # 输入框：裁剪服务名后缀
        self.fix_name_right = self._create_line_edit(extra_layout, self.lang['ui.dialog_settings_main_9'], self.config_main.get('fix_name_right', ''))
        # 分组
        extra_group = QGroupBox(self.lang['ui.dialog_settings_main_10'])
        extra_group.setStyleSheet("QGroupBox { font-weight: bold; text-align: center; }")
        extra_group.setLayout(extra_layout)
        return extra_group

    @staticmethod
    def _create_combo_box(layout: QVBoxLayout,
                          items: List[str],
                          label_text: str,
                          current_text: str) -> QComboBox:
        """
        创建并返回一个预配置的下拉框。

        :param layout: 要添加下拉框的布局。
        :type layout: QVBoxLayout
        :param items: 下拉框中的选项列表。
        :type items: List[str]
        :param label_text: 下拉框旁边的标签文本。
        :type label_text: str
        :param current_text: 下拉框的当前选中项。
        :type current_text: str
        :return: 配置好的下拉框。
        :rtype: QComboBox
        """
        combo_box = QComboBox()
        combo_box.addItems(items)
        combo_box.setCurrentText(current_text)
        layout.addWidget(QLabel(label_text))
        layout.addWidget(combo_box)
        return combo_box

    @staticmethod
    def _create_line_edit(layout: QVBoxLayout,
                          label_text: str,
                          text: str) -> QLineEdit:
        """
        创建并返回一个预配置的文本输入框。

        :param layout: 要添加文本输入框的布局。
        :type layout: QVBoxLayout
        :param label_text: 文本输入框旁边的标签文本。
        :type label_text: str
        :param text: 文本输入框的初始文本。
        :type text: str
        :return: 配置好的文本输入框。
        :rtype: QLineEdit
        """
        line_edit = QLineEdit(text)
        layout.addWidget(QLabel(label_text))
        layout.addWidget(line_edit)
        return line_edit

    def _create_buttons(self) -> QHBoxLayout:
        """
        创建并返回对话框底部的按钮布局。

        此私有方法用于构建对话框底部的按钮，包括确定和取消按钮。

        :return: 包含确定和取消按钮的布局。
        :rtype: QHBoxLayout
        """
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.ok_button = self.button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setText(self.lang['ui.dialog_settings_main_11'])
        self.cancel_button = self.button_box.button(QDialogButtonBox.Cancel)
        self.cancel_button.setText(self.lang['ui.dialog_settings_main_12'])
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_box)
        button_layout.setContentsMargins(0, 10, 0, 0)
        return button_layout

    def reject(self) -> None:
        """
        处理对话框的取消操作。

        当用户点击取消按钮时，关闭对话框并忽略所有未保存的更改。
        """
        super().reject()

    def accept(self) -> None:
        """
        处理对话框的确认操作。

        当用户点击确认按钮时，此方法会更新配置，并尝试将其写入配置文件。如果成功，则发出状态更新信号；如果失败，则显示错误消息。

        :return: 无返回值。
        :rtype: None
        """
        try:
            # 对比语言值，有修改则在LangManager类中修改
            self._check_language_change()
            # 读取用户输入的新配置
            self._update_config()
            # 更新ConfigManager类实例中的配置
            self.config_manager.update_config_main(self.config_main)
            # 发送更新成功状态信号
            self.status_updated.emit(self.lang['ui.dialog_settings_main_13'])
            super().accept()
            logger.info("Settings saved")
        except Exception:
            logger.exception("Error while updating settings")
            self.status_updated.emit(self.lang['label_status_error'])

    def _update_config(self) -> None:
        """
        更新配置信息。

        从对话框中收集用户输入的数据，并更新内存中的配置信息。不直接写入文件。

        :return: 无返回值。
        :rtype: None
        """
        before_list = self.fix_name_before.text().split(' ')
        after_list = self.fix_name_after.text().split(' ')
        before_list, after_list = self._adjust_list_lengths(before_list, after_list)

        self.config_main['fix_name_before'] = ' '.join(before_list)
        self.config_main['fix_name_after'] = ' '.join(after_list)
        self.config_main['lang'] = self.language_combo_box.currentText()
        self.config_main['config_center'] = self.config_center_combo_box.currentText()
        self.config_main['apollo_name'] = self.apollo_name_combo_box.currentText()
        self.config_main['color_set'] = self.color_set_combo_box.currentText()
        self.config_main['fix_name_left'] = self.fix_name_left.text()
        self.config_main['fix_name_right'] = self.fix_name_right.text()

    @staticmethod
    def _adjust_list_lengths(before_list: List[str],
                             after_list: List[str]) -> Tuple[List[str], List[str]]:
        """
        调整两个列表的长度使其相等。

        此方法用于处理替换前后的名称列表，确保两个列表长度相同。如果长度不同，它会截断较长列表以匹配较短列表的长度。

        :param before_list: 替换前的名称列表。
        :type before_list: List[str]
        :param after_list: 替换后的名称列表。
        :type after_list: List[str]
        :return: 调整长度后的两个列表。
        :rtype: Tuple[List[str], List[str]]
        """
        min_length = min(len(before_list), len(after_list))
        if len(before_list) != len(after_list):
            logger.warning("Before and after lists do not have the same length. Adjusting to the smaller list size.")
            before_list = before_list[:min_length]
            after_list = after_list[:min_length]
        return before_list, after_list

    def _check_language_change(self) -> None:
        """
        检查语言设置是否更改。

        如果用户更改语言设置，要调用LangManager类的方法update_lang，发送新语言字符串。
        更新LangManager类实例中的self.lang_dict内容，并发送lang_updated信号。
        所有连接了LangManager类实例lang_updated信号的类，将会执行绑定的函数。
        一般是self.update_lang()，里面最先运行的就是更新自己的self.lang：
        self.lang = self.lang_manager.get_lang()
        然后是用方法更新各地方的显示字符串：
        self.action_about.setText(self.lang['ui.action_about_1'])

        :rtype: None
        :return: 无返回值。
        """
        if self.language_combo_box.currentText() != self.config_main.get('lang', 'English'):
            self.lang_manager.update_lang(self.language_combo_box.currentText())
