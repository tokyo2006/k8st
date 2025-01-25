from typing import Callable, Dict, Any

command_registry: Dict[str, Dict[str, Any]] = {}

def command(name: str, services: Dict[str, Any]) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        command_registry[name] = {'func': func, 'services': services}
        return func
    return decorator
