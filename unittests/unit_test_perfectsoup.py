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
import sys
import unittest

# TODO: It doesn't work, if script called from command line
#       in directory one level higher.
sys.path.append('../')
sys.path.append('../lib/')
try:
    from lib.perfect_soup import *
except ImportError as e:
    print(str(e))
    sys.exit()


class TestPerfectSoup(unittest.TestCase):

    def test_perfectsoup_get_html(self):
        """ Checks the type of the returned class of function get_html(sURL)
            from perfectSoup module """
    #     sQueryString = 'https://en.wikipedia.org/wiki' \
    #                    '/American_Journal_of_Law_&_Medicine'
    #     html = urlopen('https://ru.wikipedia.org/')
    #     self.assertEqual(type(PerfectSoup(sQueryString)),
    #                      type(BeautifulSoup(sQueryString, "html5lib")))


if __name__ == '__main__':
    unittest.main()
