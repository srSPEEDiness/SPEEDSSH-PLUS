import json
import logging

from typing import Callable
from flask import request, Response


from checkuser.infra.controller import Controller, HttpRequest

logger = logging.getLogger(__name__)


class FlaskAdpater:
    @staticmethod
    def adapt(controller: Controller) -> Callable[..., Response]:
        def wrapper(*args, **kwargs):
            try:
                response = controller.handle(
                    HttpRequest(
                        query={
                            **request.args,
                            **(request.view_args or {}),
                        },
                        body={
                            **request.form,
                            **(request.get_json(silent=True) or {}),
                        },
                    )
                )
                return Response(
                    response=json.dumps(response.body, indent=4),
                    status=response.status_code,
                    mimetype='application/json',
                )
            except Exception as e:
                logger.exception(e)
                return Response(
                    response=json.dumps({'error': str(e)}),
                    status=500,
                    mimetype='application/json',
                )

        return wrapper


class WebSocketAdapter:
    @staticmethod
    def adapt(controller: Controller, data: dict) -> str:
        try:
            response = controller.handle(
                HttpRequest(
                    query=data,
                    body=data,
                )
            )
            return json.dumps(response.body, indent=4)
        except Exception as e:
            return json.dumps({'error': str(e)})
