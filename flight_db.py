#!/usr/bin/env python                                                            
# -*- coding: utf-8 -*-
"""Connects and provides the interfaces with the MySQL data store keeping all
flight information
"""
import MySQLdb
from _mysql_exceptions import IntegrityError
import logger
from os import getenv
import codecs

log = logger.get()

class FlightDB(object):


    def insert_airports(self,airports):
        """Given list of lists containing all airports found insert them into
        flight database

        Parameters
        ---------
        airports : list of lists
            inner list contents:
                0 : IATA code
                1 : ICAO code
                2 : wiki link for airport
                3 : airport name
                4 : airport city wiki link
                5 : airport city name
                6 : airport timezone wiki link
                7 : airport timezone offset from UTC
            example:
                ['AZZ', 'FNAM', u'/wiki/Ambriz_Airport', 'Ambriz Airport',
                u'/wiki/Ambriz', 'Ambriz', u'/wiki/West_Africa_Time',
                'UTC+01:00', '']
        Returns
        -------
        """
        def show_first_iata(airports):
            """Only used for logging.  Function prevents index error by checking
            to make sure that the structure will allow an internal print of
            airports[0][0]
            """
            if len(airports) > 0:
                if len(airports[0]) > 0:
                    return airports[0][0]
            else:
                return None

        count_successful = 0
        count_duplicates = 0
        for a in airports:
            try:
                self.cursor.execute("""
                INSERT INTO
                    airports(`iata`,
                            `icao`,
                            `airport_wiki_url`,
                            `airport_name`,
                            `airport_place_wiki_url`,
                            `airport_place_name`)
                VALUES
                    (%s,%s,%s,%s,%s,%s)""",
                    (a[0],a[1],a[2],a[3],a[4],
                    a[5]))
                self.conn.commit()
                count_successful += 1
            except IntegrityError:
                count_duplicates += 1
        log.info("Airport Inserts: Successful - %s Duplicate - %s " + 
                "First IATA - %s",
                count_successful,count_duplicates,
                show_first_iata(airports))

    def __enter__(self):
        self.conn = MySQLdb.connect(host=getenv('FLIGHT_HOST'),
                                    user=getenv('FLIGHT_USER'),
                                    passwd=getenv('FLIGHT_PW'),
                                    db='flight-data',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        log.debug('Connected to Flight DB')
        return self

    def __exit__(self, eType, eValue, eTrace):
        self.cursor.close()
        self.conn.close()
        log.debug('Disconnected from Flight DB')
