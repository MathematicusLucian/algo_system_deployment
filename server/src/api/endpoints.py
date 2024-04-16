# -*- coding: utf-8 -*-
import sys, os
from markupsafe import escape
import json
import random
from bidict import bidict
from functools import wraps
import time
from datetime import datetime
import pytz
import threading
import traceback
from flask import abort, app, Blueprint, jsonify, redirect, render_template, request, url_for
# from flask_cache import Cache
# from flask_login import current_user
from pandas import Timestamp
import wandb
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# from matplotlib.offsetbox import AnnotationBbox, OffsetImage
# import seaborn as sns
# import logging
from okx.exceptions import OkxAPIException, OkxParamsException, OkxRequestException
from okx.MarketData import MarketAPI
from okx.PublicData import PublicAPI
# from src.services.market_data_service.WssMarketDataService import ChecksumThread, WssMarketDataService
from src.services.metals_data_service.gold_prices import fetch_gold_price
from src.strategy.macd import determine_macd_crypto
# from src.services.sentiment_service import XSentimentService
# from src.services.x_service import XArchive, x_unofficial
# from src.services.crypto_analysis import *
# from src.strategy.SampleMM import SampleMM
# from src.utils import *
# from src.utils import chart_colors
from src.utils.common import get_config
from src.services.coindata import CoinDataService

api_key = get_config('LIVECOINWATCH_API_KEY')
base_currency = get_config('BASE_CURRENCY')
coins = get_config('COINS')
coin_data = CoinDataService(api_key, base_currency)
algo_rest_blueprint = Blueprint('crypto_rest', __name__)

def create_okx_api(api, is_paper_trading):
    flag='0' if not is_paper_trading else '1'
    if api=="MarketAPI":
        return MarketAPI(flag, debug=False)
    elif api=="PublicAPI":
        return PublicAPI(flag, debug=False)

# @algo_rest_blueprint.errorhandler(404)
# def not_found():
#     return redirect(url_for('not_found'))

# @algo_rest_blueprint('/not-found')
# def page_not_found(error):
#     abort(404)

# --------------------
# ------- ROOT -------
# --------------------    
def get_root():
    return "Hello World"

# http://127.0.0.1:5000/
@algo_rest_blueprint.route("/")
# @cache.cached(timeout=60)
def index():
    version = "v1.0.0"
    return jsonify({"CryptoTracker API" : format(escape(version))})

@algo_rest_blueprint.route("/api")
def helloworld():
    return jsonify({"status": 200, "msg":"CryptoTracker Flask API"})

@algo_rest_blueprint.route("/api/ping")
def ping():
    return jsonify({"status": 200, "msg":"I am the CryptoTracker Flask API"})

@algo_rest_blueprint.route("api//2000")
def fetch_2000():
    with open('api_sample_data/user.json') as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)
    return jsonify(parsed_json)

@algo_rest_blueprint.route("/api/audusd15m")
def fetch_audusd15m():
    with open('api_sample_data/audusd15m.json') as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)
    return jsonify(parsed_json)

@algo_rest_blueprint.route("/api/audusd15m_")
def fetch_audusd15m_():
    with open('api_sample_data/audusd15m_.json') as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)
    return jsonify(parsed_json)

# /api/currencies?selected=GBP
@algo_rest_blueprint.route("/api/currencies")
def currencies():
    selected_currency = request.args.get('selected') if request.args.get('selected') else None
    currencies = coin_data.get_currencies(selected_currency)
    return jsonify({"res": currencies})

# /api/currencies?base=GBP&second_currency=BTC
@algo_rest_blueprint.route("/api/coin_history")
def historic_values__coin():
    base = request.args.get('base')
    second_currency = request.args.get('second_currency')
    period = request.args.get('period')
    return coin_data.get_historic_values__coin(second_currency, base, period)

@algo_rest_blueprint.route("/api/coins_history")
def historic_values__coins():
    return coin_data.get_historic_values__coins(coins)

@algo_rest_blueprint.route("/api/latest_values")
def latest_values():
    return coin_data.get_latest_values(coins)