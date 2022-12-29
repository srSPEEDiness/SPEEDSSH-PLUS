import socket
import re

from checkuser.data.executor import CommandExecutor
from checkuser.domain.connection import Connection, ConnectionKill


class SSHConnection(ConnectionKill):
    def __init__(self, executor: CommandExecutor):
        self.executor = executor

    def count(self, username: str) -> int:
        cmd = 'ps -u {} | grep sshd | wc -l'.format(username)
        return int(self.executor.execute(cmd))

    def kill(self, username: str) -> None:
        cmd = 'kill -9 $(ps -u {} | grep sshd | awk \'{{print $1}}\')'.format(username)
        self.executor.execute(cmd)

    def all(self) -> int:
        cmd = 'ps -ef | grep sshd | grep -v grep | grep -v root | wc -l'
        return int(self.executor.execute(cmd))


class AUXOpenVPNConnection:
    __socket: socket.socket

    def __init__(self, host: str = '127.0.0.1', port: int = 7505) -> None:
        self.host = host
        self.port = port

    def send(self, data: str) -> None:
        self.__socket.send(data.encode())

    def receive(self, size: int = 1024) -> str:
        data = b''
        chunk = self.__socket.recv(size)
        while chunk.count(b'\r\nEND\r\n') == 0:
            data += chunk
            chunk = self.__socket.recv(size)
        data += chunk
        return data.decode()

    def close(self) -> None:
        self.__socket.close()

    def __enter__(self) -> 'AUXOpenVPNConnection':
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.host, self.port))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class OpenVPNConnection(ConnectionKill):
    def __init__(self, connection: AUXOpenVPNConnection) -> None:
        self.connection = connection

    def count(self, username: str) -> int:
        try:
            with self.connection:
                self.connection.send('status\n')
                data = self.connection.receive()
                count = data.count(username)
                return count // 2 if count > 0 else 0
        except Exception:
            return 0

    def kill(self, username: str) -> None:
        with self.connection:
            self.connection.send('kill {}\n'.format(username))

    def all(self) -> int:
        try:
            with self.connection:
                self.connection.send('status\n')
                data = self.connection.receive()
                pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3},\w+,)')
                return len(pattern.findall(data))
        except Exception:
            return 0


class V2RayService:
    __log_file = '/var/log/v2ray/access.log'

    def __init__(self, executor: CommandExecutor):
        self.executor = executor

    def __find_v2ray_port(self) -> str:
        cmd = 'netstat -tlpn | grep v2ray'
        data = self.executor.execute(cmd).splitlines()[-1]
        return data.split()[3].split(':')[-1]

    def __find_addresses(self) -> list:
        addresses = []
        try:
            cmd = (
                'netstat -np 2>/dev/null | grep :%s | grep ESTABLISHED | awk \'{print $5}\' | sort | uniq'
                % self.__find_v2ray_port()
            )
            addresses.extend(self.executor.execute(cmd).splitlines())
        except Exception:
            pass

        return addresses

    def count(self, username: str) -> int:
        try:
            data = self.executor.execute('tail -n 1000 %s' % self.__log_file)
            for address in self.__find_addresses():
                pattern = r'%s.*email: %s' % (address, username)
                if re.search(pattern, data):
                    return 1
            return 0
        except Exception:
            return 0

    def all(self) -> int:
        try:
            data = self.executor.execute('tail -n 1000 %s' % self.__log_file)
            emails = []
            for address in self.__find_addresses():
                pattern = r'%s.*email: (\S+)' % address
                email = re.search(pattern, data)
                if email and email.group(1) not in emails:
                    emails.append(email.group(1))
            return len(emails)
        except Exception:
            return 0


class V2rayConnection(Connection):
    def __init__(self, service: V2RayService):
        self.service = service

    def count(self, username: str) -> int:
        return self.service.count(username)

    def all(self) -> int:
        return self.service.all()


class InMemoryConnection(ConnectionKill):
    def count(self, username: str) -> int:
        return len(username)

    def kill(self, username: str) -> None:
        pass

    def all(self) -> int:
        return 100
