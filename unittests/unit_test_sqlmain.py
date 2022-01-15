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
import logging
import sqlite3
import unittest
from unittest import TestCase

from lib.sqlmain import SQLmain
from lib.strmain import get_file_patch


def type_connector():
    """ Creates temporal object of sqlite3.Connection and return its type.

        :return: The type sqlite3.Connection.
        """
    oConnector = sqlite3.connect(":memory:")
    return type(oConnector)


def fill_db_for_test():
    """ Creates temporal object of sqlite3.Connection for test.

        :return: The Sqlmain object.
    """
    file_script = get_file_patch('files', 'db_script.sql')
    oConnector = SQLmain(":memory:")
    sSQL = ''
    with open(file_script, "r") as f:
        for s in f:
            sSQL = sSQL + s

    oConnector.execute_script(sSQL)
    return oConnector


def suite():
    oSuite = unittest.TestSuite()
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

    return oSuite


class TestSQLiteMain(TestCase):
    """ A set of methods for checking the functionality of the SQLmain module
    """

    def test_sqlmain__init__(self):
        """ Check if the object being created has an instance of
            the sqlite3.Connection class.
            """
        oConnect = SQLmain(":memory:")
        self.assertEqual(type(oConnect.oConnect), type_connector(), )
        del oConnect

    def test_sqlmain_execute(self):
        """ Check if execute_script and execute_query work. """
        oConnector = fill_db_for_test()
        oCursor = oConnector.execute_query('SELECT discipline_name '
                                           'FROM Discipline '
                                           'WHERE discipline_name="air"')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'air')
        del oConnector

    def test_sqlmain_insert_row(self):
        """ Check if insert_row work correctly. """
        oConnector = fill_db_for_test()
        bIns = oConnector.insert_row('Discipline',
                                     'discipline_name', ('check',))
        self.assertTrue(bIns)

        oCursor = oConnector.execute_query('SELECT discipline_name '
                                           'FROM Discipline '
                                           'WHERE discipline_name="check"')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'check')

        logging.disable(logging.CRITICAL)
        bIns = oConnector.insert_row('Discipline',
                                     'discipline_name', ('check_too', 1, 2))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_select(self):
        """ Check if select work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        oCursor = oConnector.select('Discipline', 'discipline_name',
                                    'discipline_name', ('check',))
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'check')

        oCursor = oConnector.select('Discipline', 'discipline_name')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'air')
        self.assertEqual(lRows[1][0], 'check')

        oCursor = oConnector.select('Discipline', '*', sFunc='Count')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 2)
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))

        oCursor = oConnector.select('Discipline',
                                    'discipline_name', sFunc='DISTINCT')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'air')
        self.assertEqual(lRows[1][0], 'check')
        del oConnector

    def test_sqlmain_delete_row(self):
        """ Check if delete_row work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        iDel = oConnector.delete_row('Discipline',
                                     'discipline_name', ('check',))
        self.assertTrue(iDel)
        oCursor = oConnector.select('Discipline', 'discipline_name',
                                    'discipline_name', ('check',))
        lRows = oCursor.fetchall()
        self.assertFalse(lRows)
        oCursor = oConnector.select('Discipline', 'discipline_name',
                                    'discipline_name', ('air',))
        lRows = oCursor.fetchall()
        self.assertTrue(lRows)

        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        iDel = oConnector.delete_row('Discipline')
        self.assertTrue(iDel)
        lRows = oConnector.sql_count('Discipline')
        self.assertEqual(lRows, 0)
        del oConnector

    # TODO: test for export_db
    def test_sqlmain_export_db(self):
        """ Check if export_db work correctly. """
        oConnector = fill_db_for_test()
        del oConnector

    def test_sqlmain_sql_count(self):
        """ Check if sql_count work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        oCursor = oConnector.select('Discipline', '*', sFunc='Count')
        lRowsLow = oCursor.fetchall()
        lRowsAverage = oConnector.sql_count('Discipline')
        self.assertEqual(lRowsLow[0][0], lRowsAverage)
        del oConnector

    def test_sqlmain_sql_get_all(self):
        """ Check if sql_get_all work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        oCursor = oConnector.select('Discipline', '*')
        lRowsLow = oCursor.fetchall()
        lRowsAverage = oConnector.sql_get_all('Discipline')
        self.assertEqual(lRowsLow[0][0], lRowsAverage[0][0])
        self.assertEqual(lRowsLow[1][0], lRowsAverage[1][0])

        lRows = oConnector.sql_get_all('Mistake')
        self.assertFalse(lRows)
        del oConnector

    def test_sqlmain_sql_get_id(self):
        """ Check if sql_get_id work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        oCursor = oConnector.select('Discipline', 'id_discipline',
                                    'discipline_name', ('check',))
        lRowsLow = oCursor.fetchall()
        lRowsAverage = oConnector.sql_get_id('Discipline', 'id_discipline',
                                             'discipline_name', ('check',))
        self.assertEqual(lRowsLow[0][0], lRowsAverage)

        lRow = oConnector.sql_get_id('Mistake', 'id_discipline',
                                     'discipline_name', ('check',))
        self.assertEqual(lRow, 0)
        del oConnector

    def test_sqlmain_sql_table_clean(self):
        """ Check if sql_table_clean work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        iDel = oConnector.delete_row('Discipline')
        self.assertTrue(iDel)
        lRows = oConnector.sql_count('Discipline')
        self.assertEqual(lRows, 0)

        iDel = oConnector.delete_row('Mistake')
        self.assertFalse(iDel)
        del oConnector

    def test_sqlmain_q_get_id_country(self):
        """ Check if q_get_id_country work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Country', 'en_name_country', ('check',))
        lRowsAverage = oConnector.sql_get_id('Country', 'id_country',
                                             'en_name_country', ('check',))
        lRowsHigh = oConnector.q_get_id_country('check')
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_country('Mistake')
        self.assertEqual(lRow, 0)
        del oConnector

    def test_sqlmain_q_get_id_dspln(self):
        """ Check if q_get_id_dspln work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        lRowsAverage = oConnector.sql_get_id('Discipline', 'id_discipline',
                                             'discipline_name', ('check',))
        lRowsHigh = oConnector.q_get_id_dspln('check')
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_dspln('Mistake')
        self.assertEqual(lRow, 0)
        del oConnector

    def test_sqlmain_q_get_id_lang(self):
        """ Check if q_get_id_lang work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Lang', 'lang', ('check',))
        lRowsAverage = oConnector.sql_get_id('Lang', 'id_lang',
                                             'lang', ('check',))
        lRowsHigh = oConnector.q_get_id_lang('check')
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_lang('Mistake')
        self.assertEqual(lRow, 0)
        del oConnector

    def test_sqlmain_q_get_id_lang_by_name(self):
        """ Check if q_get_id_lang_by_name work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('LangVariant', 'id_lang, lang', (2, 'check',))
        lRowsAverage = oConnector.sql_get_id('LangVariant', 'id_lang',
                                             'lang', ('check',))
        lRowsHigh = oConnector.q_get_id_lang_by_name('check')
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_lang_by_name('Mistake')
        self.assertEqual(lRow, 0)
        del oConnector

    def test_sqlmain_q_get_id_publisher(self):
        """ Check if q_get_id_publisher work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Publisher', 'publisher_name', ('check',))
        lRowsHigh = oConnector.q_get_id_publisher('check')
        self.assertEqual(lRowsHigh, 1)

        lRow = oConnector.q_get_id_publisher('Mistake')
        self.assertEqual(lRow, 0)
        del oConnector

    def test_sqlmain_q_insert_book_dspln(self):
        """ Check if q_insert_book_dspln work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Book', 'book_name', ('check1',))
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        bIns = oConnector.q_insert_book_dspln((1, 1,))
        self.assertTrue(bIns)

        bIns = oConnector.q_insert_book_dspln((1, 'check',))
        self.assertTrue(bIns)

        bIns = oConnector.q_insert_book_dspln(('check1', 'check',))
        self.assertTrue(bIns)

        bIns = oConnector.q_insert_book_dspln(('check1', 1,))
        self.assertTrue(bIns)

        logging.disable(logging.CRITICAL)
        bIns = oConnector.q_insert_book_dspln((1, 2, 3,))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_book_editor(self):
        """ Check if q_insert_book_editor work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Book', 'book_name', ('check',))
        bIns = oConnector.q_insert_book_editor((1, 'Check',))
        self.assertTrue(bIns)

        logging.disable(logging.CRITICAL)
        bIns = oConnector.q_insert_book_editor(('Check',))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_book_lang(self):
        """ Check if q_insert_book_lang work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Book', 'book_name', ('check1',))
        oConnector.insert_row('Lang', 'lang', ('check',))
        oConnector.insert_row('LangVariant', 'id_lang, lang', (1, 'check',))
        bIns = oConnector.q_insert_book_lang((1, 1,))
        self.assertTrue(bIns)

        bIns = oConnector.q_insert_book_lang((1, 'check',))
        self.assertTrue(bIns)

        bIns = oConnector.q_insert_book_lang(('check1', 'check',))
        self.assertTrue(bIns)

        bIns = oConnector.q_insert_book_lang(('check1', 1,))
        self.assertTrue(bIns)

        logging.disable(logging.CRITICAL)
        bIns = oConnector.q_insert_book_lang((1, 2, 3,))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_dspln(self):
        """ Check if q_insert_dspln work correctly. """
        oConnector = fill_db_for_test()
        bIns = oConnector.q_insert_dspln(('check', 1,))
        self.assertTrue(bIns)
        lRows = oConnector.q_get_id_dspln('check')
        self.assertEqual(lRows, 2)

        logging.disable(logging.CRITICAL)
        bIns = oConnector.q_insert_dspln(('check_too', 1, 2))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_lang(self):
        """ Check if q_insert_lang work correctly. """
        oConnector = fill_db_for_test()
        bIns = oConnector.q_insert_lang(('check',))
        self.assertTrue(bIns)
        lRows = oConnector.q_get_id_lang('check')
        self.assertEqual(lRows, 1)
        del oConnector

    def test_sqlmain_q_insert_lang_var(self):
        """ Check if q_insert_lang_var work correctly. """
        oConnector = fill_db_for_test()
        bIns = oConnector.q_insert_lang(('check',))
        self.assertTrue(bIns)
        lRows = oConnector.q_get_id_lang('check')
        self.assertEqual(lRows, 1)
        del oConnector

    def test_sqlmain_q_update_book(self):
        """ Check if q_update_book work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Book', 'book_name', ('air',))
        bIns = oConnector.q_update_book('book_name', ('check', 1))
        self.assertTrue(bIns)
        lRows = oConnector.sql_get_id('Book',
                                      'id_book', 'book_name', ('check',))
        self.assertEqual(lRows, 1)
        del oConnector

    def test_sqlmain_q_update_publisher(self):
        """ Check if q_update_publisher work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Publisher', 'publisher_name', ('Air',))
        bIns = oConnector.q_update_publisher('publisher_name', ('check', 1,))
        self.assertTrue(bIns)
        lRows = oConnector.q_get_id_publisher('check')
        self.assertEqual(lRows, 1)
        del oConnector


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
