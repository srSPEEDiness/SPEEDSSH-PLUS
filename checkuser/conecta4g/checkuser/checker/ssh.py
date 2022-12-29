import typing as t
import os

class SSHManager:
    def count_connections(self, username: str) -> int:
        command = 'ps -u %s' % username
        result = os.popen(command).readlines()
        return len([line for line in result if 'sshd' in line])

    def get_pids(self, username: str) -> t.List[int]:
        command = 'ps -u %s' % username
        result = os.popen(command).readlines()
        return [int(line.split()[0]) for line in result if 'sshd' in line]

    def kill_connection(self, username: str) -> None:
        pids = self.get_pids(username)
        for pid in pids:
            os.kill(pid, 9)
