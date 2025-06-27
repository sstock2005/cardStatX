"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

from syncdatabase import SyncCardDatabase
from logging_setup import setup_logging
from lxml import etree
import cloudscraper
import time
import hashlib
import logging
import bs4

setup_logging()

logger = logging.getLogger('scraper')

BASEURL = "https://www.tcdb.com"

def update_catalog():
    """Scrapes sets from tcdb by year"""
    
    logger.info("Starting catalog update - fetching years from TCDB")
    scraper = cloudscraper.create_scraper()
    html_doc = scraper.get("https://www.tcdb.com/ViewAll.cfm/sp/Football?MODE=Years").text
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    dom = etree.HTML(str(soup))
    
    years = {}
    table = dom.xpath('//*[@id="content"]/div[1]/div[1]/table[2]')[0]
    for element in table:
        for tr in element:
            for li in tr:
                for a in li:
                    if a is not None:
                        year = a.text
                        link = a.get("href")
                        years.update({year: link})
                        
    years = {key:value for key, value in sorted(years.items(), key=lambda item: int(item[0]))}
    
    logger.info(f"Found {len(years)} years to process: {', '.join(years.keys())}")
    
    for key, item in years.items():
        year_doc = scraper.get(BASEURL + item).text
        year_soup = bs4.BeautifulSoup(year_doc, 'html.parser')
        year_dom = etree.HTML(str(year_soup))
        
        year_releases = {}
        releases_blocks = year_dom.xpath('//*[@id="content"]/div[1]/div[2]')
        
        for release_block in releases_blocks:
            release_name = None
            for element in release_block:
                if element.tag == "h3":
                    release_name = element.text
                elif element.tag == 'ul' and release_name:
                    for ee in element:
                        if ee.tag == 'li':
                            for e in ee:
                                if e.tag == 'a':
                                    if e.text is None:
                                        continue
                                    
                                    set_name = e.text
                                    set_link = e.get("href")
                                    if release_name in year_releases:
                                        year_releases[release_name].update({set_name: set_link})
                                    else:
                                        year_releases[release_name] = {set_name: set_link}
        
        years[key] = year_releases
        time.sleep(1)  # some reason if we do not add a delay, some years are blank
        
    logger.info(f"Catalog update complete - processed {len(years)} years")
    return years

def update_sets(year_catalog: dict[str, dict[str, dict[str, str]]]):
    """Grabs cards from each set for each year"""
    
    logger.info("Starting card set update process")
    
    db = SyncCardDatabase()
    db.initialize()
    
    scraper = cloudscraper.create_scraper()
    total_years = len(year_catalog)
    year_count = 0
    total_cards_processed = 0
    
    for year, releases in year_catalog.items():
        year_count += 1
        logger.info(f"Processing year {year} ({year_count}/{total_years}) - {len(releases)} releases")
        
        year_cards = 0
        for _, sets in releases.items():
            
            for set_name, set_link in sets.items():
                
                set_id = set_link.split("sid/")[1].split("/")[0]
                printable_link = "/PrintChecklist.cfm?SetID=" + set_id
                doc = scraper.get(BASEURL + printable_link).text
                soup = bs4.BeautifulSoup(doc, 'html.parser')
                
                set_cards = 0
                for td in soup.find_all('td'):
                    for div in td.find_all('div', recursive=False):
                        card = set_name + " " + div.get_text(strip=True)
                        card_hash = hashlib.md5(card.encode()).hexdigest()
                        db.add_card(card_hash, card)
                        set_cards += 1
                
                year_cards += set_cards
                total_cards_processed += set_cards
        
        logger.info(f"Completed year {year} - processed {year_cards} cards")
    
    logger.info(f"Card processing complete - total {total_cards_processed} cards processed")
    logger.info("Card data saved to database")
    
    return total_cards_processed

if __name__ == "__main__":
    
    db = SyncCardDatabase()
    db.initialize()
    
    catalog = update_catalog()
    update_sets(catalog)