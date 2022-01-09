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

""" The main module for UnitTest. Runs all tests for the program. """
import unittest
import unit_test_strmain
import unit_test_perfectsoup


def suite():
    """ Collects all tests from other modules for them running here.

    :return: Object of TestSuit class
    """
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(unit_test_strmain.TestStrMainFunctions))
    testSuite.addTest(unittest.makeSuite(unit_test_perfectsoup.TestPerfectSoupFunctions))

    return testSuite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
