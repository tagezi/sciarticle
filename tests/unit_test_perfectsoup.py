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

""" Provides methods for testing perfectSoup module. """
import os
import unittest

from files.config import *
from sciarticle.lib.perfect_soup import *


class TestPerfectSoup(unittest.TestCase):

    def test_perfectsoup_get_title_h1(self):
        """ Checks if PerfectSoup gives text from h1 tag """
        oPS = PerfectSoup('file:///' + os.path.abspath(FILE_WITH_TABLE_H1))
        sString = oPS.get_title_h1()
        self.assertEqual(sString, 'Checker')

    def test_perfectsoup_get_column_table(self):
        """ Checks if func gives text from a column of a table. """
        oPS = PerfectSoup('file:///' + os.path.abspath(FILE_WITH_TABLE_H1))
        oTableInfo = oPS.find("table", {"infobox"})
        lAnswer = ['Discipline', 'Language', 'Edited\xa0by',
                   'History', 'Publisher', 'Frequency',
                   'ISO 4', 'ISSN', 'LCCN', 'JSTOR', 'OCLC\xa0no.']
        dTable = {}
        if oTableInfo:
            dTable = get_column_table(oTableInfo, 'th', 'infobox-label')

        self.assertEqual(dTable, lAnswer)

    def test_perfectsoup_tableinfo_to_dict(self):
        """ Checks if method gives text from a column of a table. """
        oPS = PerfectSoup('file:///' + os.path.abspath(FILE_WITH_TABLE_H1))
        dAnswer = {'Discipline': 'Music',
                   'Language': 'English',
                   'Edited\xa0by': 'Lawrence Kramer',
                   'History': '1977â€“present',
                   'Publisher': 'University of California '
                                'Press\xa0(United States)',
                   'Frequency': 'Triannual',
                   'ISO 4': '19th-Century Music',
                   'ISSN': '0148-2076\xa0(print)1533-8606\xa0(web)',
                   'LCCN': '77644140',
                   'JSTOR': '01482076',
                   'OCLC\xa0no.': '8973601',
                   'Journal homepage': 'https://online.ucpress.edu/ncm',
                   'Online access': 'https://online.ucpress.edu/ncm/'
                                    'search-results?page=1&q=&fl_S'
                                    'iteID=1000031&sort=Date+-+Newest+First',
                   'Online archive': 'https://online.ucpress.edu/'
                                     'ncm/issue/browse-by-year'}
        dTable = oPS.tableinfo_to_dict()
        self.assertEqual(dAnswer, dTable)

        oPS = PerfectSoup('file:///' + os.path.abspath(FILE_WITHOUT_TABLE))
        self.assertFalse(oPS.tableinfo_to_dict())

    def test_perfectsoup_get_name_from_bold(self):
        """ Checks if method gives text from bold tags. """
        oPS = PerfectSoup('file:///' + os.path.abspath(FILE_WITH_BOLD_1))
        dAnswer = {'FullName': 'Architecture and the Built Environment',
                   'ShortName': 'A+BE'}
        dBold = oPS.get_name_from_bold()
        self.assertEqual(dAnswer, dBold)

        oPS = PerfectSoup('file:///' + os.path.abspath(FILE_WITH_BOLD_2))
        dBold = oPS.get_name_from_bold()
        self.assertEqual(dAnswer, dBold)

        oPS = PerfectSoup('file:///' + os.path.abspath(FILE_WITH_BOLD_3))
        dAnswer = {'FullName': 'Architecture and the Built Environment'}
        dBold = oPS.get_name_from_bold()
        self.assertEqual(dAnswer, dBold)


if __name__ == '__main__':
    unittest.main()
