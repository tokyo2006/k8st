import subprocess
from ..utils.console import ConsoleOutput

def install_required_package_manager(system):
    """安装系统所需的包管理器"""
    if system == 'darwin':
        try:
            subprocess.run(['brew', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            ConsoleOutput.print_yellow("Installing Homebrew...")
            install_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            subprocess.run(install_cmd, shell=True, check=True)
            ConsoleOutput.print_green("Homebrew installed successfully")
    elif system == 'windows':
        try:
            subprocess.run(['choco', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            ConsoleOutput.print_yellow("Installing Chocolatey...")
            install_cmd = [
                'powershell',
                '-Command',
                'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))'
            ]
            subprocess.run(install_cmd, check=True)
            ConsoleOutput.print_green("Chocolatey installed successfully")