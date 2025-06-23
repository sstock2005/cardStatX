# cardStatX

A comprehensive football card data ingestion and analysis system that scrapes card information from TCDB and monitors eBay pricing data.

## Overview

cardStatX is a multi-component system designed to:
- Scrape football card catalog data from The Trading Card Database (TCDB)
- Monitor eBay listings for pricing information
- Provide a web API for accessing card statistics and averages
- Maintain a continuously updated database of card values

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Rename `constants.py.example` to `constants.py` and edit like so:
```python
OAUTH_TOKEN = "your_ebay_oauth_token_here"
```

3. Ensure data directory exists:
```bash
mkdir -p data logs
```

## TODO

- Add more filtering to eBay search results
- Combine scripts into modules
- Website Frontend

## License

This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- **NonCommercial** — You may not use the material for commercial purposes

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