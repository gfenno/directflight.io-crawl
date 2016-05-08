#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Creates easy to import object for central logging setup as well as adding
additional objects to the logging stream
"""
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
def setup():
    """Returns initial object that can be called to create a logging stream
    """
    logger = logging.getLogger()
    stream_formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s'
            )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(stream_handler)

    return logger

def get():
    """Returns an object that allows additional objects to stream to the
    existing log
    """
    logger = logging.getLogger()

    return logger
