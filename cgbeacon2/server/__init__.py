# -*- coding: utf-8 -*-
import logging


logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def create_app():
    """Method that creates the Flask app"""

    app = None
    LOG.info('Configuring app from environment variable')
    app = Flask(__name__)
    app.config.from_envvar('CGBEACON2_CONFIG')

    return app
