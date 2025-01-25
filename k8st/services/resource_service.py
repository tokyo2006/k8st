from ..logger_confiuration import logger
from .helm_service import HelmService
from .kube_service import KubeService
from ..utils.console import ConsoleOutput
from ..utils.file import FileUtils

class ResourceService:
    def __init__(self, kube_service: KubeService, helm_service: HelmService = None):
        self.kube_service = kube_service
        self.helm_service = helm_service

    def get_releases(self, reload=False) -> dict:
        context = self.kube_service.get_current_context()
        temp_file_path = FileUtils.get_temp_file_path(f'helm_releases_{context}.json')
        
        try:
            releases = FileUtils.read_from_file(temp_file_path)
        except Exception as e:
            ConsoleOutput.print_red(f"Error reading file {temp_file_path}: {e}")
            releases = None

        if releases is not None and not reload:
            logger.debug(f"Reading Helm releases from {temp_file_path}")
        else:
            logger.debug("Fetching Helm releases using helm list")
            try:
                releases = self.helm_service.list_releases()
                FileUtils.write_to_file(temp_file_path, releases)
            except Exception as e:
                ConsoleOutput.print_red(f"Error fetching Helm releases: {e}")
                return {}

        return releases if releases is not None else {}

    def get_deployments(self, reload=False) -> dict:
        context = self.kube_service.get_current_context()
        temp_file_path = FileUtils.get_temp_file_path(f'k8s_deployments_{context}.json')
        
        try:
            deployments = FileUtils.read_from_file(temp_file_path)
        except Exception as e:
            ConsoleOutput.print_red(f"Error reading file {temp_file_path}: {e}")
            logger.error(f"Error reading file {temp_file_path}: {e}")
            deployments = None

        if deployments is not None and not reload:
            logger.debug(f"Reading Kubernetes deployments from {temp_file_path}")
        else:
            logger.debug("Fetching Kubernetes deployments using kubectl")
            try:
                deployments = self.kube_service.list_deployments()
                FileUtils.write_to_file(temp_file_path, deployments)
            except Exception as e:
                ConsoleOutput.print_red(f"Error fetching Kubernetes deployments: {e}")
                logger.error(f"Error fetching Kubernetes deployments: {e}")
                return {}

        return deployments if deployments is not None else {}