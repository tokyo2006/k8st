import unittest
from unittest.mock import patch, MagicMock
import argparse
from k8st.main import create_parser
from k8st.core.command_registry import command_registry

class TestCreateParser(unittest.TestCase):
    def setUp(self):
        # 模拟命令注册表
        self.mock_func = MagicMock()
        self.mock_service = MagicMock()
        command_registry.clear()
        command_registry['test_command'] = {
            'func': self.mock_func,
            'services': [self.mock_service]
        }

    def test_create_parser_basic_arguments(self):
        """测试基本参数的创建"""
        config = {'commands': []}
        parser = create_parser(config)
        
        # 测试基本参数
        args = parser.parse_args(['--debug'])
        self.assertTrue(args.debug)
        self.assertFalse(args.reload)
        self.assertEqual(args.namespace, 'default')

        args = parser.parse_args(['--reload'])
        self.assertFalse(args.debug)
        self.assertTrue(args.reload)

        args = parser.parse_args(['--namespace', 'test-ns'])
        self.assertEqual(args.namespace, 'test-ns')

    def test_create_parser_with_command(self):
        """测试带命令的解析器创建"""
        config = {
            'commands': [{
                'name': 'test_command',
                'help': 'Test command help'
            }]
        }
        parser = create_parser(config)
        
        args = parser.parse_args(['test_command'])
        self.assertEqual(args.command, 'test_command')
        self.assertEqual(args.func, self.mock_func)
        self.assertEqual(args.services, [self.mock_service])

    def test_create_parser_with_command_arguments(self):
        """测试带参数的命令解析器创建"""
        config = {
            'commands': [{
                'name': 'test_command',
                'help': 'Test command help',
                'arguments': [
                    {
                        'name': '--test-arg',
                        'help': 'Test argument help',
                        'type': str,
                        'required': True
                    },
                    {
                        'name': '--flag',
                        'help': 'Test flag help',
                        'action': 'store_true'
                    }
                ]
            }]
        }
        parser = create_parser(config)
        
        # 测试必需参数
        with self.assertRaises(SystemExit):
            parser.parse_args(['test_command'])
        
        # 测试有效参数
        args = parser.parse_args(['test_command', '--test-arg', 'value', '--flag'])
        self.assertEqual(args.command, 'test_command')
        self.assertEqual(args.test_arg, 'value')
        self.assertTrue(args.flag)

    def test_create_parser_invalid_command(self):
        """测试无效命令处理"""
        config = {
            'commands': [{
                'name': 'test_command',
                'help': 'Test command help'
            }]
        }
        parser = create_parser(config)
        
        with self.assertRaises(SystemExit):
            parser.parse_args(['invalid_command'])

    def test_create_parser_help_message(self):
        """测试帮助信息生成"""
        config = {
            'commands': [{
                'name': 'test_command',
                'help': 'Test command help',
                'arguments': [{
                    'name': '--test-arg',
                    'help': 'Test argument help',
                    'type': str
                }]
            }]
        }
        parser = create_parser(config)
        
        with patch('sys.stdout') as mock_stdout:
            with self.assertRaises(SystemExit):
                parser.parse_args(['--help'])
            # 验证帮助信息包含命令描述
            help_output = mock_stdout.write.call_args_list[0][0][0]
            self.assertIn('K8s Tool', help_output)
            self.assertIn('test_command', help_output)

if __name__ == '__main__':
    unittest.main()