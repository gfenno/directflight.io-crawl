#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Top level object that implements features of other objects and implements scheduling from the settings.ini file
"""
import logger
import settings
from wiki import WikiInteract
settings = settings.setup()
# print settings['update_frequency']['update_airport_list']
log = logger.setup()

wiki = WikiInteract()
wiki.pull_airport_list()
