import unittest
from unittest.mock import patch, Mock
import json
import base64
import subprocess
from k8st.services.kube_service import KubeService
from k8st.utils.console import ConsoleOutput

class TestKubeService(unittest.TestCase):
    def setUp(self):
        self.kube_service = KubeService()
        self.test_secret_name = "test-secret"
        self.test_namespace = "test-namespace"

    @patch('subprocess.run')
    def test_get_secret_values_success(self, mock_run):
        # 准备测试数据
        test_data = {
            "data": {
                "username": base64.b64encode("admin".encode()).decode(),
                "password": base64.b64encode("secret123".encode()).decode()
            }
        }
        
        # 配置 mock
        mock_process = Mock()
        mock_process.stdout = json.dumps(test_data)
        mock_run.return_value = mock_process

        # 执行测试
        result = self.kube_service.get_secret_values(self.test_secret_name, self.test_namespace)

        # 验证结果
        self.assertEqual(result["username"], "admin")
        self.assertEqual(result["password"], "secret123")
        mock_run.assert_called_once_with(
            ['kubectl', 'get', 'secret', self.test_secret_name, '-n', self.test_namespace, '-o', 'json'],
            capture_output=True, text=True, check=True
        )

    @patch('subprocess.run')
    def test_get_secret_values_empty_data(self, mock_run):
        # 准备测试数据
        test_data = {"data": {}}
        
        # 配置 mock
        mock_process = Mock()
        mock_process.stdout = json.dumps(test_data)
        mock_run.return_value = mock_process

        # 执行测试
        result = self.kube_service.get_secret_values(self.test_secret_name)

        # 验证结果
        self.assertEqual(result, {})

    @patch('subprocess.run')
    def test_get_secret_values_command_error(self, mock_run):
        # 配置 mock 抛出异常
        mock_run.side_effect = subprocess.CalledProcessError(1, [], stderr="Command failed")

        # 配置 ConsoleOutput mock
        with patch.object(ConsoleOutput, 'print_red') as mock_print:
            # 执行测试
            result = self.kube_service.get_secret_values(self.test_secret_name)

            # 验证结果
            self.assertEqual(result, {})
            mock_print.assert_called_once_with(
                f"Error fetching secret values for {self.test_secret_name}"
            )

    @patch('subprocess.run')
    def test_get_secret_values_invalid_base64(self, mock_run):
        # 准备测试数据
        test_data = {
            "data": {
                "invalid": "aW52YWxpZF9iYXNlNjQ="
            }
        }
        
        # 配置 mock
        mock_process = Mock()
        mock_process.stdout = json.dumps(test_data)
        mock_run.return_value = mock_process

        # 执行测试
        result = self.kube_service.get_secret_values(self.test_secret_name)
        print(result)
        # 验证结果
        self.assertEqual(result, {'invalid': 'invalid_base64'})

if __name__ == '__main__':
    unittest.main()