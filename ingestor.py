"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

from logging_setup import setup_logging
from typing import Any
import threading
import hashlib
import logging
import requests
import constants
import json
import time
import os

setup_logging()

logger = logging.getLogger('ingestor')
    
def search(keyword: str) -> Any | None:
    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={keyword}&category_ids=261328&limit=200"

    payload = {}
    headers = {
    'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US',
    'Authorization': f'Bearer {constants.OAUTH_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    with open("response.json", "w") as f:
        f.write(response.content.decode())
        
    
    if response.ok:
        if int(response.json()['total']) == 0:
            logger.warning(f"[search::warning] {keyword} returned 0 results")
            
        return response.json()
    else:
        logger.error(f"[search::error] {keyword} search failed")
        return None
    
def filter(data):
    
    items = {}
    
    if not data:
        return None
    
    if int(data['total']) == 0:
        return None
    
    found_items = data['itemSummaries']
        
    for item in found_items:
        id = item['itemId']
        title = item['title']
        
        # filter out non-standard items
        if "|0" not in id:
            logger.warning(f"[filter::warning] skipping non standard item {id}")
            continue
        
        if item['price']['currency'] != 'USD':
            logger.warning(f"[filter::warning] skipped non USD item {id}")
            continue
        
        try:
            condition = item['condition'] + ':' + item['conditionId']
        except KeyError as ke:
            continue  # skip items without condition information
            
        # TODO add more filtering here
        # item['Set']
        # item['Card Number']
        
        cost = item['price']['value']

        itemCreationDate = item['itemCreationDate']
        
        items.update({id: (title, condition, cost, itemCreationDate)})
        
    return items

def initialize():
    if not os.path.isdir('data'):
        os.mkdir('data')

def iterate(stop_event: threading.Event):
    initialize()
    
    while True:
        
        if stop_event.is_set():
            break
        
        with open("data/map.json", 'r') as f:
            cards: dict = json.load(f)
            
        for card in cards.values():
            current = filter(search(card))
            
            name = card
            card = hashlib.md5(card.encode()).hexdigest()
            
            if not current:
                continue
            
            if not os.path.isfile('data/' + card + '.json'):
                with open('data/' + card + '.json', 'w', encoding='utf-8') as f:
                    json.dump(current, f, ensure_ascii=False, indent=4)
            else:
                with open('data/' + card + '.json', 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                
                cached.update(current)
                
                with open('data/' + card + '.json', 'w', encoding='utf-8') as f:
                    json.dump(cached, f, ensure_ascii=False, indent=4)
                
            if not os.path.isfile('data/map.json'):
                with open('data/map.json', 'w', encoding='utf-8') as f:
                    json.dump({card: name}, f, ensure_ascii=False, indent=4)
            else:
                with open('data/map.json', 'r', encoding='utf-8') as f:
                    map = json.load(f)
                    
                map.update({card: name})
                
                with open('data/map.json', 'w', encoding='utf-8') as f:
                    json.dump(map, f, ensure_ascii=False, indent=4)
                    
            logger.info(f"[iterate::success] processed {name} ({card})")
            
            time.sleep(1)
            
        logger.info(f"[iterate::success] saved results to data/{card}.json")
        
        time.sleep(10)
        
if __name__ == "__main__":
    logger.info("Starting ingestor")
    
    stop_event = threading.Event()
    
    try:
        iterate(stop_event)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping ingestor")
        stop_event.set()
        
    logger.info("Ingestor stopped")