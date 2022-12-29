import logging
import os

from . import args
from .infra.http.flask import app
from .infra.ws.websocket import ws
from .infra.ws.socketio import io

try:
    from eventlet import monkey_patch

    monkey_patch()
except ImportError:
    pass

args.add_argument('--host', type=str, help='Host to listen', default='0.0.0.0')
args.add_argument('--port', '-p', type=int, help='Port', default=5000)
args.add_argument('--start', action='store_true', help='Start the daemon')
args.add_argument('--log', '-l', type=str, help='LogLevel', default='INFO')
args.add_argument('--log-file', type=str, help='Log file', default='/var/log/checkuser.log')


def main(debug: bool = os.getenv('APP_DEBUG') == '1') -> None:
    data = args.parse_args()

    try:
        logging.basicConfig(
            level=getattr(logging, data.log.upper()),
            format='%(asctime)s - %(message)s',
            filename=data.log_file,
        )
    except PermissionError:
        logging.basicConfig(
            level=getattr(logging, data.log.upper()),
            format='%(asctime)s - %(message)s',
        )

    if data.start:
        io.init_app(app)
        ws.init_app(app)
        io.run(app, host=data.host, port=data.port, debug=debug)
        return

    args.print_help()


if __name__ == '__main__':
    main()
