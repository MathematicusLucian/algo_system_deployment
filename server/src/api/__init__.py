# -*- coding: utf-8 -*-
from server.src.api import create_app

def create_app_blueprint(config): #Flask app as RMIS instance
    return create_app(config, __name__, __path__)