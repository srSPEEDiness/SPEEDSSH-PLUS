import subprocess
from abc import ABCMeta, abstractmethod


class CommandExecutor(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, command: str) -> str:
        raise NotImplementedError


class CommandExecutorImpl(CommandExecutor):
    def execute(self, command: str) -> str:
        data = subprocess.check_output(
            command,
            shell=True,
            timeout=1,
        )
        return data.decode('utf-8')
