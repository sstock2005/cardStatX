# cardStatX

A comprehensive football card data ingestion and analysis system that scrapes card information from TCDB and monitors eBay pricing data.

## Overview

cardStatX is a multi-component system designed to:
- Scrape football card catalog data from The Trading Card Database (TCDB)
- Monitor eBay listings for pricing information
- Provide a web API for accessing card statistics and averages
- Maintain a continuously updated database of card values

## Showcase

Database Showcase #1
![image](https://github.com/user-attachments/assets/df5b9eae-6c51-479a-9dbc-f82327a53726)

Database Showcase #2
![image](https://github.com/user-attachments/assets/9545589f-75e5-467f-bf7f-978f478885a2)

Website API Showcase #1
![image](https://github.com/user-attachments/assets/a14bc522-21f6-4951-b914-8a431bb46194)

Website API Showcase #2
![image](https://github.com/user-attachments/assets/c1cd5a4d-3fdf-41d0-9dd8-cf58749e484f)

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Rename `constants.py.example` to `constants.py` and edit like so:
```python
OAUTH_TOKEN = "your_ebay_oauth_token_here"
```
[But how do I get an OAUTH token??](https://developer.ebay.com/api-docs/static/oauth-tokens.html)


3. Run `scraper.py` and wait. It will take up to 20 minutes.

4. Run `ingestor.py` and wait. It could take several hours depending on how much data you want from eBay.

5. Run `web.py` and go wild.
```
/api/list - returns a list of every card's id along with it's name
/api/<card>/stats/average - returns average price in USD of card based on eBay data. comes in week, month, and year.
```

## TODO
I don't know if these will ever happen, pr open!
- Add more filtering to eBay search results
- Combine scripts into modules
- Website Frontend

## Contributing

When contributing to this project, please:
1. Maintain the existing code style and logging patterns
2. Add appropriate error handling and logging
3. Update documentation for any new features
4. Test thoroughly with rate limiting in mind

## Disclaimer

This tool is for educational and personal use only. Please respect:
- eBay's Terms of Service and rate limits
- TCDB's robots.txt and usage policies
- All applicable laws and regulations regarding data scraping

The author is not responsible for any misuse of this software or violations of third-party terms of service.
