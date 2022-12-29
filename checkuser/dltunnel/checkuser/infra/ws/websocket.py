import logging

from json import loads
from flask_sock import Sock, Server

from checkuser.infra.factories.make_controller import Controllers
from checkuser.infra.adapter import WebSocketAdapter

ws = Sock()
logger = logging.getLogger(__name__)


@ws.route('/')
def handle_message(server: Server):
    while True:
        body = server.receive()

        if body is None:
            break

        data = loads(body)
        logger.info('-' * 50)
        logger.info('[WEBSOCKET SERVER]')
        logger.info('[IP] -> %s', server.sock.getpeername()[0])
        logger.info('[ACTION] -> %s', data['action'])
        logger.info('-' * 50)

        response = WebSocketAdapter.adapt(Controllers.get(data['action']), data['data'])
        server.send(response)
