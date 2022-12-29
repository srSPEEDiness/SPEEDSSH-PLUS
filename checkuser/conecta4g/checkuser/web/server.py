import socket

from threading import Thread
from .utils import ThreadPool
from ..utils import logger


class Server:
    def __init__(self, host: str, port: int, num_workers: int = 10):
        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.pool = ThreadPool(num_workers)
        self.pool.start()

        self.is_running = False

    def handle(self, client, addr) -> None:
        self.pool.add_task(client, addr)

    def run(self) -> None:
        self.socket.bind((self.host, self.port))
        self.socket.listen(0)
        self.is_running = True

        logger.info(f'Server is running on {self.host}:{self.port}')

        try:
            while self.is_running:
                client, addr = self.socket.accept()
                self.handle(client, addr)

        except KeyboardInterrupt:
            pass

        finally:
            self.stop()

    def stop(self) -> None:
        self.is_running = False
        if self.socket:
            self.socket.close()


class ServerManager:
    def __init__(self, host: str, port: int, num_workers: int = 10, use_thread: bool = True):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.use_thread = use_thread

        self.server = Server(self.host, self.port, self.num_workers)
        self.thread = Thread(target=self.server.run)

    @property
    def is_running(self) -> bool:
        return self.server.is_running

    def start(self) -> None:
        if self.use_thread:
            self.thread.start()
            return

        self.server.run()
