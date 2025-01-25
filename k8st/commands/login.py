from ..services.aws_service import AWSService
from ..utils.file import FileUtils
from ..utils.console import ConsoleOutput
from ..logger_confiuration import logger
from ..constants import Constants
from ..core.command_registry import command

@command(name='login', services=[AWSService])
def login(args,aws_service: AWSService) -> None:
    ConsoleOutput.print_green("Logging in to AWS SSO...")
    config = FileUtils.read_config_file(Constants.CONFIG_FILE_PATH)
    if not config or not config.get("initialized"):
        ConsoleOutput.print_red("Tool is not initialized. Please run 'k8st init' to initialize the tool.")
        return
    selected_profiles = config.get("selected_profiles")
    if not selected_profiles:
        ConsoleOutput.print_red("No AWS profiles selected. Please run 'k8st init' to select AWS profiles.")
        return
    aws_service.login_profiles(selected_profiles)
    ConsoleOutput.print_green("AWS SSO login successful.")
