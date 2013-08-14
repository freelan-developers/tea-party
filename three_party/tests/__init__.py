"""
three-party unit tests.
"""

import os
import unittest

from three_party.party import load_party_file


class TestThreeParty(unittest.TestCase):

    def setUp(self):
        self.fixtures_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'fixtures'
            )
        )
        self.party_file = os.path.join(self.fixtures_path, 'party.yaml')

    def test_parsing(self):
        party = load_party_file(self.party_file)
        self.assertIn('boost', party.attendees)
        self.assertIn('libiconv', party.attendees)
