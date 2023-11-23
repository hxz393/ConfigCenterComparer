"""
这是一个用于设置和管理软件连接配置的Python模块。

此模块包含主要类 `DialogSettingsConnection`，负责创建和处理软件的连接设置对话框。该对话框允许用户配置MySQL和SSH连接参数，并将这些设置保存到配置文件中。此外，该模块还包含辅助函数，用于创建UI组件和处理用户输入。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""


import logging
import os
from typing import Union

from PyQt5.QtCore import Qt, QRegExp, QObject
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QTabWidget, QWidget, QHBoxLayout, QFrame, QVBoxLayout, QGroupBox, QLabel, QCheckBox

from ConfigCenterComparer import ConfigCenterComparer
from lib.get_resource_path import get_resource_path
from lib.write_dict_to_json import write_dict_to_json
from module.read_config import read_config
from module.config_path_get import config_path_get
from ui.message_show import message_show

logger = logging.getLogger(__name__)


class DialogSettingsConnection(QDialog):
    """
    表示一个处理软件连接设置的对话框类。

    此类负责创建和管理软件的连接设置对话框，包括MySQL和SSH的配置。用户可以在此对话框中输入并保存连接参数。

    :param main_window: 主窗口对象，用于获取语言资源和状态标签。
    :type main_window: ConfigCenterComparer
    """

    def __init__(self, main_window: ConfigCenterComparer):
        """
        初始化连接设置对话框。

        :param main_window: 主窗口对象，用于获取语言资源和状态标签。
        :type main_window: ConfigCenterComparer
        """
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        self.main_window = main_window
        self.lang = self.main_window.get_elements('lang')
        self.label_status = self.main_window.get_elements('label_status')

        self.setWindowTitle(self.lang['ui.dialog_settings_connection_1'])
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-database-administrator-26')))
        self.setStyleSheet("font-size: 14px;")
        self.setMinimumSize(370, 490)

        self.config_main, self.config_connection = read_config()
        self.tab_config = {
            'PRO_CONFIG': self.lang['ui.dialog_settings_connection_2'],
            'PRE_CONFIG': self.lang['ui.dialog_settings_connection_3'],
            'TEST_CONFIG': self.lang['ui.dialog_settings_connection_4'],
            'DEV_CONFIG': self.lang['ui.dialog_settings_connection_5'],
        }
        self.initUI()

    def initUI(self):
        """
        初始化对话框的用户界面。

        创建并布置各种UI组件，如标签页、按钮和布局。
        """
        # 主布局
        layout = QFormLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.tab_widget = QTabWidget(self)
        # 创建标签页
        for config_key, tab_name in self.tab_config.items():
            self._construct_tab(config_key, tab_name)

        # 创建按钮
        self._construct_buttons()
        # 加入主布局
        layout.addRow(self.tab_widget)
        layout.addRow(self.button_layout)

    def _construct_tab(self, config_key: str, tab_name: str) -> None:
        """
        构建一个标签页。

        :param config_key: 配置键，用于标识不同的设置（如'PRO_CONFIG'）。
        :type config_key: str
        :param tab_name: 标签页的显示名称。
        :type tab_name: str
        """
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.addWidget(self._create_mysql_group(config_key))
        tab_layout.addWidget(self._create_ssh_group(config_key))
        # 组件之间添加弹性空间
        tab_layout.addStretch()
        # 插入标签页
        self.tab_widget.addTab(tab, tab_name)

    def _construct_buttons(self) -> None:
        """
        构建并配置对话框的按钮。

        此方法用于创建确认和取消按钮，并连接相应的事件处理函数。按钮文本使用当前语言环境下的文本进行设置。

        此方法还创建一个水平布局，将按钮添加到布局中，并设置布局的边距。
        """
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # 找到 Ok 和 Cancel 按钮并设置中文文本
        self.ok_button = self.button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setText(self.lang['ui.dialog_settings_main_11'])
        self.cancel_button = self.button_box.button(QDialogButtonBox.Cancel)
        self.cancel_button.setText(self.lang['ui.dialog_settings_main_12'])
        # 按钮连接事件
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # 创建一个水平布局
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button_box)
        self.button_layout.setContentsMargins(0, 0, 13, 8)

    def _create_check_box(self, config_key: str, name: str, group_box: QGroupBox, layout: QFormLayout, label_name: str) -> QCheckBox:
        """
        创建并添加一个复选框到指定布局。

        此方法用于创建一个复选框，并根据给定的配置键和名称设置初始状态。

        :param config_key: 配置键，用于标识不同的设置。
        :type config_key: str
        :param name: 复选框的名称。
        :type name: str
        :param group_box: 包含复选框的组框。
        :type group_box: QGroupBox
        :param layout: 要添加复选框的布局。
        :type layout: QFormLayout
        :param label_name: 复选框旁边的标签文本。
        :type label_name: str
        :return: 创建的复选框。
        :rtype: QCheckBox
        """
        check_box = QCheckBox()
        check_box.setObjectName(f"{config_key}_{name}_check_box")
        check_box.stateChanged.connect(lambda: self._toggle_edit_controls(check_box.isChecked(), group_box))
        check_box.setChecked(self.config_connection[config_key][f'{name}_on'])
        layout.addRow(QLabel(label_name), check_box)
        return check_box

    @staticmethod
    def _create_separator(layout: QFormLayout) -> QFrame:
        """
        创建并添加一个分隔符到指定布局。

        此方法用于在布局中添加一个水平分隔符。

        :param layout: 要添加分隔符的布局。
        :type layout: QFormLayout
        :return: 创建的分隔符。
        :rtype: QFrame
        """
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Raised)
        layout.addRow(separator)
        return separator

    def _create_line_edit(self, config_key: str, name: str, key: str, placeholder_txt: str, reg_exp: str, layout: QFormLayout, label_name: str) -> QLineEdit:
        """
        创建并添加一个输入框到指定布局。

        此方法用于创建一个输入框，并根据给定的配置键和名称设置初始值和验证规则。

        :param config_key: 配置键，用于标识不同的设置。
        :type config_key: str
        :param name: 输入框的名称。
        :type name: str
        :param key: 输入框关联的配置项键。
        :type key: str
        :param placeholder_txt: 输入框的占位符文本。
        :type placeholder_txt: str
        :param reg_exp: 输入验证的正则表达式。
        :type reg_exp: str
        :param layout: 要添加输入框的布局。
        :type layout: QFormLayout
        :param label_name: 输入框旁边的标签文本。
        :type label_name: str
        :return: 创建的输入框。
        :rtype: QLineEdit
        """
        config = self.config_connection[config_key][name]
        line_edit = QLineEdit(config.get(key, ''))
        line_edit.setObjectName(f"{config_key}_{name}_{key}")
        line_edit.setPlaceholderText(placeholder_txt)
        line_edit.setValidator(QRegExpValidator(QRegExp(reg_exp)))
        layout.addRow(QLabel(label_name), line_edit)
        return line_edit

    def _create_ssh_group(self, config_key: str) -> QGroupBox:
        """
        创建并配置SSH设置的界面组件。

        此方法用于创建包含SSH设置的用户界面组件，并将其添加到对话框中。

        :param config_key: 配置键，用于标识不同环境的SSH设置。
        :type config_key: str
        :return: 创建的SSH设置组框。
        :rtype: QGroupBox
        """
        # 创建SSH设置区域
        ssh_group_box = QGroupBox(self.lang['ui.dialog_settings_connection_6'])
        ssh_group_box.setStyleSheet("QGroupBox { font-weight: bold; text-align: center; }")
        ssh_layout = QFormLayout()

        # SSH 开关
        ssh_check_box = self._create_check_box(config_key, 'ssh', ssh_group_box, ssh_layout, self.lang['ui.dialog_settings_connection_7'])
        # 分隔符
        self._create_separator(ssh_layout)
        # 配置行
        self._create_line_edit(config_key, 'ssh', 'hostname', '127.0.0.1', "^[ -~]+$", ssh_layout, self.lang['ui.dialog_settings_connection_8'])
        self._create_line_edit(config_key, 'ssh', 'port', '22', "^[0-9]+$", ssh_layout, self.lang['ui.dialog_settings_connection_9'])
        self._create_line_edit(config_key, 'ssh', 'username', 'root', "^[ -~]+$", ssh_layout, self.lang['ui.dialog_settings_connection_10'])
        self._create_line_edit(config_key, 'ssh', 'password', '123456', "^[ -~]+$", ssh_layout, self.lang['ui.dialog_settings_connection_11'])

        # 将设置区域添加到对话框的布局中
        ssh_group_box.setLayout(ssh_layout)
        # 根据初始状态设置控件的可编辑状态
        self._toggle_edit_controls(ssh_check_box.isChecked(), ssh_group_box)
        return ssh_group_box

    def _create_mysql_group(self, config_key: str) -> QGroupBox:
        """
        创建并配置MySQL设置的界面组件。

        此方法用于创建包含MySQL设置的用户界面组件，并将其添加到对话框中。

        :param config_key: 配置键，用于标识不同环境的MySQL设置。
        :type config_key: str
        :return: 创建的MySQL设置组框。
        :rtype: QGroupBox
        """
        # 创建MySQL设置区域
        mysql_group_box = QGroupBox(self.lang['ui.dialog_settings_connection_13'])
        mysql_group_box.setStyleSheet("QGroupBox { font-weight: bold; text-align: center; }")
        mysql_layout = QFormLayout()
        # MySQL 开关
        mysql_check_box = self._create_check_box(config_key, 'mysql', mysql_group_box, mysql_layout, self.lang['ui.dialog_settings_connection_7'])
        # 分隔符
        self._create_separator(mysql_layout)
        # 配置行
        self._create_line_edit(config_key, 'mysql', 'host', '127.0.0.1', "^[ -~]+$", mysql_layout, self.lang['ui.dialog_settings_connection_8'])
        self._create_line_edit(config_key, 'mysql', 'port', '3306', "^[0-9]+$", mysql_layout, self.lang['ui.dialog_settings_connection_9'])
        self._create_line_edit(config_key, 'mysql', 'user', 'root', "^[ -~]+$", mysql_layout, self.lang['ui.dialog_settings_connection_10'])
        self._create_line_edit(config_key, 'mysql', 'password', '123456', "^[ -~]+$", mysql_layout, self.lang['ui.dialog_settings_connection_11'])
        self._create_line_edit(config_key, 'mysql', 'db', 'apolloconfigdb', "^[ -~]+$", mysql_layout, self.lang['ui.dialog_settings_connection_12'])

        # 将设置区域添加到对话框的布局中
        mysql_group_box.setLayout(mysql_layout)
        self._toggle_edit_controls(mysql_check_box.isChecked(), mysql_group_box)
        return mysql_group_box

    def _toggle_edit_controls(self, is_checked: bool, root: Union[QWidget, QObject]) -> None:
        """
        根据复选框的状态切换输入框的可编辑状态。

        :param is_checked: 复选框是否被选中。
        :type is_checked: bool
        :param root: 包含输入框的根控件。
        :type root: Union[QWidget, QObject]
        """
        for widget in root.findChildren(QLineEdit):
            self._set_line_edit_style(widget, not is_checked)

    @staticmethod
    def _set_line_edit_style(line_edit: QLineEdit, is_read_only: bool) -> None:
        """
        设置输入框的只读状态和样式。

        :param line_edit: 要设置样式的输入框。
        :type line_edit: QLineEdit
        :param is_read_only: 输入框是否为只读。
        :type is_read_only: bool
        """
        line_edit.setReadOnly(is_read_only)
        if is_read_only:
            line_edit.setStyleSheet("QLineEdit { background-color: '#e0e0e0'; }")
        else:
            line_edit.setStyleSheet("QLineEdit { background-color: white; }")

    def accept(self) -> None:
        """
        处理对话框的确认操作。

        当用户点击确认按钮时，从UI组件中提取数据更新配置字典，并将新配置写入文件。
        如果写入过程出错，则记录错误信息。
        """
        try:
            # 从输入框更新 config_connection
            self._update_config()
            # 将更新后的配置写入文件
            if write_dict_to_json(os.path.normpath(config_path_get(self.config_main)), self.config_connection):
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
        更新连接配置字典。

        从对话框的输入框中提取数据，更新内部的配置字典。
        """
        config_fields = {
            'mysql': ['host', 'port', 'user', 'password', 'db'],
            'ssh': ['hostname', 'port', 'username', 'password']
        }

        for config_key in self.tab_config.keys():
            for service, fields in config_fields.items():
                self._update_service_config(config_key, service, fields)

    def _update_service_config(self, config_key: str, service: str, fields: list) -> None:
        """
        更新特定服务的配置。

        此方法从对话框中的输入框提取数据，更新内部配置字典中特定服务的配置项。

        :param config_key: 配置键，用于标识不同环境的配置。
        :type config_key: str
        :param service: 服务类型（如 'mysql' 或 'ssh'）。
        :type service: str
        :param fields: 配置字段列表。
        :type fields: list
        """
        self.config_connection[config_key][f'{service}_on'] = self.findChild(QCheckBox, f"{config_key}_{service}_check_box").isChecked()
        for field in fields:
            self.config_connection[config_key][service][field] = self.findChild(QLineEdit, f"{config_key}_{service}_{field}").text()
