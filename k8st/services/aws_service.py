import os
import configparser
import subprocess
from ..utils.console import ConsoleOutput
from ..logger_confiuration import logger

class AWSService:
    def __init__(self):
        self.aws_config_path = os.path.expanduser("~/.aws/config")

    def get_profile_list(self):
        if not os.path.exists(self.aws_config_path):
            ConsoleOutput.print_red("AWS config file not found. Please run 'aws configure' to set up your AWS credentials.")
            return []

        config = configparser.ConfigParser()
        config.read(self.aws_config_path)

        profiles = [section.replace('profile ', '') for section in config.sections() if section.startswith('profile ')]
        return profiles
    
    def login_profiles(self, profiles):
        for profile in profiles:
            ConsoleOutput.print_green(f"Logging in to AWS SSO for profile: {profile}")
            try:
                command = ['aws', 'sso', 'login', '--profile', profile]
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                ConsoleOutput.print_red(f"Error logging in to AWS SSO for profile {profile}!")
                logger.error(f"Error logging in to AWS SSO for profile {profile}: {e}")
