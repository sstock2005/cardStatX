"""
cardStatX - Football Card Data Ingestion System
Author: Samuel Stockstrom
License: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
"""

import logging
import logging.config
import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    'handlers': {
        # Handler for ingestor
        'ingestor': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'logs/ingestor.log',
            'backupCount': 3,
            'encoding': 'utf-8',
        },
        # Handler for web
        'web': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'logs/web.log',
            'backupCount': 3,
            'encoding': 'utf-8',
        },
        # Handler for scraper
        'scraper': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'logs/scraper.log',
            'backupCount': 3,
            'encoding': 'utf-8',
        }
        # ...
    },

    'loggers': {
        # Logger for ingestor
        'ingestor': {
            'handlers': ['ingestor'],
            'level': 'DEBUG',
            'propagate': False,   # avoid also sending to root
        },
        # Logger for web
        'web': {
            'handlers': ['web'],
            'level': 'DEBUG',
            'propagate': False,   # avoid also sending to root
        },
        # Logger for scraper
        'scraper': {
            'handlers': ['scraper'],
            'level': 'DEBUG',
            'propagate': False,   # avoid also sending to root
        }
    }
}

def setup_logging():
    
    if not os.path.isdir("logs"):
        os.mkdir("logs")
        
    logging.config.dictConfig(LOGGING_CONFIG)