import logging

from flask import request
from flask_socketio import SocketIO, emit
from checkuser.infra.factories.make_controller import Controllers
from checkuser.infra.adapter import WebSocketAdapter

io = SocketIO(cors_allowed_origins='*')
logger = logging.getLogger(__name__)


def _get_session_id() -> str:
    return request.sid  # type: ignore


@io.on('message')
def on_message(data: dict) -> None:
    logger.info('-' * 50)
    logger.info('[SOCKETIO SERVER]')
    logger.info('[IP] -> %s', request.remote_addr)
    logger.info('[SID] -> %s', _get_session_id())
    logger.info('[ACTION] -> %s', data['action'])
    logger.info('-' * 50)

    response = WebSocketAdapter.adapt(Controllers.get(data['action']), data['data'])
    emit('message', response)
