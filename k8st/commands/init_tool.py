import inquirer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
import os
import time
from ..services.aws_service import AWSService
from ..utils.console import ConsoleOutput
from ..utils.file import FileUtils
from ..logger_confiuration import logger
from ..constants import Constants
from ..core.command_registry import command

@command(name='init', services=[AWSService])
def initialize_tool(args, aws_service: AWSService) -> None:
    ConsoleOutput.print_green("Initializing tool...")
    # Get AWS profiles
    profiles = aws_service.get_profile_list()
    if not profiles:
        ConsoleOutput.print_red("No AWS profiles found. Please run 'aws configure' to set up your AWS credentials.")
        return

    # Prompt user to select profiles using prompt_toolkit
    profile_completer = FuzzyCompleter(WordCompleter(profiles, ignore_case=True, sentence=True))
    selected_profiles = []
    while True:
        profile = prompt("Select AWS profile (type 'done' to finish): ", completer=profile_completer)
        if profile.lower() == 'done':
            break
        if profile in profiles and profile not in selected_profiles:
            selected_profiles.append(profile)
            ConsoleOutput.print_green(f"Selected profile: {profile}")
        else:
            ConsoleOutput.print_red(f"Invalid profile: {profile}")
    logger.debug(f"Selected profiles: {selected_profiles}")
    # Save ldap ussername
    ldap_username = input("Enter your ldap username: ")
    logger.debug(f"Selected ldap username: {ldap_username}")
    # Perform initialization operations here
    config_data = {
        "initialized": True,
        "timestamp": time.time(),
        "ldap_username": ldap_username, 
        "selected_profiles": selected_profiles
    }
    os.makedirs(os.path.dirname(Constants.CONFIG_FILE_PATH), exist_ok=True)
    FileUtils.write_config_file(Constants.CONFIG_FILE_PATH, config_data)
    ConsoleOutput.print_green("Tool initialized successfully.")

