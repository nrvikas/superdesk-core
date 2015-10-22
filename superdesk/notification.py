# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

"""Superdesk push notifications"""

import os
import logging
import asyncio
import websockets

from flask import json
from flask import current_app as app
from datetime import datetime


logging.basicConfig()
logger = logging.getLogger(__name__)


class ClosedSocket():
    """Mimic closed socket to simplify logic when connection
    can't be estabilished at first place.
    """
    def __init__(self):
        self.open = False

    def close(self):
        pass


def init_app(app):
    """Create websocket connection and put it on app object."""
    host = app.config['WS_HOST']
    port = app.config['WS_PORT']
    loop = asyncio.get_event_loop()
    try:
        app.ws_client = loop.run_until_complete(websockets.connect('ws://%s:%s/server' % (host, port)))
        logger.info('websocket connected on=%s:%s' % app.ws_client.local_address)
    except OSError as err:
        # not working now, but we can try later when actually sending something
        logger.exception(err)
        app.ws_client = ClosedSocket()


def _notify(**kwargs):
    """Send out all kwargs as json string."""
    kwargs.setdefault('_created', datetime.utcnow().isoformat())
    kwargs.setdefault('_process', os.getpid())
    message = json.dumps(kwargs)

    @asyncio.coroutine
    def send_message():
        yield from app.ws_client.send(message)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())


def push_notification(name, **kwargs):
    """Push notification to websocket.

    In case socket is closed it will try to reconnect.

    :param name: event name
    """
    logger.info('pushing event {0} ({1})'.format(name, json.dumps(kwargs)))

    if not app.ws_client.open:
        app.ws_client.close()
        init_app(app)

    if not app.ws_client.open:
        logger.error('No connection to websocket server. Dropping event %s' % name)
        return

    try:
        _notify(event=name, extra=kwargs)
    except Exception as err:
        logger.exception(err)
