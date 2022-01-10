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

from lib.strmain import *


class TestStrMainFunctions(unittest.TestCase):

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
        self.assertEqual(clean_parens('a b (d 12)'), 'a b')

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
        self.assertEqual(get_filename_patch('db.files', 'file.csv'),
                         normcase(join('db.files', 'file.csv')))
        self.assertEqual(get_filename_patch('db.files/', 'file.csv'),
                         normcase(join('db.files', 'file.csv')))


if __name__ == '__main__':
    unittest.main()
