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

from unit_test_pep8 import TestPEP8
from unit_test_sqlmain import TestSQLiteMain
from unit_test_strmain import TestStrMain
from unit_test_perfectsoup import TestPerfectSoup


def suite():
    """ Collects all tests from other modules for them running here.

    :return: Object of TestSuit class
    """
    oSuite = unittest.TestSuite()
    oSuite.addTest(unittest.makeSuite(TestPEP8))
    oSuite.addTest(TestSQLiteMain('test_sqlmain__init__'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_execute'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_insert_row'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_select'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_sql_count'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_delete_row'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_sql_get_all'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_sql_get_id'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_sql_table_clean'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_country'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_dspln'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_lang'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_lang_by_name'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_publisher'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_lang_by_name'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_book_dspln'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_book_editor'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_book_lang'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_dspln'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_lang'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_lang_var'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_update_publisher'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_update_book'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_export_db'))
    oSuite.addTest(unittest.makeSuite(TestStrMain))
    oSuite.addTest(unittest.makeSuite(TestPerfectSoup))

    return oSuite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
