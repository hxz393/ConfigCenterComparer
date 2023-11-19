"""
这是一个用于配置和管理软件设置的Python模块。

本模块包含主要类 `DialogSettingsMain`，用于展示和处理软件设置对话框。此对话框允许用户修改多种设置，包括界面语言、配置中心类型、服务名替换规则等。

本模块的目的是为用户提供一个简洁直观的界面，用于调整和保存软件的关键设置。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import os
from typing import List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QComboBox

from ConfigCenterComparer import ConfigCenterComparer
from config.lang_dict_all import lang_dict_all
from config.settings import CONFIG_MAIN_PATH, CONFIG_CENTER_LIST, APOLLO_NAME_LIST
from lib.get_resource_path import get_resource_path
from lib.write_dict_to_json import write_dict_to_json
from module.read_config import read_config
from .message_restart import message_restart
from .message_show import message_show

logger = logging.getLogger(__name__)


class DialogSettingsMain(QDialog):
    """
    表示配置中心比较器的主设置对话框类。

    提供一个图形用户界面，允许用户更改语言、配置中心类型等设置，并将这些设置保存到配置文件中。

    :param main_window: 配置中心比较器的主窗口对象。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化配置中心比较器的主设置对话框。

        设置窗口标题、图标、样式、最小尺寸，并从配置文件读取当前配置。最后，调用 `initUI` 方法来初始化用户界面。

        :param main_window: 配置中心比较器的主窗口对象。
        :type main_window: ConfigCenterComparer
        """
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        self.main_window = main_window
        self.lang = self.main_window.get_elements('lang')
        self.label_status = self.main_window.get_elements('label_status')

        self.setWindowTitle(self.lang['ui.dialog_settings_main_1'])
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-setting-26')))
        self.setStyleSheet("font-size: 14px;")
        self.setMinimumSize(370, 490)

        # 从配置文件读取配置
        self.config_main, _ = read_config()
        # 存储原始语言设置
        self.original_language_setting = self.config_main.get('lang', 'English')
        self.initUI()

    def initUI(self):
        """
        初始化用户界面。

        创建并布局主界面和额外界面的组件，包括语言选择、配置中心类型选择等。
        """
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
        self.language_combo_box = self._create_combo_box(main_layout, lang_dict_all.keys(), self.lang['ui.dialog_settings_main_2'], self.config_main.get('lang', 'English'))
        # 下拉框：选择配置中心类型
        self.config_center_combo_box = self._create_combo_box(main_layout, CONFIG_CENTER_LIST, self.lang['ui.dialog_settings_main_3'], self.config_main.get('config_center', 'Apollo'))
        # 下拉框：选择 Apollo 配置服务名字段
        self.apollo_name_combo_box = self._create_combo_box(main_layout, APOLLO_NAME_LIST, self.lang['ui.dialog_settings_main_4'], self.config_main.get('apollo_name', 'AppId'))

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

        extra_group = QGroupBox(self.lang['ui.dialog_settings_main_10'])
        extra_group.setStyleSheet("QGroupBox { font-weight: bold; text-align: center; }")
        extra_group.setLayout(extra_layout)
        return extra_group

    @staticmethod
    def _create_combo_box(layout: QVBoxLayout, items: List[str], label_text: str, current_text: str) -> QComboBox:
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
    def _create_line_edit(layout: QVBoxLayout, label_text: str, text: str) -> QLineEdit:
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

    def accept(self):
        """
        处理对话框的确认操作。

        当用户点击确认按钮时，更新配置，并尝试将其写入配置文件。如果语言设置发生变化，提示重启。
        """
        try:
            self._update_config()
            if self._write_config_to_file():
                self._check_language_change()
                self.label_status.setText(self.lang['ui.dialog_settings_main_13'])
                super().accept()
            else:
                message_show('Critical', self.lang['ui.dialog_settings_main_14'])
        except Exception:
            logger.exception("Unexpected error")
            self.label_status.setText(self.lang['label_status_error'])

    def reject(self) -> None:
        """
        处理对话框的取消操作。

        当用户点击取消按钮时，关闭对话框并忽略所有未保存的更改。
        """
        super().reject()

    def _update_config(self) -> None:
        """
        更新配置信息。

        从对话框中收集用户输入的数据，并更新内存中的配置信息。不直接写入文件。
        """
        before_list = self.fix_name_before.text().split(' ')
        after_list = self.fix_name_after.text().split(' ')
        before_list, after_list = self._adjust_list_lengths(before_list, after_list)

        self.config_main['fix_name_before'] = ' '.join(before_list)
        self.config_main['fix_name_after'] = ' '.join(after_list)
        self.config_main['lang'] = self.language_combo_box.currentText()
        self.config_main['config_center'] = self.config_center_combo_box.currentText()
        self.config_main['apollo_name'] = self.apollo_name_combo_box.currentText()
        self.config_main['fix_name_left'] = self.fix_name_left.text()
        self.config_main['fix_name_right'] = self.fix_name_right.text()

    @staticmethod
    def _adjust_list_lengths(before_list: List[str], after_list: List[str]) -> Tuple[List[str], List[str]]:
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

    def _write_config_to_file(self) -> bool:
        """
        将配置信息写入文件。

        将内存中更新后的配置信息保存到配置文件中。

        :return: 如果写入成功则返回 True，否则返回 False。
        :rtype: bool
        """
        try:
            write_dict_to_json(os.path.normpath(CONFIG_MAIN_PATH), self.config_main)
            return True
        except Exception:
            logger.exception("Unexpected error")
            return False

    def _check_language_change(self) -> None:
        """
        检查语言设置是否更改。

        如果用户更改了语言设置，显示重启消息提示用户重启应用以应用新的语言设置。
        """
        if self.language_combo_box.currentText() != self.original_language_setting:
            message_restart(self.lang['ui.dialog_settings_main_15'])
