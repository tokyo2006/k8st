import inquirer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from ..services.helm_service import HelmService
from ..services.kube_service import KubeService
from ..logger_confiuration import logger
from ..services.resource_service import ResourceService
from ..utils.console import ConsoleOutput
from ..core.command_registry import command


@command('secret',services=[KubeService,HelmService])
def get_secret(args,kube_service: KubeService, helm_service: HelmService):
    resource_service = ResourceService(kube_service, helm_service)
    secrets = resource_service.get_secrets()
    secret_names = [secret['name'] for secret in secrets]
    selected_secret_name = prompt_user_for_secret(secret_names)
    if selected_secret_name:
        # 从 secrets 列表中找到选中的 secret
        selected_secret = next((secret for secret in secrets if secret['name'] == selected_secret_name), None)
        if selected_secret and 'values' in selected_secret:
            for key, value in selected_secret['values'].items():  # 使用 .items() 来遍历字典
                ConsoleOutput.print_blue(f'{key}: {value}')

def prompt_user_for_secret(secrets):
    deployment_completer = FuzzyCompleter(WordCompleter(secrets, ignore_case=True, sentence=True))
    selected_secret = prompt("Select Secret: ", completer=deployment_completer)
    if selected_secret not in secrets:
        ConsoleOutput.print_red(f"Invalid secret: {selected_secret}")
        return None
    return selected_secret