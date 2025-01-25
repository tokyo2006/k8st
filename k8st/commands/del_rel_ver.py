import inquirer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from ..services.helm_service import HelmService
from ..services.kube_service import KubeService
from ..logger_confiuration import logger
from ..services.resource_service import ResourceService
from ..utils.console import ConsoleOutput
from ..core.command_registry import command

@command(name='del-rel-ver', services=[KubeService, HelmService])
def delete_release_version_secret(args, kube_service: KubeService, helm_service: HelmService) -> None:
    """Delete a specific version secret of a release."""
    try:
        # Get release list
        resource_service = ResourceService(kube_service=kube_service, helm_service=helm_service)
        releases = resource_service.get_releases(args.reload)
        release_names = [release['name'] for release in releases]

        # Prompt user to select release
        release_completer = FuzzyCompleter(WordCompleter(release_names, ignore_case=True, sentence=True))
        selected_release = prompt("Select Service Release: ", completer=release_completer)
        if selected_release not in release_names:
            ConsoleOutput.print_red(f"Invalid release: {selected_release}")
            return

        release_versions = kube_service.get_service_release_versions(selected_release)
        questions = [
            inquirer.List('version',
                          message="Select version secret to delete",
                          choices=release_versions,
                          ),
        ]
        answers = inquirer.prompt(questions)
        selected_release_version = answers['version']
        if selected_release_version not in release_versions:
            ConsoleOutput.print_red(f"Invalid version: {selected_release_version}")
            return

        # Perform deletion
        logger.info(f"Delete {selected_release} version {selected_release_version}")
        # Assuming there's a method to delete the version secret
        # kube_service.delete_release_version_secret(selected_release, selected_release_version)
        ConsoleOutput.print_green(f"Successfully deleted {selected_release_version}")

    except Exception as e:
        logger.error(f"Failed to delete release version secret: {e}")
        ConsoleOutput.print_red("An error occurred while deleting the release version secret.")
