#!/usr/bin/python

# Utility functions for the Doneit project

import logging

logger = logging.getLogger('doneit')
hdlr = logging.FileHandler('/var/log/doneit.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

# Log a message
def log(msg):
    logger.info(msg)
