"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

from database import CardDatabase
from typing import Optional, Dict

async def get_card_list() -> Optional[Dict[str, str]]:
    """Get list of all cards from database"""
    
    db = CardDatabase()
    return await db.get_all_cards()

async def get_card_averages(card_id: str) -> Optional[Dict[str, float]]:
    """Get price averages for a specific card"""
    
    db = CardDatabase()
    return await db.get_card_averages(card_id)