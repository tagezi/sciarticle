#     This code is a part of program Science Articles Orderliness
#     Copyright (C) 2021  Valerii Goncharuk (aka tagezi)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
from unittest import TestCase

from sciarticle.lib.publishermain import PublisherValue


def suite():
    oSuite = unittest.TestSuite()
    oSuite.addTest(TestPublisherValue('test_publishermain_get_value'))
    oSuite.addTest(TestPublisherValue('test_publishermain_get_name'))
    oSuite.addTest(TestPublisherValue('test_publishermain__init__'))

    return oSuite


class TestPublisherValue(unittest.TestCase):
    def test_publishermain_get_value(self):
        oPV = PublisherValue(WIKI_URL_2)
        sPredecessor = oPV.get_value('Predecessor')
        self.assertEqual('Verlag Hans Huber', sPredecessor)

        oPV = PublisherValue(WIKI_URL_3)
        sLocation = oPV.get_value('Location')
        self.assertEqual('United States', sLocation)

    def test_publishermain_get_name(self):
        """ Checks if get_name can choose names. """
        oPV = PublisherValue(WIKI_URL_1)
        sFullName = oPV.get_name('FullName')
        self.assertEqual(sFullName, 'ABC-Clio, LLC')
        sShortName = oPV.get_name('ShortName')
        self.assertEqual(sShortName, 'ABC-CLIO')

    def test_publishermain__init__(self):
        """ Checks if __init__ filling members by values. """
        oPV = PublisherValue(WIKI_URL_1)
        oROW = (oPV.sFullName, oPV.sShortName, oPV.ParentCompany,
                oPV.Status, oPV.Predecessor, oPV.sFounder,
                oPV.CountryOfOrigin, oPV.Headquarters, oPV.PublicationTypes,
                oPV.Owner, oPV.sWebsite, oPV.OtherName, oPV.FormerName,
                oPV.Type, oPV.ParentInstitution, oPV.AcademicAffiliation,
                oPV.Location, oPV.Language, oPV.WikiURL,)
        lAnswer = ('ABC-Clio, LLC', 'ABC-CLIO', None, 'Active', None,
                   ['Eric Boehm'], None, 'Santa Barbara, California',
                   ['books', 'databases', 'magazines', 'journals'], None,
                   'http://www.abc-clio.com/', None, None, None, None, None,
                   None, None, 'https://en.wikipedia.org/wiki/ABC-Clio')
        self.assertEqual(oROW, lAnswer)


WIKI_URL_1 = "https://en.wikipedia.org/wiki/ABC-Clio"
WIKI_URL_2 = "https://en.wikipedia.org/wiki/Hogrefe_Publishing_Group"
WIKI_URL_3 = "https://en.wikipedia.org/wiki/American_Chemical_Society"

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
