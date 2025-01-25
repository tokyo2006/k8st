import subprocess
import json
from ..constants import Constants
from ..utils.console import ConsoleOutput
from ..logger_confiuration import logger

class KubeService:
    def __init__(self):
        self.min_version = Constants.MIN_KUBECTL_VERSION
        if not self.is_kube_installed():
            ConsoleOutput.print_red("Kubectl is not installed!Please install kubectl first.")
            exit(1)
        if not self.check_kubectl_version():
            ConsoleOutput.print_red(f"Kubectl version is lower than the minimum required version {self.min_version}. Please upgrade kubectl.")
            exit(1)
    
    def list_context(self):
        try:
            result = subprocess.run(['kubectl', 'config', 'get-contexts', '-o', 'name'], capture_output=True, text=True, check=True)
            contexts = result.stdout.splitlines()
            return contexts
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red("Error fetching kubectl contexts, please check your kubectl configuration in ~/.kube.")
            logger.error(f"Error fetching kubectl contexts: {e.stderr}")
            return []
        
    def is_kube_installed(self):
        try:
            subprocess.run(['kubectl', 'help'], capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            return False
    
    def set_context(self,context):
        try:
            subprocess.run(['kubectl', 'config', 'use-context', context], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error setting kubectl context")
            logger.error(f"Error setting kubectl context: {e.stderr}")
            return False
        return True
    
    def check_kubectl_version(self):
        try:
            result = subprocess.run(['kubectl', 'version', '--client','-o','json'], capture_output=True, text=True, check=True)
            kube_version = json.loads(result.stdout)
            version = kube_version['clientVersion']['gitVersion'].replace("v", "")
            return self.compare_versions(version, self.min_version)
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error checking kubectl version.")
            logger.error(f"Error checking kubectl version: {e.stderr}")
            return False

    def compare_versions(self, current_version, min_version):
        current_version_parts = list(map(int, current_version.split(".")))
        min_version_parts = list(map(int, min_version.split(".")))
        return current_version_parts >= min_version_parts

    def get_current_context(self):
        try:
            result = subprocess.run(['kubectl', 'config', 'current-context'], capture_output=True, text=True, check=True)
            current_context = result.stdout.strip()
            return current_context
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error fetching current kubectl context.")
            logger.error(f"Error fetching current kubectl context: {e.stderr}")
            return None
        
    def get_service_release_versions(self, release_name, namespace='default'):
        try:
            result = subprocess.run(['kubectl', 'get', 'secrets', '-n', namespace, '-o', 'jsonpath={.items[*].metadata.name}'], capture_output=True, text=True, check=True)
            secrets = result.stdout.split()
            release_versions = [secret for secret in secrets if secret.startswith(f"sh.helm.release.v1.{release_name}")]
            if logger:
                for version in release_versions:
                    logger.debug(f"Found release version: {version}")
            return release_versions
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error fetching release versions.")
            logger.error(f"Error fetching release versions: {e.stderr}")
            return []

    def get_pods_by_deployment(self, deployment_name, app_label ,namespace='default'):
        try:
            deployment_name = deployment_name.rsplit('-', 1)[0]
            command = ['kubectl', 'get', 'pods', '-n', namespace, '-l', f'app={app_label}', '-o', 'jsonpath={.items[*].metadata.name}']
            logger.debug(f"Running command: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            pods = result.stdout.split()
            logger.debug(f"Found pods for deployment {deployment_name}: {pods}")
            return pods
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error fetching pods for deployment {deployment_name}")
            logger.error(f"Error fetching pods for deployment {deployment_name}: {e.stderr}")
            return []
    
    def debug_pod(self, pod_name, image,container_name,namespace='default'):
        try:
            ConsoleOutput.print_green(f"Debugging pod {pod_name} in namespace {namespace}")
            command = ['kubectl', 'debug', '-it', pod_name, '-n', namespace, f'--image={image}', f'--target={container_name}','--','sh']
            logger.debug(f"Running command: {' '.join(command)}")
            subprocess.run(['kubectl', 'debug', '-it', pod_name, '-n', namespace, f'--image={image}', f'--target={container_name}','--','sh'], check=True)
           
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error debugging pod {pod_name}")
            logger.error(f"Error debugging pod {pod_name}: {e.stderr}")

    def get_containers_by_pod(self, pod_name, namespace='default'):
        try:
            result = subprocess.run(['kubectl', 'get', 'pod', pod_name, '-n', namespace, '-o', 'jsonpath={.spec.containers[*].name}'], capture_output=True, text=True, check=True)
            containers = result.stdout.split()
            return containers
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error fetching containers for pod {pod_name}")
            logger.error(f"Error fetching containers for pod {pod_name}: {e.stderr}")
            return []

    def list_deployments(self, namespace='default'):
        try:
            result = subprocess.run(['kubectl', 'get', 'deployments', '-n', namespace, '-o', 'json'], capture_output=True, text=True, check=True)
            deployments = json.loads(result.stdout)
            deployment_list = []
            for item in deployments['items']:
                deployment = {}
                name = item['metadata']['name']
                app_label = item['spec']['template']['metadata']['labels'].get('app', 'N/A')
                deployment['name'] = name
                deployment['label'] = app_label
                deployment_list.append(deployment)
            logger.debug(f"Found deployments in namespace {namespace}: {deployment_list}")
            return deployment_list
        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error fetching deployments in namespace {namespace}")
            logger.error(f"Error fetching deployments in namespace {namespace}: {e.stderr}")
            return []

    def exec_pod(self, pod_name, container_name, namespace='default'):
        try:
            command = ['kubectl', 'exec', '-it', pod_name, '-n', namespace, '-c', container_name, '--', '/bin/sh', '-c', 'TERM=xterm-256color; [ -x /bin/bash ] && bash || sh']
            subprocess.run(command, capture_output=True, text=True, check=True)

        except subprocess.CalledProcessError as e:
            ConsoleOutput.print_red(f"Error attached pod {pod_name}'s container {container_name}")
            logger.error(f"Error attached pod {pod_name}'s container {container_name}: {e.stderr}")