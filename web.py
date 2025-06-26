"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

from quart import Quart, jsonify
from util import get_card_list, get_card_averages
from ingestor import AsyncCardIngestor
from database import CardDatabase
import asyncio
import logging
from logging_setup import setup_logging

app = Quart('cardstatx')
setup_logging()
logger = logging.getLogger('web')

@app.route('/')
async def hello():
    return 'Hello, World!'

@app.route('/api/list')
async def api_list():
    cards = await get_card_list()
    if cards is None:
        return jsonify({"error": "No cards found"}), 404
    return jsonify(cards)

@app.route('/api/<card_id>/stats/average')
async def api_stats_average(card_id: str):
    averages = await get_card_averages(card_id)
    
    if averages is None:
        return jsonify({"error": "Card not found"}), 404
    
    return jsonify(averages)

if __name__ == '__main__':
    app.run(debug=True, port=5000)