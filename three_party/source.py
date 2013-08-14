"""
3party 'Source' class.
"""

from three_party.fetchers import get_fetcher_class_from_shortname, guess_fetcher_instance


def make_sources(sources):
    """
    Build a list of Source instances.

    `sources` can be either a simple location string, a dictionary, or an
    iterable of strings and/or dictionaries.

    If `sources` is false, an empty list is returned.
    """

    if not sources:
        return []

    elif isinstance(sources, basestring):
        return [
            Source(
                location=unicode(sources),
                fetcher_class=guess_fetcher_instance,
            ),
        ]

    elif isinstance(sources, dict):
        return [
            Source(
                location=sources.get('location'),
                fetcher_class=get_fetcher_class_from_shortname(
                    sources.get('fetcher')
                ),
            ),
        ]

    return sum(map(make_sources, sources), [])


class Source(object):

    """
    A Source instance holds information about where and how to get a
    third-party software.
    """

    def __init__(self, location, fetcher_class):
        """
        Create a Source instance.

        `location` is the origin of the third-party software archive to get.
        Its format an meaning depends on the associated `fetcher_class`.
        """

        self.location = location
        self.fetcher_class = fetcher_class
        self.__fetcher = None

    @property
    def fetcher(self):
        """
        Get the associated fetcher instance.
        """

        if self.__fetcher is None:
            self.__fetcher = self.fetcher_class(self.location)

        return self.__fetcher
