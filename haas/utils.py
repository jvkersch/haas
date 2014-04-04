# -*- coding: utf-8 -*-
# Copyright (c) 2013-2014 Simon Jagoe
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the 3-clause BSD license.  See the LICENSE.txt file for details.
from __future__ import absolute_import, unicode_literals

import haas
import logging
import sys
import re


LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'fatal': logging.FATAL,
    'critical': logging.CRITICAL,
}


def configure_logging(level):
    actual_level = LEVELS.get(level, logging.WARNING)
    format_ = '%(asctime)s %(levelname)-8.8s [%(name)s:%(lineno)s] %(message)s'
    formatter = logging.Formatter(format_)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(actual_level)
    logger = logging.getLogger(haas.__name__)
    logger.addHandler(handler)
    logger.setLevel(actual_level)
    logger.info('Logging configured for haas at level %r',
                logging.getLevelName(actual_level))


def get_module_by_name(name):
    """Import a module and return the imported module object.

    """
    __import__(name)
    return sys.modules[name]


UNCAMELCASE_FIRST_PASS = re.compile(
    r'(?P<before>.)(?P<caps>[A-Z]+)')
UNCAMELCASE_SECOND_PASS = re.compile(
    r'(?P<before>.)(?<=[A-Z])(?P<caps>[A-Z][a-z]+)')


def uncamelcase(string, sep='_'):
    replace = '\g<before>{}\g<caps>'.format(sep)
    temp = UNCAMELCASE_FIRST_PASS.sub(replace, string)
    return UNCAMELCASE_SECOND_PASS.sub(replace, temp).lower()
