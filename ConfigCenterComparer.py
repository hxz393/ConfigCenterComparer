"""
这是一个用于比较和管理不同配置中心的Python模块。

本模块主要包含一个名为 `ConfigCenterComparer` 的类，该类用于创建和管理配置中心比较器的主窗口界面。此外，还包含一系列辅助函数和类，用于处理配置中心数据的展示和管理。

本模块的主要目的是提供一个界面友好且功能全面的配置中心管理工具。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""
import logging
import sys
from multiprocessing import freeze_support
from typing import Optional, Any

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, QToolBar)

from config.settings import LOG_PATH, PROGRAM_NAME
from lib.get_resource_path import get_resource_path
from lib.logging_config import logging_config
from module.init_config import init_config
from module.get_lang_dict import get_lang_dict
from ui import *

logger = logging.getLogger(__name__)


class ConfigCenterComparer(QMainWindow):
    """
    主窗口类，用于显示和管理配置中心比较器的界面。

    该类封装了配置中心比较器的主窗口界面，包括状态栏、工具栏、菜单栏以及主视图区域的管理和配置。
    """

    def __init__(self):
        """
        初始化配置中心比较器的主窗口。
        """
        super().__init__()

        init_config()
        self.lang = get_lang_dict()

        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面。

        此方法负责创建和配置主窗口中的所有用户界面元素，包括状态栏、表单、过滤器、动作、菜单栏和工具栏。
        """
        try:
            # 创建状态栏
            self._create_statusbar()
            # 创建表单
            self.table = TableMain(self)
            # 创建过滤器
            self.filter_bar = FilterBar(self)
            # 创建动作
            self._create_action()
            # 创建菜单栏
            self._create_menubar()
            # 创建工具栏
            self._create_toolbar()
            # 主窗口配置
            self._configure_main_window()
        except Exception:
            logger.exception("Unexpected error when initializing main window.")
            self.label_status.setText(self.lang['label_status_error'])

    def _create_statusbar(self) -> None:
        """
        创建状态栏。

        此方法用于创建并配置程序的状态栏，状态栏用于显示程序的状态信息。
        """
        self.label_status = QLabel(self.lang['main_1'])
        self.status_bar = self.statusBar()
        self.status_bar.addPermanentWidget(self.label_status)

    def _create_action(self) -> None:
        """
        创建程序中所有的动作。

        此方法负责初始化程序中的所有动作，包括关于、日志、设置等。
        """
        self.ActionAbout = ActionAbout(self)
        self.ActionLogs = ActionLogs(self)
        self.ActionSettingMain = ActionSettingMain(self)
        self.ActionSettingConnection = ActionSettingConnection(self)
        self.ActionExit = ActionExit(self)
        self.ActionUnskip = ActionUnskip(self)
        self.ActionSkip = ActionSkip(self)
        self.ActionSave = ActionSave(self)
        self.ActionCopy = ActionCopy(self)
        self.ActionUpdate = ActionUpdate(self)
        self.ActionStart = ActionStart(self)
        self.ActionTest = ActionTest(self)

    def _create_menubar(self) -> None:
        """
        创建菜单栏。

        此方法用于创建和配置程序的菜单栏，包括运行、编辑、选项和帮助等菜单。
        """
        menubar = self.menuBar()

        menu_run = menubar.addMenu(self.lang['main_2'])
        menu_run.addAction(self.ActionStart.action_start)
        menu_run.addAction(self.ActionTest.action_test)
        menu_run.addSeparator()
        menu_run.addAction(self.ActionExit.action_exit)
        menu_edit = menubar.addMenu(self.lang['main_3'])
        menu_edit.addAction(self.ActionCopy.action_copy)
        menu_edit.addSeparator()
        menu_edit.addAction(self.ActionSkip.action_skip)
        menu_edit.addAction(self.ActionUnskip.action_unskip)
        menu_edit.addSeparator()
        menu_edit.addAction(self.ActionSave.action_save)
        menu_option = menubar.addMenu(self.lang['main_4'])
        menu_option.addAction(self.ActionSettingMain.action_setting)
        menu_option.addAction(self.ActionSettingConnection.action_setting)
        menu_help = menubar.addMenu(self.lang['main_5'])
        menu_help.addAction(self.ActionLogs.action_logs)
        menu_help.addSeparator()
        menu_help.addAction(self.ActionUpdate.action_update)
        menu_help.addAction(self.ActionAbout.action_about)

    def _create_toolbar(self) -> None:
        """
        创建工具栏。

        此方法用于创建和配置程序的工具栏，提供快速访问的功能按钮。
        """
        toolbar = QToolBar(self.lang['main_6'], self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar.addAction(self.ActionStart.action_start)
        toolbar.addAction(self.ActionTest.action_test)
        toolbar.addSeparator()
        toolbar.addAction(self.ActionSkip.action_skip)
        toolbar.addAction(self.ActionUnskip.action_unskip)
        toolbar.addSeparator()
        toolbar.addAction(self.ActionCopy.action_copy)
        toolbar.addAction(self.ActionSave.action_save)
        toolbar.addSeparator()
        toolbar.addAction(self.ActionSettingMain.action_setting)
        toolbar.addAction(self.ActionSettingConnection.action_setting)
        toolbar.addSeparator()
        toolbar.addAction(self.ActionLogs.action_logs)
        toolbar.addAction(self.ActionExit.action_exit)

    def _configure_main_window(self) -> None:
        """
        配置主窗口的基本属性。

        此方法用于设置窗口大小、图标、名称以及布局。
        """
        # 设置窗口大小、图标和名称
        self.setGeometry(10, 10, 1280, 720)
        self.setWindowTitle(PROGRAM_NAME)
        self.setWindowIcon(QIcon(get_resource_path('media/main.svg')))

        # 创建垂直布局，加入表格和过滤器布局
        self.central_widget = QWidget()
        self.main_area = QVBoxLayout()
        self.main_area.addWidget(self.filter_bar)
        self.main_area.addWidget(self.table)
        self.central_widget.setLayout(self.main_area)

        # 设置为主窗口的中心部件
        self.central_widget.layout().setContentsMargins(10, 6, 10, 0)
        self.setCentralWidget(self.central_widget)

        # 移动窗口到屏幕中心
        self._center_window()

        # 展示主窗口
        self.show()

    def _center_window(self) -> None:
        """
        将窗口移动到屏幕中心。

        此方法用于计算屏幕尺寸，并将窗口移动到屏幕的中心位置。
        """
        screenGeometry = QApplication.desktop().screenGeometry()
        x = (screenGeometry.width() - self.width()) / 2
        y = (screenGeometry.height() - self.height()) / 2
        self.move(int(x), int(y))

    def get_elements(self, name: str) -> Optional[Any]:
        """
        获取界面上的指定元素。

        :param name: 元素名称，如 'lang'、'label_status' 等。
        :type name: str
        :return: 请求的界面元素或None。
        :rtype: Optional[Any]
        """
        try:
            if name == 'lang':
                return self.lang
            elif name == 'label_status':
                return self.label_status
            elif name == 'table':
                return self.table
            elif name == 'filter_bar':
                return self.filter_bar
            else:
                return None
        except Exception:
            logger.exception(f"Failed to get elements {name}")
            self.label_status.setText(self.lang['label_status_error'])


def main() -> None:
    """
    程序的主入口函数。

    此函数初始化应用程序和主窗口，并启动事件循环。
    """
    app = QApplication(sys.argv)
    _ = ConfigCenterComparer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # 在此处配置日志，避免在顶端配置导致收集重复日志，因为此文件会被其他模块导入。
    logging_config(log_file=LOG_PATH, console_output=True, max_log_size=1, log_level='DEBUG')
    freeze_support()
    main()
