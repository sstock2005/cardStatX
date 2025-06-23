"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

from datetime import datetime, timedelta
import os
import json

def parse_ts(ts_str):
    return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%fZ")

def get_card_list():
    if not os.path.isfile("data/map.json"):
        return None
    
    with open("data/map.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_card_json(card):
    if not os.path.isfile("data/" + card + ".json"):
        return None
    
    with open("data/" + card + ".json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_card_averages(card):
    if not os.path.isfile("data/" + card + ".json"):
        return None
    
    with open("data/" + card + ".json", "r", encoding="utf-8") as f:
        data = json.load(f)
       
    now = datetime.utcnow()
    cutoff_week  = now - timedelta(weeks=1)
    cutoff_month = now - timedelta(days=30)
    cutoff_year  = now - timedelta(days=365)
    
    sums = {'week': 0.0, 'month': 0.0, 'year': 0.0}
    counts = {'week': 0,   'month': 0,     'year': 0}

    for key, value in data.items():
        price = float(value[2])
        ts = parse_ts(value[3])

        if ts >= cutoff_week:
            sums['week']  += price
            counts['week'] += 1
        if ts >= cutoff_month:
            sums['month'] += price
            counts['month'] += 1
        if ts >= cutoff_year:
            sums['year']  += price
            counts['year'] += 1

    averages = {}
    for period in ('week','month','year'):
        if counts[period]:
            averages[period] = round(sums[period] / counts[period], 2)
        else:
            averages[period] = 0.0
    
    return averages