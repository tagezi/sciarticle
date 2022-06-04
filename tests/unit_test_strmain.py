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

""" Provides methods for testing strmain module.  """
import unittest

from sciarticle.lib.strmain import *


class TestStrMain(unittest.TestCase):

    def test_get_value(self):
        """ Can a function split a line containing ",", ";" and "and" to
            the list correctly.
            """
        sString = 'a b, c,d;i; f and g,and j'
        self.assertEqual(get_values(sString),
                         ['a b', 'c', 'd', 'i', 'f', 'g', 'j'])
        with self.assertRaises(TypeError):
            sString.split(1)

    def test_clean_spaces(self):
        """ Checks if non-break spaces and spaces in the start and
            the end of string is removed from a string.
            """
        self.assertEqual(clean_spaces('a b'), 'a b')
        self.assertEqual(clean_spaces(' a b '), 'a b')
        self.assertEqual(clean_spaces('a\xa0b '), 'a b')
        self.assertEqual(clean_spaces(' a b\xa0'), 'a b')

    def test_clean_parens(self):
        """ Checks the removal of parentheses from string with content. """
        self.assertEqual(clean_parens('a(b)'), 'a')
        self.assertEqual(clean_parens('a(b d)'), 'a')
        self.assertEqual(clean_parens('a b (d 12)'), 'a b ')
        self.assertEqual(clean_parens('a[b] c'), 'a c')
        self.assertEqual(clean_parens('(a b) c[d]'), ' c')

    def test_clean_string(self):
        """ Checks the removal of parentheses and double spaces. """
        self.assertEqual(clean_string('a(b)'), 'a')
        self.assertEqual(clean_string(' a(b d)'), 'a')
        self.assertEqual(clean_string('a b (d 12) '), 'a b')
        self.assertEqual(clean_string(' a[b]\xa0c '), 'a c')
        self.assertEqual(clean_string('(a b) c[d]'), 'c')

    def test_iri_to_uri(self):
        """ Checks for correct change of UTF-8 characters to ascii in IRI. """
        sQueryString = 'https://en.wikipedia.org/wiki/Americ' \
                       'än_Journal_of_Law_&_Medicine'
        sAnsverSrting = 'https://en.wikipedia.org/wiki/Americ%C3' \
                        '%A4n_Journal_of_Law_%26_Medicine'
        self.assertEqual(iri_to_uri(sQueryString), sAnsverSrting)

    def test_get_filename_time(self):
        """ Checks if the date and time are correctly change in the file name.
            """
        sQueryString = 'backup.file/main.file.csv'
        oTime = localtime()
        sTime = strftime("%Y%m%d%H%M%S", oTime)
        lDirAndFile = splitext(sQueryString)
        sAnsverSrting = lDirAndFile[0] + "_" + sTime + lDirAndFile[-1]
        self.assertEqual(get_filename_time(sQueryString), sAnsverSrting)

    def test_get_filename_patch(self):
        """ Checks if join patch and normalisation with OS rules"""
        self.assertEqual(get_file_patch('db.files', 'file.csv'),
                         normcase(join('db.files', 'file.csv')))
        self.assertEqual(get_file_patch('db.files/', 'file.csv'),
                         normcase(join('db.files', 'file.csv')))

    def test_split_by_and(self):
        """ Checks if string is separated to list by '&' and 'and'. """
        sTested = 'a and b'
        self.assertEqual(['a', 'b'], split_by_and(sTested))

        sTested = 'a & b'
        self.assertEqual(['a', 'b'], split_by_and(sTested))

    def test_str_to_year(self):
        """ Checks if it can choose numbers of year from string. """
        sTested = 'I was born in 1972 year.'
        self.assertEqual(1972, str_to_year(sTested))

        tTested = ('I', 'was', 'born  ', 'in', '1972 ', 'year', '.',)
        self.assertEqual(1972, str_to_year(tTested))

        lTested = ['I', 'was', 'born  ', 'in', '1972 ', 'year', '.']
        self.assertEqual(1972, str_to_year(lTested))

    def test_get_wiki_url(self):
        """ Checks if function return wiki url. """
        sTested = '/wiki/Something'
        sURL = 'https://en.wikipedia.org/wiki/Something'
        self. assertEqual(sURL, get_wiki_url(sTested))

    def test_get_bibtext_author(self):
        """ Checks if the function can separate authors in bibtex string. """
        sTested = 'Mouse Brain and Mouse Pinky and &CO'
        lList = ['Mouse Brain', 'Mouse Pinky', '&CO']
        self.assertEqual(lList, get_bibtext_author(sTested))

    def test_lower_list_values(self):
        """ Checks if the function returns list in low register. """
        lTested = ['Mouse Brain', 'Mouse Pinky']
        lList = ['mouse brain', 'mouse pinky']
        self.assertEqual(lList, lower_list_values(lTested))
        self.assertEqual(['mouse brain'], lower_list_values('Mouse Brain'))


if __name__ == '__main__':
    unittest.main()
