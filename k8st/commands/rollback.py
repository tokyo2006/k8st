import inquirer
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from ..services.helm_service import HelmService
from ..services.kube_service import KubeService
from ..logger_confiuration import logger
from ..services.resource_service import ResourceService
from ..utils.console import ConsoleOutput
from ..core.command_registry import command

@command(name='rollback', services=[KubeService, HelmService])
def rollback_release(args, kube_service: KubeService, helm_service: HelmService) -> None:
    try:
        # 获取发布列表
        resource_service = ResourceService(kube_service, helm_service)
        releases = resource_service.get_releases(args.reload)
        release_names = [release['name'] for release in releases]
        logger.debug(f"Fetched {len(release_names)} releases")

        # 提示用户选择发布
        release_completer = FuzzyCompleter(WordCompleter(release_names, ignore_case=True))
        selected_release = prompt("Select Helm release: ", completer=release_completer)
        if selected_release not in release_names:
            ConsoleOutput.print_red(f"Invalid release: {selected_release}")
            return
        logger.debug(f"Selected release: {selected_release}")

        # 获取发布版本
        versions = helm_service.get_release_versions(selected_release)
        version_numbers = [str(version['revision']) for version in versions]
        logger.debug(f"Fetched {len(version_numbers)} versions for release {selected_release}")

        # 提示用户选择版本
        questions = [
            inquirer.List('version',
                          message="Select version to rollback to",
                          choices=version_numbers,
                          ),
        ]
        answers = inquirer.prompt(questions)
        selected_version = answers['version']
        if selected_version not in version_numbers:
            ConsoleOutput.print_red(f"Invalid version: {selected_version}")
            return
        logger.debug(f"Selected version: {selected_version}")

        # 执行回滚
        helm_service.rollback_release(selected_release, selected_version, ns=args.namespace)
        logger.info(f"Rolled back {selected_release} to version {selected_version}")

    except Exception as e:
        logger.error(f"Failed to rollback release: {e}")
        ConsoleOutput.print_red("An error occurred during rollback.")
