import typing as t
import json
import socket
import queue
import threading

from checkuser.utils import logger

from ..checker import check_user, kill_user
from ..utils.config import Config


class ParserServerRequest:
    def __init__(self, data: bytes):
        self.data = data
        self.command = None
        self.content = None

        self.commands_allowed = ['CHECK' 'KILL']

    def parse(self) -> None:
        try:
            data = self.data.decode('utf-8')

            first_line = data.split('\n')[0]
            path = first_line.split(' ')[1]

            self.command = path.split('/')[1]
            self.content = path.split('/')[2].split('?')[0]

        except Exception:
            self.command = None
            self.content = None


class FunctionExecutor:
    def __init__(self, command: str, content: str):
        self.command = command
        self.content = content

    def execute(self) -> t.Dict[str, t.Any]:
        if self.command.upper() == 'CHECK':
            data = check_user(self.content)

            for exclude in Config().exclude:
                if exclude in data:
                    logger.debug(f'Exclude: {exclude}')
                    del data[exclude]

            return data

        if self.command.upper() == 'KILL':
            return kill_user(self.content)

        return {'error': 'Command not allowed'}


class WorkerThread(threading.Thread):
    def __init__(self, queue: queue.Queue):
        super(WorkerThread, self).__init__()
        self.queue = queue
        self.daemon = True
        self.name = 'WorkerThread ' + str(self.ident)

        self.is_running = False

    def parse_request(self, data: bytes) -> t.Dict[str, t.Any]:
        request = ParserServerRequest(data.strip())
        request.parse()

        function_executor = FunctionExecutor(request.command, request.content)
        return function_executor.execute()

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                client, addr = self.queue.get()

                data = client.recv(8192 * 8)
                if not data:
                    continue

                response_data = 'HTTP/1.1 200 OK\r\n Content-Type: application/json\r\n\r\n'
                response_data += json.dumps(self.parse_request(data), indent=4)

                client.send(response_data.encode('utf-8'))
                client.close()

            except Exception as e:
                pass

    def stop(self):
        self.is_running = False


class ThreadPool:
    def __init__(self, max_workers: int = 10):
        self.queue = queue.Queue()
        self.workers = []
        self.max_workers = max_workers

    def start(self):
        for _ in range(self.max_workers):
            worker = WorkerThread(self.queue)
            worker.start()
            self.workers.append(worker)

    def join(self):
        for worker in self.workers:
            worker.stop()
            worker.join()

    def add_task(self, task: socket.socket, *args):
        self.queue.put((task, args))
