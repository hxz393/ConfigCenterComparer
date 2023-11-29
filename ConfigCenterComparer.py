"""
本模块实现了一个配置中心比较器应用，提供界面交互和配置管理功能。

主要包括 `ConfigCenterComparer` 类，用于创建和管理应用程序的主窗口。该类整合了各种UI组件和功能，如状态栏、过滤器、动作管理等，以提供完整的用户界面和交互逻辑。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
import sys
from multiprocessing import freeze_support

from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QToolBar

from config.settings import LOG_PATH, PROGRAM_NAME
from lib.get_resource_path import get_resource_path
from lib.logging_config import logging_config
from module.init_config import init_config
from ui import LangManager, ConfigManager, StatusBar, TableMain, FilterBar, ActionExit, ActionAbout, ActionLogs, ActionSettingMain, ActionSettingConnection, ActionUpdate, ActionTest, ActionCopy, ActionSave, ActionSkip, ActionUnskip, ActionStart, ActionDebug, ActionCompare, global_signals

logger = logging.getLogger(__name__)


class ConfigCenterComparer(QMainWindow):
    """
    配置中心比较器主窗口类。

    此类创建并管理应用程序的主界面，包括状态栏、表格、过滤器栏和工具栏等组件。它还负责处理用户的操作和界面更新。
    """

    def __init__(self):
        super().__init__()
        # 初始化配置文件。
        init_config()
        self.lang_manager = LangManager()
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.lang = self.lang_manager.get_lang()
        self.config_manager = ConfigManager()
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面组件。

        :return: 无返回值。
        :rtype: None
        """
        # 创建状态栏
        self.status_bar = StatusBar(self.lang_manager)
        # 创建表单
        self.table = TableMain(self.lang_manager, self.config_manager)
        # 创建过滤器
        self.filter_bar = FilterBar(self.lang_manager, self.config_manager, self.table)
        # 创建动作和连接信号
        self._create_action()
        # 创建菜单栏
        self._create_menubar()
        # 创建工具栏
        self._create_toolbar()
        # 主窗口配置
        self._configure_main_window()
        # 更新主界面文字
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :rtype: None
        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.menu_run.setTitle(self.lang['main_2'])
        self.menu_edit.setTitle(self.lang['main_3'])
        self.menu_option.setTitle(self.lang['main_4'])
        self.menu_help.setTitle(self.lang['main_5'])

    def _create_action(self) -> None:
        """
        创建应用程序的动作，并连接信号和槽。

        :return: 无返回值。
        :rtype: None
        """
        self.table.status_updated.connect(self.status_bar.show_message)
        self.table.filter_updated.connect(self.filter_bar.filter_table)
        self.filter_bar.status_updated.connect(self.status_bar.show_message)
        self.actionExit = ActionExit(self.lang_manager)
        self.actionExit.status_updated.connect(self.status_bar.show_message)
        self.actionAbout = ActionAbout(self.lang_manager)
        self.actionAbout.status_updated.connect(self.status_bar.show_message)
        self.actionLogs = ActionLogs(self.lang_manager)
        self.actionLogs.status_updated.connect(self.status_bar.show_message)
        self.actionSettingMain = ActionSettingMain(self.lang_manager, self.config_manager)
        self.actionSettingMain.status_updated.connect(self.status_bar.show_message)
        self.actionSettingConnection = ActionSettingConnection(self.lang_manager, self.config_manager)
        self.actionSettingConnection.status_updated.connect(self.status_bar.show_message)
        self.actionUpdate = ActionUpdate(self.lang_manager)
        self.actionUpdate.status_updated.connect(self.status_bar.show_message)
        self.actionTest = ActionTest(self.lang_manager, self.config_manager)
        self.actionTest.status_updated.connect(self.status_bar.show_message)
        self.actionCopy = ActionCopy(self.lang_manager, self.table)
        self.actionCopy.status_updated.connect(self.status_bar.show_message)
        self.actionSave = ActionSave(self.lang_manager, self.table)
        self.actionSave.status_updated.connect(self.status_bar.show_message)
        self.actionSkip = ActionSkip(self.lang_manager, self.config_manager, self.table)
        self.actionSkip.status_updated.connect(self.status_bar.show_message)
        self.actionSkip.filter_updated.connect(self.filter_bar.filter_table)
        self.actionUnskip = ActionUnskip(self.lang_manager, self.config_manager, self.table)
        self.actionUnskip.status_updated.connect(self.status_bar.show_message)
        self.actionUnskip.filter_updated.connect(self.filter_bar.filter_table)
        self.actionStart = ActionStart(self.lang_manager, self.config_manager, self.table, self.filter_bar)
        self.actionStart.status_updated.connect(self.status_bar.show_message)
        self.actionDebug = ActionDebug(self.lang_manager, self.config_manager, self.table, self.filter_bar)
        self.actionDebug.status_updated.connect(self.status_bar.show_message)
        self.actionCompare = ActionCompare(self.lang_manager, self.config_manager, self.table)
        self.actionCompare.status_updated.connect(self.status_bar.show_message)

    def _create_menubar(self) -> None:
        """
        创建菜单栏。

        :return: 无返回值。
        :rtype: None
        """
        menubar = self.menuBar()

        self.menu_run = menubar.addMenu("")
        self.menu_run.addAction(self.actionStart.action_start)
        self.menu_run.addAction(self.actionTest.action_test)
        self.menu_run.addAction(self.actionCompare.action_compare)
        self.menu_run.addSeparator()
        self.menu_run.addAction(self.actionExit.action_exit)
        self.menu_edit = menubar.addMenu("")
        self.menu_edit.addAction(self.actionCopy.action_copy)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.actionSkip.action_skip)
        self.menu_edit.addAction(self.actionUnskip.action_unskip)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.actionSave.action_save)
        self.menu_option = menubar.addMenu("")
        self.menu_option.addAction(self.actionSettingMain.action_setting)
        self.menu_option.addAction(self.actionSettingConnection.action_setting)
        self.menu_help = menubar.addMenu("")
        self.menu_help.addAction(self.actionLogs.action_logs)
        self.menu_help.addAction(self.actionDebug.action_debug)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.actionUpdate.action_update)
        self.menu_help.addAction(self.actionAbout.action_about)

    def _create_toolbar(self) -> None:
        """
        创建工具栏。

        :return: 无返回值。
        :rtype: None
        """
        self.toolbar = QToolBar('ToolBar', self)
        self.toolbar.setMovable(False)

        self.toolbar.addAction(self.actionStart.action_start)
        self.toolbar.addAction(self.actionTest.action_test)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionSkip.action_skip)
        self.toolbar.addAction(self.actionUnskip.action_unskip)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionCopy.action_copy)
        self.toolbar.addAction(self.actionSave.action_save)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionSettingMain.action_setting)
        self.toolbar.addAction(self.actionSettingConnection.action_setting)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionLogs.action_logs)
        self.toolbar.addAction(self.actionExit.action_exit)

    def _configure_main_window(self) -> None:
        """
        配置主窗口的基本属性。

        此方法负责设置主窗口的大小、图标、名称，以及添加主要的UI组件，如表格和过滤器。

        :return: 无返回值。
        :rtype: None
        """
        # 设置窗口大小、图标和名称
        self.setGeometry(10, 10, 1280, 720)
        self.setWindowTitle(PROGRAM_NAME)
        self.setWindowIcon(QIcon(get_resource_path('media/main.svg')))
        # 创建垂直布局，加入表格和过滤器
        self.central_widget = QWidget()
        self.main_area = QVBoxLayout()
        self.main_area.addWidget(self.filter_bar)
        self.main_area.addWidget(self.table)
        self.setStatusBar(self.status_bar)
        self.addToolBar(self.toolbar)
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

        :return: 无返回值。
        :rtype: None
        """
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) / 2
        y = (screen.height() - self.height()) / 2
        self.move(int(x), int(y))

    def closeEvent(self, event: QCloseEvent):
        """
        处理窗口关闭事件。

        当用户尝试关闭窗口时，此方法将被调用。它负责发送关闭信号并处理异常。

        :param event: 关闭事件对象。
        :type event: QCloseEvent
        :return: 无返回值。
        :rtype: None
        """
        try:
            global_signals.close_all.emit()
        except Exception:
            logger.exception("Error encountered while sending close signal")
            event.ignore()
        else:
            event.accept()


def main() -> None:
    """
    应用程序的主入口函数。

    此函数负责初始化和启动应用程序。

    :return: 无返回值。
    :rtype: None
    """
    try:
        app = QApplication(sys.argv)
        _ = ConfigCenterComparer()
        sys.exit(app.exec_())
    except Exception:
        logger.exception("Application failed to start")


if __name__ == '__main__':
    logging_config(log_file=LOG_PATH, console_output=True, max_log_size=1, log_level='DEBUG')
    freeze_support()
    main()
