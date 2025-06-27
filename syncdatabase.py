"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

from typing import Dict
import sqlite3
import logging
import os

logger = logging.getLogger('sync_database')

class SyncCardDatabase:
    def __init__(self, db_path: str = "data/cards.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    def initialize(self):
        """Initialize the database with required tables"""
        
        with sqlite3.connect(self.db_path) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS cards (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            db.execute("""
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
            
            db.execute("""
                CREATE INDEX IF NOT EXISTS idx_card_id ON listings(card_id)
            """)
            
            db.execute("""
                CREATE INDEX IF NOT EXISTS idx_listing_date ON listings(listing_date)
            """)
            
            db.commit()
    
    def add_card(self, card_id: str, card_name: str) -> bool:
        """Add a new card or update existing one"""
        
        try:
            with sqlite3.connect(self.db_path) as db:
                db.execute("""
                    INSERT OR REPLACE INTO cards (id, name, updated_at) 
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                """, (card_id, card_name))
                db.commit()
                
                return True
            
        except Exception as e:
            logger.error(f"Error adding card {card_id}: {e}")
            return False
    
    def get_all_cards(self) -> Dict[str, str]:
        """Get all cards as a dictionary {id: name}"""
        
        with sqlite3.connect(self.db_path) as db:
            cursor = db.execute("SELECT id, name FROM cards")
            rows = cursor.fetchall()
            
            return {row[0]: row[1] for row in rows}