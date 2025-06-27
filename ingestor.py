"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

from logging_setup import setup_logging
from database import CardDatabase
from typing import Optional
import constants
import asyncio
import aiohttp
import logging

logger = logging.getLogger('async_ingestor')

class AsyncCardIngestor:
    def __init__(self, db: CardDatabase):
        self.db = db
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_ebay(self, keyword: str) -> Optional[dict]:
        """Search eBay API asynchronously"""
        
        url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={keyword}&category_ids=261328&limit=200"
        
        headers = {
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US',
            'Authorization': f'Bearer {constants.OAUTH_TOKEN}'
        }
        
        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if int(data.get('total', 0)) == 0:
                        logger.warning(f"Search for '{keyword}' returned 0 results")
                        
                    return data
                else:
                    logger.error(f"eBay search failed for '{keyword}': {response.status}")
                    return None
                
        except Exception as e:
            logger.error(f"Error searching eBay for '{keyword}': {e}")
            return None
    
    def filter_items(self, data: dict) -> Optional[dict]:
        """Filter eBay search results"""
        
        if not data or int(data.get('total', 0)) == 0:
            return None
        
        items = {}
        found_items = data.get('itemSummaries', [])
        
        for item in found_items:
            item_id = item['itemId']
            title = item['title']
            
            if "|0" not in item_id:
                continue
            
            if item['price']['currency'] != 'USD':
                continue
            
            try:
                condition = item['condition'] + ':' + item['conditionId']
                
            except KeyError:
                continue
            
            price = float(item['price']['value'])
            creation_date = item['itemCreationDate']
            
            items[item_id] = (title, condition, price, creation_date)
        
        return items if items else None
    
    async def process_card(self, card_id: str, card_name: str) -> int:
        """Process a single card - search eBay and store results"""
        
        try:
            search_data = await self.search_ebay(card_name)
            filtered_items = self.filter_items(search_data)
            
            if not filtered_items:
                return 0
            
            listings_added = 0
            for listing_id, (title, condition, price, listing_date) in filtered_items.items():
                success = await self.db.add_listing(
                    listing_id, card_id, title, condition, price, listing_date
                )
                if success:
                    listings_added += 1
            
            logger.info(f"Processed {card_name} ({card_id}) - added {listings_added} listings")
            return listings_added
            
        except Exception as e:
            logger.error(f"Error processing card {card_name}: {e}")
            return 0
    
    async def process_all_cards(self, concurrency_limit: int = 5):
        """Process all cards with controlled concurrency"""
        
        cards = await self.db.get_all_cards()
        
        if not cards:
            logger.warning("No cards found in database")
            return
        
        logger.info(f"Starting to process {len(cards)} cards with concurrency limit {concurrency_limit}")
        
        semaphore = asyncio.Semaphore(concurrency_limit)
        
        async def process_with_semaphore(card_id: str, card_name: str):
            async with semaphore:
                result = await self.process_card(card_id, card_name)
                await asyncio.sleep(1)
                return result
        
        tasks = [
            process_with_semaphore(card_id, card_name) 
            for card_id, card_name in cards.items()
        ]
        
        total_listings = 0
        completed = 0
        
        for task in asyncio.as_completed(tasks):
            listings_count = await task
            total_listings += listings_count
            completed += 1
            
            if completed % 10 == 0:
                logger.info(f"Progress: {completed}/{len(cards)} cards processed")
        
        logger.info(f"Completed processing all cards - total {total_listings} listings added")

async def main():
    
    setup_logging()

    db = CardDatabase()
    
    await db.initialize()
    
    async with AsyncCardIngestor(db) as ingestor:
        await ingestor.process_all_cards(concurrency_limit=3)

if __name__ == "__main__":
    asyncio.run(main())