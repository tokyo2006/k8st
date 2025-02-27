import argparse
import os
import yaml
from prompt_toolkit import prompt
from .logger_confiuration import logger
import logging
from .utils.console import ConsoleOutput
from .utils.file import FileUtils
from .constants import Constants
import importlib
from .core.command_registry import command_registry


def dynamic_import_commands():
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'k8st.commands.{filename[:-3]}'
            importlib.import_module(module_name)
            
def load_commands_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def create_parser(commands_config):
    parser = argparse.ArgumentParser(description="K8s Tool")
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug logging')
    parser.add_argument('--reload', '-r', action='store_true', help='Force fetch all resources from cluster')
    parser.add_argument('--namespace','-n', type=str, default='default', help='Kubernetes namespace (default: default)',required=False)
    subparsers = parser.add_subparsers(dest='command')
    for command in commands_config['commands']:
        subparser = subparsers.add_parser(command['name'], help=command['help'])
        subparser.set_defaults(func=command_registry[command['name']]['func'], services=command_registry[command['name']]['services'])
        if 'arguments' in command:
            for arg in command['arguments']:
                kwargs = {
                    'help': arg['help']
                }
                if arg.get('default'):
                    kwargs['default'] = arg['default']
                if arg.get('action'):
                    kwargs['action'] = arg['action']
                if arg.get('type'):
                    kwargs['type'] = arg['type']
                kwargs['required'] = bool(arg.get('required',False))
                name = arg['name']

                if not name.startswith('-'):
                    name = '--' + name.lstrip('-')
                if arg.get('short'):
                    short_name = arg['short']
                    if not short_name.startswith('-'):
                        short_name = '-' + short_name.lstrip('-')
                    subparser.add_argument(name, short_name, **kwargs)
                else:
                    subparser.add_argument(name, **kwargs)
    return parser

def exists_initialization():
    config = FileUtils.read_config_file(Constants.CONFIG_FILE_PATH)
    if not config or not config.get("initialized"):
        ConsoleOutput.print_red("Tool is not initialized. Please run 'k8st init' to initialize the tool.")
        return False
    else:
        return True

def set_log_level(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

def check_initialization(args):
    if args.command != 'init' and not exists_initialization():
        ConsoleOutput.print_red("Tool is not initialized. Please run 'k8st init' to initialize the tool.")
        exit(1)

def main():
    # Dynamically import all command modules
    dynamic_import_commands()
    
    # Command to function mapping
    command_config_path = os.path.join(os.path.dirname(__file__), 'commands_config.yaml')
    commands_config = load_commands_config(command_config_path)
    
    # Create argument parser from configuration
    parser = create_parser(commands_config)
    args = parser.parse_args()
    
    # Set logger level based on debug argument
    set_log_level(args)
    # Check if namespace exists
    # Check if the tool is initialized, except for the "init" command
    # check_initialization(args)
    
    if hasattr(args, 'func'):
        try:
            services = [service() for service in args.services]
            args.func(args, *services)
        except Exception as e:
            logger.error(f"Failed to create services: {e}")
            exit(1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
