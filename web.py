"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

from logging_setup import setup_logging
from ingestor import iterate
from util import get_card_list, get_card_averages
import threading, signal
from flask import Flask
import json
import logging

app = Flask('web')
stop_event = threading.Event()

def iterate_task():
    iterate(stop_event)
    
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/list')
def api_list():
    return get_card_list()

@app.route('/api/<card>/stats/average')
def api_stats_average(card: str):
    averages = get_card_averages(card)
    
    if averages is None:
        return {"error": "Card not found"}, 404

    else:
        return averages
if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger('web')
    
    app.run(debug=True, use_reloader=False)