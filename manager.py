#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Top level object that implements features of other objects and implements
scheduling from the settings.ini file
"""
import logger
import settings
from wiki import WikiInteract
from flight_db import FlightDB
settings = settings.setup()
log = logger.setup()

def update_airport_list():
    """Pulls a complete list of all airports and updates it in the database

   Returns
    -------
    list of lists
        outer list
            airport complete information
        inner list
            item 0 : string
                IATA code for airport
            item 1 : string
                ICAO code for airport
            item 2 : string
                airport wiki link
            item 3 : string
                airport name
            item 4 : airport location name
    """
    wiki = WikiInteract()
    airports = wiki.pull_airport_list()

    with FlightDB() as db:
        db.insert_airports(airports)

if __name__ == '__main__':
    update_airport_list()
