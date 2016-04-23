#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Object that provides crawl responses from wikipedia pages crawled to populate
information on flights available from airports for directflight.io
"""
import settings
import logger

class WikiInteract():
    """Provides all interaction methods for requests to Wikipedia
    """
    def pull_airport_list(self):
        log = logger.get()
        log.debug("Test output of log")
