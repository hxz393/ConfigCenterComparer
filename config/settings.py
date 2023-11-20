"""
全局静态变量
"""
# 配置路径
CONFIG_MAIN_PATH = r'config/config_main.json'
CONFIG_APOLLO_PATH = r'config/config_apollo.json'
CONFIG_NACOS_PATH = r'config/config_nacos.json'
CONFIG_SKIP_PATH = r'config/config_skip.txt'
LOG_PATH = 'logs/run.log'
# 程序信息
PROGRAM_NAME = 'ConfigCenterComparer'
VERSION_INFO = 'v1.0.2'
AUTHOR_NAME = 'assassing'
CONTACT_MAIL = 'hxz393@gmail.com'
WEBSITE_URL = 'https://blog.x2b.net'
CHECK_UPDATE_URL = 'https://blog.x2b.net/ver/configcentercomparerversion.txt'
GITHUB_PROFILE = 'https://github.com/hxz393'
GITHUB_URL = 'https://github.com/hxz393/ConfigCenterComparer'
# 设置菜单下拉列表
CONFIG_CENTER_LIST = ['Apollo', 'Nacos',]
APOLLO_NAME_LIST = ['AppId', 'Name',]
# 默认配置
DEFAULT_CONFIG_MAIN = {
    'lang': 'English',  # zh-cht en zh-chs
    'config_center': 'Apollo',
    'apollo_name': 'AppId',
    'fix_name_before': '',
    'fix_name_after': '',
    'fix_name_left': '',
    'fix_name_right': '',
}
DEFAULT_CONFIG_CONNECTION = {
    'PRO_CONFIG': {
        'mysql_on': False,
        'mysql': {
            'host': '',
            'port': '',
            'user': '',
            'password': '',
            'db': '',
        },
        'ssh_on': False,
        'ssh': {
            'hostname': '',
            'port': '',
            'username': '',
            'password': '',
        }
    },
    'PRE_CONFIG': {
        'mysql_on': False,
        'mysql': {
            'host': '',
            'port': '',
            'user': '',
            'password': '',
            'db': '',
        },
        'ssh_on': False,
        'ssh': {
            'hostname': '',
            'port': '',
            'username': '',
            'password': '',
        }
    },
    'TEST_CONFIG': {
        'mysql_on': False,
        'mysql': {
            'host': '',
            'port': '',
            'user': '',
            'password': '',
            'db': '',
        },
        'ssh_on': False,
        'ssh': {
            'hostname': '',
            'port': '',
            'username': '',
            'password': '',
        }
    },
    'DEV_CONFIG': {
        'mysql_on': False,
        'mysql': {
            'host': '',
            'port': '',
            'user': '',
            'password': '',
            'db': '',
        },
        'ssh_on': False,
        'ssh': {
            'hostname': '',
            'port': '',
            'username': '',
            'password': '',
        }
    },
}
# SQL 查询语句
SQL_TEST_MYSQL = "SELECT VERSION()"
SQL_CONFIG_APOLLO_ID = """
SELECT
  n.AppId,
  n.NamespaceName,
  i.`Key`,
  i.`Value`,
  i.DataChange_LastTime
FROM
  Item i
INNER JOIN Namespace n ON i.NamespaceId = n.Id
WHERE
  i.IsDeleted = 0
  AND i.`Key` != '';
"""
SQL_CONFIG_APOLLO_NAME = """
SELECT
  App.Name,
  n.NamespaceName,
  i.`Key`,
  i.`Value`,
  i.DataChange_LastTime
FROM
  Item i
INNER JOIN Namespace n ON i.NamespaceId = n.Id
INNER JOIN App ON n.AppId = App.AppId
WHERE
  i.IsDeleted = 0
  AND i.`Key` != '';
"""
SQL_CONFIG_NACOS = """
SELECT
  data_id,
  group_id,
  content,
  gmt_modified
FROM
  config_info
"""
# 表头对应关系设置
COL_INFO = {
    "name": {"col": 0},
    "group": {"col": 1},
    "key": {"col": 2},
    "pro_value": {"col": 3},
    "pro_time": {"col": 4},
    "pre_value": {"col": 5},
    "pre_time": {"col": 6},
    "test_value": {"col": 7},
    "test_time": {"col": 8},
    "dev_value": {"col": 9},
    "dev_time": {"col": 10},
    "consistency": {"col": 11},
    "skip": {"col": 12},

}
# 表格颜色代码
COLOR_CONSISTENCY_FULLY = '#ccffcc'
COLOR_CONSISTENCY_PARTIALLY = '#bbddff'
COLOR_DEFAULT = '#ffffff'
COLOR_EMPTY = '#ffdbcd'
COLOR_SKIP = '#e0e0e0'
COLOR_HIGHLIGHT = '#ffff66'
