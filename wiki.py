#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Object that provides crawl responses from wikipedia pages crawled to populate
information on flights available from airports for directflight.io
"""
import settings
import logger
from requests import get
import urlparse
import string
from bs4 import BeautifulSoup,UnicodeDammit
from re import search

settings = settings.setup()
log = logger.get()

wiki_base = "https://en.wikipedia.org/"

class WikiInteract():
    """Provides all interaction methods for requests to Wikipedia

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
                item 4 : string
                    airport location name
    """

    def pull_airport_list(self):
        """Makes request to Wikipedia for airport list and returns it in a
        structured data format
        """
        airport_base = urlparse.urljoin(
                wiki_base,
                "wiki/List_of_airports_by_IATA_code:_")

        airport_pages = [airport_base + letter \
            for letter in list(string.ascii_uppercase)]

        # Eventually need to iterate through all elements here 
        r = get(airport_pages[0])
        soup = BeautifulSoup(
                r.text.encode('utf-8',
                errors='ignore'),
                "html.parser")

        table = soup.find("table")

        data_result = [row.find_all('td') for row in \
            table.find_all('tr')]

        data_result = filter(None,data_result)

        def clean_text(text):
            """When passed a cell from Wikipedia determine if the cell has a
            link and pass back a tuple if so, if not pass back text

            Returns
            -------
            tuple : string
                tuple of items to be added to airport information
            """

        def parse_sections(row):
            """Cleans text and returnes both the link and the text if the link
            is present or just the text cleaned if no link is present

            Parameters
            ----------
            row : list
                combination of text and text with href links in it

            Returns
            -------
            cleaned : list
                cleaned text with links seperated into seperate entries
            """
            cleaned = []
            for item in row:
                a_ref = item.find('a')
                if a_ref is not None:
                    cleaned.append(a_ref['href'])
                    cleaned.append(a_ref.get_text().encode('utf-8'))
                else:
                    cleaned.append(item.get_text().encode('utf-8'))
            return cleaned

        data_result = map(parse_sections,data_result)

        def filter_result(row):
            """Cleans results and verifies that data matches expected output,
            items that do not meet requirments are logged

            Parameters
            ----------
            row : list
                combination of links and text cleaned of html

            Returns
            -------
            cleaned : list
                list that has items removed that do not meet requirments

            --Requirments--:
                ICAO meets [A-Z]{3} regex
                IATA meets [A-Z]{4} regex
                Airport has a valid Wikipedia Page Link
            """
            if len(row) >= 8:
                if not search('[A-Z]{3}',row[0]):
                    log.debug('ICAO requirment not passed for: ' + \
                        '%s contained in %s',
                        row[0],row)
                    return False
                if not search('[A-Z]{4}',row[1]):
                    log.debug('IATA requirment not passed for: ' + \
                        '%s contained in %s',
                        row[1],row)
                    return False
                if search('redlink',row[2]):
                    log.debug( "Bad Link: %s",str(row[2]))
                    return False
            return True

        data_result = filter(filter_result,data_result)
        return data_result
