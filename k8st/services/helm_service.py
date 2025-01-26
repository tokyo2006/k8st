import subprocess
import json
from ..utils.console import ConsoleOutput
from ..logger_confiuration import logger
from .required_package import install_required_package_manager      
import platform

class HelmService:
    def __init__(self):
        if not self.is_helm_installed():
            install_helm(self)

    def install_helm(self):
        """Install Helm based on the operating system"""
        try:
            system = platform.system().lower()
            install_required_package_manager(system)
            if system == "darwin":  # macOS
                # 安装 helm
                subprocess.run(['brew', 'install', 'helm'], check=True)
            elif system == "linux":
                # 使用官方脚本安装 Helm
                ConsoleOutput.print_yellow("Installing Helm using official script...")
                subprocess.run(['curl', '-fsSL', '-o', 'get_helm.sh', 'https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3'], check=True)
                subprocess.run(['chmod', '700', 'get_helm.sh'], check=True)
                subprocess.run(['./get_helm.sh'], check=True)
                subprocess.run(['rm', 'get_helm.sh'], check=True)
                ConsoleOutput.print_green("Helm installed successfully")
            elif system == "windows":
                # 使用 chocolatey 安装 helm
                ConsoleOutput.print_yellow("Installing Helm using Chocolatey...")
                subprocess.run(['choco', 'install', 'kubernetes-helm', '-y'], check=True)
                ConsoleOutput.print_green("Helm has been installed. Please restart your terminal to use helm command.")
            else:
                raise Exception(ConsoleOutput.print_red(f"Unsupported operating system: {system}"))
            
            logger.info("Helm installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            error_message = f"Failed to install Helm: {str(e)}"
            logger.error(error_message)
            raise Exception(ConsoleOutput.print_red(error_message))

    # the result of helm list is a json string, it will contain
    def list_releases(self, namespace=None):
        try:
            # Build base command with common arguments
            command = ['helm', 'list', '-d', '-o', 'json', '-m', '1024']
            # Add namespace-specific or all-namespaces flag
            if namespace:
                command.extend(['-n', namespace])
            else:
                command.append('-a')
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing helm list: {e.stderr}")
            raise Exception(ConsoleOutput.print_red(f"Error executing helm list: {e.stderr}"))
            
    def rollback_release(self, release_name, revision):
        try:
            command = ['helm', 'rollback', release_name, revision]
            subprocess.run(command, check=True)
            success_message = f"Successfully rolled back {release_name} to revision {revision}"
            ConsoleOutput.print_green(success_message)
            logger.info(success_message)
        except subprocess.CalledProcessError as e:
            error_message = f"Error rolling back release {release_name} to revision {revision}!"
            ConsoleOutput.print_red(error_message)
            logger.error(f"{error_message} Details: {e.stderr}")
    
    def is_helm_installed(self):
        try:
            subprocess.run(['helm', 'version'], capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_release_versions(self, release_name, ns="default"):
        try:
            command = ['helm', 'history', release_name, '-n', ns, '-o', 'json']
            result = subprocess.run(command,capture_output=True, text=True, check=True)
            versions = json.loads(result.stdout)
            return versions
        except subprocess.CalledProcessError as e:
            error_message = f"Error executing helm history for release {release_name} in namespace {ns}"
            ConsoleOutput.print_red(error_message)
            logger.error(f"{error_message}. Details: {e.stderr}")
            raise
        except json.JSONDecodeError as e:
            error_message = f"Error parsing JSON output for release {release_name} in namespace {ns}"
            ConsoleOutput.print_red(error_message)
            logger.error(f"{error_message}. Details: {e}")
            raise
