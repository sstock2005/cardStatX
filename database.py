"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

import aiosqlite
import asyncio
import logging
from typing import Optional, Dict, List, Tuple
from datetime import datetime
import os

logger = logging.getLogger('database')

class CardDatabase:
    def __init__(self, db_path: str = "data/cards.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
    async def initialize(self):
        """Initialize the database with required tables"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS cards (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.execute("""
                CREATE TABLE IF NOT EXISTS listings (
                    id TEXT PRIMARY KEY,
                    card_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    condition_text TEXT,
                    price REAL NOT NULL,
                    currency TEXT DEFAULT 'USD',
                    listing_date TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (card_id) REFERENCES cards (id)
                )
            """)
            
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_card_id ON listings(card_id)
            """)
            
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_listing_date ON listings(listing_date)
            """)
            
            await db.commit()
    
    async def add_card(self, card_id: str, card_name: str) -> bool:
        """Add a new card or update existing one"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO cards (id, name, updated_at) 
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (card_id, card_name))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding card {card_id}: {e}")
            return False
    
    async def add_listing(self, listing_id: str, card_id: str, title: str, 
                         condition: str, price: float, listing_date: str) -> bool:
        """Add a new listing"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO listings 
                    (id, card_id, title, condition_text, price, listing_date) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (listing_id, card_id, title, condition, price, listing_date))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding listing {listing_id}: {e}")
            return False
    
    async def get_all_cards(self) -> Dict[str, str]:
        """Get all cards as a dictionary {id: name}"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT id, name FROM cards") as cursor:
                rows = await cursor.fetchall()
                return {row[0]: row[1] for row in rows}
    
    async def get_card_averages(self, card_id: str) -> Optional[Dict[str, float]]:
        """Calculate price averages for a card over different time periods"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Get listings from different time periods
                query = """
                    SELECT price, listing_date 
                    FROM listings 
                    WHERE card_id = ? AND currency = 'USD'
                    ORDER BY listing_date DESC
                """
                
                async with db.execute(query, (card_id,)) as cursor:
                    rows = await cursor.fetchall()
                
                if not rows:
                    return None
                
                now = datetime.utcnow()
                from datetime import timedelta
                
                cutoff_week = now - timedelta(weeks=1)
                cutoff_month = now - timedelta(days=30)
                cutoff_year = now - timedelta(days=365)
                
                sums = {'week': 0.0, 'month': 0.0, 'year': 0.0}
                counts = {'week': 0, 'month': 0, 'year': 0}
                
                for price, listing_date_str in rows:
                    listing_date = datetime.strptime(listing_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    
                    if listing_date >= cutoff_week:
                        sums['week'] += price
                        counts['week'] += 1
                    if listing_date >= cutoff_month:
                        sums['month'] += price
                        counts['month'] += 1
                    if listing_date >= cutoff_year:
                        sums['year'] += price
                        counts['year'] += 1
                
                averages = {}
                for period in ('week', 'month', 'year'):
                    if counts[period] > 0:
                        averages[period] = round(sums[period] / counts[period], 2)
                    else:
                        averages[period] = 0.0
                
                return averages
                
        except Exception as e:
            logger.error(f"Error calculating averages for card {card_id}: {e}")
            return None