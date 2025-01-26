import inquirer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from ..services.helm_service import HelmService
from ..services.kube_service import KubeService
from ..logger_confiuration import logger
from ..services.resource_service import ResourceService
from ..utils.console import ConsoleOutput
from ..core.command_registry import command

@command(name='debug', services=[KubeService, HelmService])
def debug_pod(args, kube_service: KubeService, helm_service: HelmService) -> None:
    try:
        selected_resources = get_selected_resources(kube_service, helm_service,args.reload)
        if not selected_resources:
            return
        selected_pod = selected_resources['pod']    
        selected_container = selected_resources['container']
        # Debug the selected pod
        kube_service.debug_pod(selected_pod, args.image, selected_container, args.namespace)
    except Exception as e:
        logger.error(f"An error occurred during pod debugging: {e}")

@command(name='exec', services=[KubeService, HelmService])
def exec_pod(args, kube_service: KubeService, helm_service: HelmService) -> None:
    try:
        selected_resources = get_selected_resources(kube_service, helm_service)
        if not selected_resources:
            return
        selected_pod = selected_resources['pod']
        selected_container = selected_resources['container']
        # Debug the selected pod
        kube_service.exec_pod(selected_pod, selected_container, args.namespace)
    except Exception as e:
        logger.error(f"An error occurred during pod debugging: {e}")


def get_selected_resources(kube_service: KubeService, helm_service: HelmService, reload=False):
    try:
        # Get release list
        resource_service = ResourceService(kube_service, helm_service)
        deployments = resource_service.get_deployments(reload)
        deployment_names = [deployment['name'] for deployment in deployments]
        
        # Prompt user to select release
        selected_deployment = prompt_user_for_deployment(deployment_names)
        if not selected_deployment:
            return

        app_label = None
        for deployment in deployments:
            if deployment['name'] == selected_deployment:
                app_label = deployment['label']
                logger.debug(f"The app label for deployment '{selected_deployment}' is: {app_label}")
                break
        
        pods = kube_service.get_pods_by_deployment(selected_deployment, app_label)
        if not pods:
            ConsoleOutput.print_yellow(f"No pods found for deployment: {selected_deployment}, please check kubernetes cluster connection!")
            return

        selected_pod = prompt_user_for_pod(pods)
        if not selected_pod:
            return

        containers = kube_service.get_containers_by_pod(selected_pod)
        selected_container = prompt_user_for_container(containers)
        if not selected_container:
            return None
        return {'pod': selected_pod, 'container': selected_container}
    except Exception as e:
        logger.error(f"An error occurred during pod debugging: {e}")
        return None

def prompt_user_for_deployment(deployment_names):
    deployment_completer = FuzzyCompleter(WordCompleter(deployment_names, ignore_case=True, sentence=True))
    selected_deployment = prompt("Select Service Release: ", completer=deployment_completer)
    if selected_deployment not in deployment_names:
        ConsoleOutput.print_red(f"Invalid release: {selected_deployment}")
        return None
    return selected_deployment

def prompt_user_for_pod(pods):
    questions = [
        inquirer.List('pod', message="Select pod to debug", choices=pods),
    ]
    answers = inquirer.prompt(questions)
    selected_pod = answers['pod']
    ConsoleOutput.print_green(f"Selected pod: {selected_pod}")
    return selected_pod

def prompt_user_for_container(containers):
    questions = [
        inquirer.List('container', message="Select container to debug", choices=containers),
    ]
    answers = inquirer.prompt(questions)
    selected_container = answers['container']
    if selected_container not in containers:
        ConsoleOutput.print_red(f"Invalid container: {selected_container}")
        return None
    return selected_container