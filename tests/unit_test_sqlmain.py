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

from sciarticle.lib.sqlmain import *
from sciarticle.lib.strmain import get_file_patch


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
    oSuite.addTest(TestSQLiteMain('test_sqlmain_get_columns'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain__init__'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_execute'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_insert_row'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_select'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_sql_count'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_delete_row'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_sql_get_all'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_sql_get_id'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_sql_table_clean'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_author'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_book'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_country'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_dspln'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_keyword'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_lang'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_lang_by_name'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_publisher'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_publ_type'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_publication'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_get_id_lang_by_name'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_authors'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_book'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_book_dspln'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_book_editor'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_book_lang'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_dspln'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_keyword'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_lang'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_lang_var'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_publ_author'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_publ_keywords'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_publ_lang'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_insert_publ_url'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_update_publisher'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_q_update_book'))
    oSuite.addTest(TestSQLiteMain('test_sqlmain_export_db'))

    return oSuite


class TestSQLiteMain(TestCase):
    """ A set of methods for checking the functionality of the SQLmain module
    """
    def test_sqlmain_get_columns(self):
        """ Check if the function of separating column work. """
        sString = get_columns('check, check, check')
        sAnswer = 'check=? AND check=? AND check=?'
        self.assertEqual(sString, sAnswer)

        sString = get_columns('check')
        sAnswer = 'check=?'
        self.assertEqual(sString, sAnswer)

    def test_sqlmain_get_increase_value(self):
        sString = get_increase_value('check, check, check', ('Check',))
        sAnswer = ('Check', 'Check', 'Check')
        self.assertEqual(sString, sAnswer)

        sString = get_increase_value('check, check, check', ('this', 'Check',))
        sAnswer = ''
        self.assertEqual(sString, sAnswer)

    def test_sqlmain__init__(self):
        """ Check if the object being created has an instance of
            the sqlite3.Connection class.
            """
        oConnector = SQLmain(":memory:")
        self.assertEqual(type(oConnector.oConnector), type_connector(), )
        del oConnector

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
        iIDIns = oConnector.insert_row('Discipline',
                                       'discipline_name', ('check',))
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
        """ Check if delete_row work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        iDel = oConnector.delete_row('Discipline')
        self.assertTrue(iDel)
        lRows = oConnector.sql_count('Discipline')
        self.assertEqual(lRows, 0)

        iDel = oConnector.delete_row('Mistake')
        self.assertFalse(iDel)
        del oConnector

    def test_sqlmain_q_get_id_author(self):
        """ Check if q_get_id_author work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Author', 'author_name', ('check',))
        lRowsAverage = oConnector.sql_get_id('Author', 'id_author',
                                             'author_name', ('check',))
        lRowsHigh = oConnector.q_get_id_author('check')
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_author('Mistake')
        self.assertEqual(lRow, 2)
        del oConnector

    def test_sqlmain_q_get_id_book(self):
        """ Check if q_get_id_book work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Book', 'book_name', ('check',))
        lRowsAverage = oConnector.sql_get_id('Book', 'id_book',
                                             'book_name', ('check',))
        lRowsHigh = oConnector.q_get_id_book('check', '', '')
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_book('Mistake', '', '')
        self.assertEqual(lRow, 0)
        lRow = oConnector.sql_count('Publisher')
        self.assertEqual(lRow, 0)

        lRow = oConnector.q_get_id_book('Mistake', 'Checker', '123-456')
        self.assertEqual(lRow, 2)

        oCursor = oConnector.select('Book', 'publisher',
                                    'book_name', ('Mistake',))
        lRowsLow = oCursor.fetchall()
        iNum = oConnector.sql_count('Publisher')
        self.assertEqual(iNum, lRowsLow[0][0])
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

    def test_sqlmain_q_get_id_keyword(self):
        """ Check if q_get_id_keyword work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Keywords', 'keyword', ('check',))
        lRowsAverage = oConnector.sql_get_id('Keywords', 'id_keyword',
                                             'keyword', ('check',))
        lRowsHigh = oConnector.q_get_id_keyword('check')
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_keyword('Mistake')
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

    def test_sqlmain_q_get_id_publ_type(self):
        """ Check if q_get_id_publ_type work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('PublicationType', 'name_type', ('check',))
        lRowsAverage = oConnector.sql_get_id('PublicationType', 'id_publ_type',
                                             'name_type', ('check',))
        lRowsHigh = oConnector.q_get_id_publ_type('check')
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_publ_type('Mistake')
        self.assertEqual(lRow, 0)
        del oConnector

    def test_sqlmain_q_get_id_publication(self):
        """ Check if q_get_id_publication work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Publication',
                              'year, publ_name, id_book',
                              ('check', 'check1', 'check2',))
        lRowsAverage = oConnector.sql_get_id('Publication',
                                             'id_publ',
                                             'year, publ_name, id_book',
                                             ('check', 'check1', 'check2',))
        lRowsHigh = oConnector.q_get_id_publication(('check', 'check1',
                                                     'check2', '', ''))
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRowsHigh = oConnector.q_get_id_publication(('check', 'check1', 1,))
        self.assertEqual(lRowsHigh, lRowsAverage)

        lRow = oConnector.q_get_id_publication(('Mistake', 'check1',
                                                'check2', 'check3', ''))
        self.assertEqual(lRow, 0)
        del oConnector

    def test_sqlmain_q_get_id_publisher(self):
        """ Check if q_get_id_publisher work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Publisher', 'publisher_name', ('check',))
        lRowsHigh = oConnector.q_get_id_publisher('check')
        self.assertEqual(lRowsHigh, 1)
        iNum = oConnector.sql_count('Publisher')
        self.assertEqual(lRowsHigh, iNum)

        lRow = oConnector.q_get_id_publisher('Mistake')
        self.assertEqual(lRow, 2)
        del oConnector

    def test_sqlmain_q_insert_authors(self):
        """ Check if q_insert_authors work correctly. """
        oConnector = fill_db_for_test()
        bIns = oConnector.q_insert_authors('check')
        iSel = oConnector.q_get_id_author('check')
        self.assertTrue(bIns)
        self.assertEqual(iSel, bIns)

        bIns = oConnector.q_insert_authors(None)
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_book(self):
        """ Check if q_insert_book_editor work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Publisher', 'publisher_name', ('Checker',))
        bIns = oConnector.q_insert_book('check', 1, '123-456')
        iSel = oConnector.q_get_id_book('check', 1, '123-456')
        self.assertTrue(bIns)
        self.assertEqual(iSel, bIns)
        bIns = oConnector.q_insert_book('check1', 'Checker', '123-234')
        iSel = oConnector.q_get_id_book('check1', 2, '123-234')
        self.assertTrue(bIns)
        self.assertEqual(iSel, bIns)

        del oConnector

    def test_sqlmain_q_insert_book_dspln(self):
        """ Check if q_insert_book_dspln work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Book', 'book_name', ('check1',))
        oConnector.insert_row('Discipline', 'discipline_name', ('check',))
        bIns = oConnector.q_insert_book_dspln((1, 1,))
        iSel = oConnector.sql_get_id('BookDiscipline', 'id_book_discipline',
                                     'id_book, id_discipline', (1, 1,))
        self.assertTrue(bIns)
        self.assertEqual(bIns, iSel)

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
        oConnector.q_insert_lang(('check',))
        oConnector.q_insert_lang_var((1, 'check',))
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

    def test_sqlmain_q_insert_keyword(self):
        """ Check if q_insert_keyword work correctly. """
        oConnector = fill_db_for_test()
        bIns = oConnector.q_insert_keyword('check1')
        iSel = oConnector.q_get_id_keyword('check1')
        self.assertTrue(bIns)
        self.assertEqual(iSel, bIns)

        bIns = oConnector.q_insert_keyword(None)
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_lang(self):
        """ Check if q_insert_lang work correctly. """
        oConnector = fill_db_for_test()
        bIns = oConnector.q_insert_lang(('check',))
        self.assertTrue(bIns)
        lRows = oConnector.q_get_id_lang('check')
        self.assertEqual(lRows, 1)

        # Func q_insert_lang adds empty values up to 8 automatically.
        bIns = oConnector.q_insert_lang((1, 2, 3, 4, 5, 6, 7, 8,))
        self.assertTrue(bIns)

        bIns = oConnector.q_insert_lang((1, 2, 3, 4, 5, 6, 7, 8, 9,))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_lang_var(self):
        """ Check if q_insert_lang_var work correctly. """
        oConnector = fill_db_for_test()
        oConnector.q_insert_lang(('check',))
        bIns = oConnector.q_insert_lang_var((1, 'check',))
        self.assertTrue(bIns)
        lRows = oConnector.q_get_id_lang_by_name('check')
        self.assertEqual(lRows, 1)

        bIns = oConnector.q_insert_lang_var((1, 2, 3,))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_publ_author(self):
        """ Check if q_insert_publ_author work correctly. """
        oConnector = fill_db_for_test()
        iIDAuthor = oConnector.q_insert_authors('CHECK')
        iIDPublication = oConnector.insert_row('Publications', 'publ_name',
                                               ('check',))
        bIns = oConnector.q_insert_publ_author((iIDPublication, iIDAuthor,))
        self.assertTrue(bIns)
        lRows = oConnector.sql_get_id('PublicationAuthor', 'id_publ_author',
                                      'id_publ, id_author', (1, 1))
        self.assertEqual(lRows, 1)

        bIns = oConnector.q_insert_publ_author((1, 2, 3,))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_publ_lang(self):
        """ Check if q_insert_publ_lang work correctly. """
        oConnector = fill_db_for_test()
        iIDLAng = oConnector.q_insert_lang(('check', 'ar', 'abc'))
        iIDPublication = oConnector.insert_row('Publications', 'publ_name',
                                               ('check',))
        bIns = oConnector.q_insert_publ_lang((iIDPublication, iIDLAng,))
        self.assertTrue(bIns)
        lRows = oConnector.sql_get_id('PublicationLang', 'id_publ_lang',
                                      'id_publ, id_lang', (1, 1))
        self.assertEqual(lRows, 1)

        bIns = oConnector.q_insert_publ_lang((1, 2, 3,))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_publ_url(self):
        """ Check if q_insert_publ_url work correctly. """
        oConnector = fill_db_for_test()
        iIDPublication = oConnector.insert_row('Publications', 'publ_name',
                                               ('check',))
        bIns = oConnector.q_insert_publ_url((iIDPublication, 'check_url',))
        self.assertTrue(bIns)
        lRows = oConnector.sql_get_id('PublicationUrl', 'id_url',
                                      'id_publ', (1,))
        self.assertEqual(lRows, 1)

        bIns = oConnector.q_insert_publ_url((1, 2, 3,))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_insert_publ_keywords(self):
        """ Check if q_insert_publ_keywords work correctly. """
        oConnector = fill_db_for_test()
        iIDKeyword = oConnector.q_insert_keyword('CHECK')
        iIDPublication = oConnector.insert_row('Publications', 'publ_name',
                                               ('check',))
        bIns = oConnector.q_insert_publ_keywords((iIDPublication, iIDKeyword,))
        self.assertTrue(bIns)
        lRows = oConnector.sql_get_id('PublicationKeywords',
                                      'id_publ_keyword',
                                      'id_publ, id_keyword', (1, 1))
        self.assertEqual(lRows, 1)

        bIns = oConnector.q_insert_publ_keywords((1, 2, 3,))
        self.assertFalse(bIns)
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
        bIns = oConnector.q_update_book('book_name', (1, 2, 3,))
        self.assertFalse(bIns)
        del oConnector

    def test_sqlmain_q_update_publisher(self):
        """ Check if q_update_publisher work correctly. """
        oConnector = fill_db_for_test()
        oConnector.insert_row('Publisher', 'publisher_name', ('Air',))
        bIns = oConnector.q_update_publisher('publisher_name', ('check', 1,))
        self.assertTrue(bIns)
        lRows = oConnector.q_get_id_publisher('check')
        self.assertEqual(lRows, 1)
        bIns = oConnector.q_update_publisher('publisher_name', (1, 2, 3,))
        self.assertFalse(bIns)
        del oConnector


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())