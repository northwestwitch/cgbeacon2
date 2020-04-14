# -*- coding: utf-8 -*-
from flask import Flask
import logging
import os
from pymongo import MongoClient

from .blueprints import api_v1

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def create_app():
    """Method that creates the Flask app"""

    app = None
    app = Flask(__name__)

    try:
        app.config.from_envvar('CGBEACON2_CONFIG')
        LOG.info("Starting app envirironmental variable CGBEACON2_CONFIG")
    except RuntimeError:
        LOG.warning('Environment variable settings not found, configuring from instance file.')
        app_root=os.path.abspath(__file__).split('cgbeacon2')[0]

         # check if config file exists under ../instance:
        instance_path = os.path.join(app_root,'cgbeacon2', 'instance')
        if not os.path.isfile(os.path.join(instance_path,'config.py')): # running app from tests
            instance_path = os.path.join(app_root,'cgbeacon2','cgbeacon2','instance')

        app = Flask(__name__, instance_path=instance_path, instance_relative_config=True)
        app.config.from_pyfile('config.py')

    if app.config.get("DB_URI") is None:
        LOG.warning("Please add database settings param in your config file.")
        quit()

    client = MongoClient(app.config['DB_URI'])
    app.db = client[app.config['DB_NAME']]
    LOG.info('database connection info:{}'.format(app.db))

    app.register_blueprint(api_v1.ap1_bp)

    return app
