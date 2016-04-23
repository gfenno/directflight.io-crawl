#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides a simple to import object that returns access configurations in the
settings.ini file
"""
import configparser
import os

def setup():
    settings = configparser.ConfigParser()
    settings.read(
        os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)
                )
            ,"settings.ini")
        )
    return settings
