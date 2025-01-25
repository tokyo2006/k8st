from colorama import Fore, Style, init
from ..constants import Constants

# Initialize colorama
init(autoreset=True)

class ConsoleOutput:
    """处理控制台输出格式化的工具类"""
    
    @staticmethod
    def print_red(message: str) -> None:
        """打印红色错误信息"""
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")
        ConsoleOutput.print_log_info()

    @staticmethod
    def print_green(message: str) -> None:
        """打印绿色成功信息"""
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

    @staticmethod
    def print_yellow(message: str) -> None:
        """打印黄色警告信息"""
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

    @staticmethod
    def print_blue(message: str) -> None:
        """打印蓝色信息"""
        print(f"{Fore.BLUE}{message}{Style.RESET_ALL}")

    @staticmethod
    def print_cyan(message: str) -> None:
        """打印青色信息"""
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

    @staticmethod
    def print_magenta(message: str) -> None:
        """打印品红色信息"""
        print(f"{Fore.MAGENTA}{message}{Style.RESET_ALL}")

    @staticmethod
    def print_log_info() -> None:
        """打印日志文件位置信息"""
        print(f"{Fore.YELLOW}For more information, check the log file at {Constants.LOG_FILE_PATH}{Style.RESET_ALL}")