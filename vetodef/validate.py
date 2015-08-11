# -*- coding: utf-8 -*-

"""Utilities to validate a veto_def entry
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"
__version__ = "0.1"

import os

from urlparse import urlparse
from urllib2 import URLError

from dqsegdb import apicalls

SEGMENT_DATABASE = os.getenv('O1_SEGMENT_SERVER', None)


# -- veto_def validation ------------------------------------------------------

MAXIMUM_PADDING = 1200
MAXIMUM_CATEGORY = 4


def check_veto_def_times(veto):
    """Assert veto start_time and end_time are sane
    """
    start = veto.start_time
    end = veto.end_time
    assert end == 0 or end > start, "end_time before start_time"
    assert start >= 0, "start_time negative"
    assert end >= 0, "end_time negative"
    assert start < 1e10, "start_time too big"
    assert end < 1e01, "end_time too big"


def check_veto_def_padding(veto):
    """Assert veto start_pad and end_pad are sane
    """
    start = veto.start_pad
    end = veto.end_pad
    assert start > -MAXIMUM_PADDING, "start_pad too big (negative)"
    assert start < MAXIMUM_PADDING, "start_pad too big (positive)"
    assert end > -MAXIMUM_PADDING, "end_pad too big (negative)"
    assert end < MAXIMUM_PADDING, "end_pad too big (positive)"


def check_veto_def_exists(veto, url=None):
    """Assert veto flag exist in database for times given
    """
    url = urlparse(url or SEGMENT_DATABASE)
    try:
        metadata = apicalls.dqsegdbQueryTimes(
            url.scheme, url.netloc, veto.ifo, veto.name, veto.version,
            "metadata", veto.start_time, veto.end_time or 1e10)
    except URLError as e:
        raise AssertionError("Flag not found in database")


def check_veto_def_category(veto):
    """Assert veto category is sane
    """
    category = veto.category
    assert category > 0, "category less than 1"
    assert category <= MAXIMUM_CATEGORY, \
           "category greater than %d" % MAXIMUM_CATEGORY

VETO_TESTS = [val for (key, val) in locals().items() if
              key.startswith('check_veto_def')]


# -- veto_def_table validation ------------------------------------------------

def check_veto_table_versions(table):
    """Assert no two version of the same flag in the table
    """
    versions = dict()
    for veto in table:
        flag = (veto.ifo, veto.name, veto.version)
        # record information for cross tests
        try:
            versions[flag].append(veto.version)
        except KeyError:
            versions[flag] = [veto.version]

    for flag in sorted(versions.keys()):
        assert len(versions[flag]) == 1, "multiple versions of flag"


TABLE_TESTS = [val for (key, val) in locals().items() if
               key.startswith('check_veto_table')]
