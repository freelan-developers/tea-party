"""
A tea-party cache class.
"""

import os
import errno

from tea_party.log import LOGGER
from tea_party.path import from_user_path
from tea_party.defaults import *


def make_cache(data, base_path):
    """
    Make a Cache instance from a string or dictionary.

    If `data` is a string, the Cache is default created at the location
    specified by `data.

    If `data` is a dictionary, it contains the attributes for the Cache
    instance to create.

    If `data` is falsy, the Cache is default created.
    """

    if not data:
        cache_path = from_user_path(DEFAULT_CACHE_PATH)
    elif isinstance(data, basestring):
        cache_path = from_user_path(data)
    else:
        cache_path = from_user_path(data.get('location', DEFAULT_CACHE_PATH))

    if not os.path.isabs(cache_path):
        cache_path = os.path.normpath(os.path.join(base_path, cache_path))

    return Cache(path=cache_path)

class Cache(object):

    """
    A Cache instance holds information about the fetched archives.
    """

    def __init__(self, path):
        """
        Create a Cache instance.

        `path` is the cache root directory.
        """

        self.path = os.path.abspath(path)

        try:
            os.makedirs(self.path)

            LOGGER.info('Creating cache directory: %s', self.path)

        except OSError as ex:
            if ex.errno == errno.EEXIST and os.path.isdir(self.path):
                LOGGER.debug('Cache directory is at: %s', self.path)
            else:
                raise

    def get_attendee_path(self, attendee):
        """
        Get the attendee path and ensures it exists.
        """

        attendee_path = os.path.join(self.path, unicode(attendee))

        try:
            os.makedirs(attendee_path)

            LOGGER.debug('Creating attendee directory: %s', attendee_path)

        except OSError as ex:
            if ex.errno != errno.EEXIST or not os.path.isdir(attendee_path):
                raise

        return attendee_path