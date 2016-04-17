# -*- coding: utf-8 -*-

import logging
import logging.config


DEFAULT_LOGGER = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(message)s',
        },
        'default': {
            'format': '%(asctime)s %(name)s (%(levelname)s) - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'filename': 'play-scraper.log',
            'formatter': 'default',
        },
    },
    'loggers': {
        __name__: {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}


def configure_logging(**kwargs):
    logging.config.dictConfig(DEFAULT_LOGGER)
    logger = logging.getLogger(__name__)
    return logger
