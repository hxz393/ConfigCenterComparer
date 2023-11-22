import unittest

from config.settings import CONFIG_APOLLO_PATH, CONFIG_NACOS_PATH
from module.config_path_get import config_path_get


class TestConfigPathGet(unittest.TestCase):
    def test_valid_apollo(self):
        """ 测试有效的 Apollo 配置 """
        config = {'config_center': 'Apollo'}
        expected_path = CONFIG_APOLLO_PATH
        self.assertEqual(config_path_get(config), expected_path)

    def test_valid_nacos(self):
        """ 测试有效的 Nacos 配置 """
        config = {'config_center': 'Nacos'}
        expected_path = CONFIG_NACOS_PATH
        self.assertEqual(config_path_get(config), expected_path)

    def test_invalid_config_center(self):
        """ 测试无效的配置中心类型 """
        config = {'config_center': 'InvalidCenter'}
        self.assertIsNone(config_path_get(config))

    def test_empty_config(self):
        """ 测试空配置字典 """
        config = {}
        self.assertIsNone(config_path_get(config))

    def test_none_input(self):
        """ 测试 None 作为输入 """
        self.assertIsNone(config_path_get(None))

    def test_non_dict_input(self):
        """ 测试非字典类型输入 """
        config = ['not', 'a', 'dict']
        self.assertIsNone(config_path_get(config))


if __name__ == '__main__':
    unittest.main()
