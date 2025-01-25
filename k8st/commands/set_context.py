from ..services.kube_service import KubeService
from ..utils.console import ConsoleOutput
from ..logger_confiuration import logger
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from ..core.command_registry import command

@command(name='ctx', services=[KubeService])
def set_context(args, kube_service: KubeService) -> None:
    try:
        contexts = kube_service.list_context()
        if not contexts:
            logger.error("No Kubernetes contexts found. Please configure your kubectl.")
            raise ValueError("No contexts available")
        
        # Prompt user to select context using prompt_toolkit
        context_completer = FuzzyCompleter(WordCompleter(contexts, ignore_case=True, sentence=True))
        selected_context = prompt("Select Kubernetes context: ", completer=context_completer)
        
        logger.info(f"Selected kubernetes context: {selected_context}")
        kube_service.set_context(selected_context)
    except Exception as e:
        logger.exception("An error occurred while setting Kubernetes context")
        ConsoleOutput.print_red(str(e))
        raise
