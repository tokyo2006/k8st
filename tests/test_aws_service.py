import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from k8st.services.aws_service import AWSService
from k8st.utils.console import ConsoleOutput

class TestAWSService(unittest.TestCase):
    def setUp(self):
        self.aws_service = AWSService()
        self.mock_config_content = """
[default]
region = us-west-2

[profile dev]
region = us-east-1

[profile prod]
region = us-west-2

[profile staging]
region = eu-west-1
"""

    @patch('os.path.exists')
    def test_get_profile_list_no_config_file(self, mock_exists):
        """测试 AWS 配置文件不存在的情况"""
        mock_exists.return_value = False
        
        with patch.object(ConsoleOutput, 'print_red') as mock_print:
            profiles = self.aws_service.get_profile_list()
            
            self.assertEqual(profiles, [])
            mock_print.assert_called_once_with(
                "AWS config file not found. Please run 'aws configure' to set up your AWS credentials."
            )

    @patch('os.path.exists')
    @patch('configparser.ConfigParser')
    def test_get_profile_list_with_profiles(self, mock_config_parser, mock_exists):
        """测试正常读取配置文件中的 profiles"""
        mock_exists.return_value = True
        
        # Create mock parser instance
        mock_parser = MagicMock()
        mock_config_parser.return_value = mock_parser
        
        # Mock sections and their content
        mock_parser.sections.return_value = ['default', 'profile dev', 'profile prod', 'profile staging']
        
        profiles = self.aws_service.get_profile_list()
        
        self.assertEqual(len(profiles), 3)
        self.assertIn('dev', profiles)
        self.assertIn('prod', profiles)
        self.assertIn('staging', profiles)
        self.assertNotIn('default', profiles)

