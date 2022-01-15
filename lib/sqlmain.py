#     This code is a part of program Science Articles Orderliness
#   Copyright (C) 2021  Valerii Goncharuk (aka tagezi)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
import logging
import sqlite3
from sqlite3 import DatabaseError

from lib.logmain import start_logging


def get_columns(sColumns):
    """ Method of parsing a string, accepts a list of table columns separated
    by commas and returns this list with =? AND as separator.

    :param sColumns: a string with a list of table columns separated by commas.
    :return: the string with a list of table columns separated by '=? AND'.
    """
    return sColumns.replace(", ", "=? AND") + "=?"


class SQLmain():
    """
    Provides interface for working with database from others scripts.

    :methods:
    * Standard methods.
      :__init__: Method initializes a cursor of sqlite database.
      :__del__: Method closes the cursor of sqlite database.
    * Low level methods.
      :export_db: Method exports from db to sql script.
      :execute_script: Method imports from slq script to db.
      :execute_query: Method execute sql_search query.
      :insert_row: Method inserts a record in the database table.
      :delete_row: Method deletes a row from the table.
      :update: Method updates value(s) in record of the database table.
      :select: Method does selection from the table.
    * Average level API.
      :sql_get_id: Method finds id of the row by value(s) of table column(s).
      :sql_get_all: Method gets all records in database table.
      :sql_count: Method counts number of records in database table.
      :sql_table_clean: Method cleans up the table.
    * High API level.
      :q_get_id_country: Method returns country id from Country table by name.
      :q_get_id_dspln: Method returns discipline id from
                       Discipline table by lang name.
      :q_get_id_lang: Method returns lang id from Lang table by lang name.
      :q_get_id_lang_by_name: Method returns lang id from LangVariant by lang.
      :q_get_id_publisher: Method returns publisher id from Publisher by lang.
      :q_insert_book_dspln: Method inserts values into BookDiscipline table.
      :q_insert_book_editor: Method inserts values into Editor table.
      :q_insert_dspln: Method inserts values into Discipline table.
      :q_insert_lang: Method inserts values into Lang table.
      :q_insert_lang_var: Method inserts values into LangVariant table.
      :q_update_book: Method update values into Book table by id_book.
      :q_update_publisher: Method update values into Publisher table
                           by id_publisher.
    """

    # Standard methods
    def __init__(self, sFileDB):
        """ Initializes connect with database.

        :param sFileDB: Path to database as string.
        """
        try:
            self.oConnect = sqlite3.connect(sFileDB)
        except DatabaseError as e:
            logging.exception('An error has occurred: %s.\n'
                              'String of query: %s \n', e, sFileDB)
        self.logging = start_logging()

    def __del__(self):
        """ Closes connection with the database. """
        self.oConnect.close()

    # Low methods level
    def export_db(self):
        """ Method exports from db to sql script. """
        return self.oConnect.iterdump()

    def execute_script(self, SQL):
        """ Method executes sql script.

        The main difference from the method is the ability to execute
        several commands at the same time. For example, using this method,
        you can restore the database from sql dump.

        :param SQL: SQL Script as string.
        :return: True if script execution is successful, otherwise False.
        """
        oCursor = self.oConnect.cursor()
        try:
            oCursor.executescript(SQL)
        except DatabaseError as e:
            logging.exception('An error has occurred: %s.\n'
                              'String of query: %s \n', e, SQL)
            return False

        return True

    def execute_query(self, sqlString, cValues=None):
        """ Method executes sql script.

        :param sqlString: SQL query as string.
        :param cValues: value(s) that need to safe inserting into query
                        (by default, None).
        :return: True if script execution is successful, otherwise False.
        """
        oCursor = self.oConnect.cursor()
        try:
            if cValues is None:
                oCursor.execute(sqlString)
            else:
                oCursor.execute(sqlString, cValues)
        except DatabaseError as e:
            logging.exception('An error has occurred: %s.\n'
                              'String of query: %s \n'
                              'Parameters^ %s', e, sqlString, cValues)
            return False

        return oCursor

    def insert_row(self, sTable, sColumns, cValues):
        """ Inserts a record in the database table.

        :param sTable: Table name as string.
        :param sColumns: Columns names of the table by where needs inserting.
        :param cValues: Value(s) as tuple for inserting.
        :return: True if the insert was successful, otherwise False.
        """
        sSQL = ("?, " * len(sColumns.split(", ")))[:-2]
        sqlString = "INSERT INTO " \
                    + sTable + " (" + sColumns + ") VALUES (" + sSQL + ") "
        oCursor = self.execute_query(sqlString, cValues)
        if not oCursor:
            return False

        self.oConnect.commit()
        return True

    def delete_row(self, sTable, sColumns=None, cValues=None):
        """ Deletes row in the database table by value(s).

        :param sTable: A table as string in where need to delete row.
        :param sColumns: Column(s) where the value(s) will be found.
                         (by default, None).
        :param cValues: value(s) as tuple for search of rows.
                        (by default, None).
        :return: True if the deletion is successful, otherwise False.
        """
        if sColumns is not None:
            sqlString = 'DELETE FROM ' + sTable + ' WHERE ' + \
                        get_columns(sColumns)
            oCursor = self.execute_query(sqlString, cValues)
        else:
            sqlString = "DELETE FROM " + sTable
            oCursor = self.execute_query(sqlString)

        if not oCursor:
            return False

        self.oConnect.commit()
        return True

    def update(self, sTable, sSetUpdate, sWhereUpdate, cValues):
        """ Updates value(s) in the record of the database table.

        :param sTable: A Table as string where update is need to do.
        :param sSetUpdate: Column(s) where the value are writen.
        :param sWhereUpdate: A column where values correspond to the required.
        :param cValues: value(s) as tuple for search corresponding rows.
        :return: True if the insert was successful, otherwise False.
        """
        sSetUpdate = sSetUpdate + "=?"
        sWhereUpdate = get_columns(sWhereUpdate)
        sqlString = "UPDATE " + sTable + " SET " + sSetUpdate + \
                    " WHERE " + sWhereUpdate + " "
        oCursor = self.execute_query(sqlString, cValues)
        if not oCursor:
            return False

        self.oConnect.commit()
        return True

    def select(self, sTable, sGet, sWhere=None, cValues=None, sFunc=None):
        """ Looks for row by value(s) in table column(s).

        :param sTable: Table name as string.
        :param sGet: Name of the column of the table, which will be returned.
        :param sWhere: Names of columns of the table, by which to search
                       (by default, None).
        :param cValues: Value(s) as tuple for search
                        (by default, None).
        :param sFunc: Function name of sqlite, which need to apply
                      (by default, None). Now, you can use only two sqlite
                      functions: Count and DISTINCT.
        :return: Cursor object within rows that was found, or False,
                 if the row not found.
        """
        if sFunc == 'Count':
            sGet = 'Count(' + sGet + ')'
        elif sFunc == 'DISTINCT':
            sGet = sFunc + ' ' + sGet

        if sWhere is not None:
            sCol = get_columns(sWhere)
            sqlString = "SELECT " + sGet + " FROM " + sTable + " WHERE " + sCol
            oCursor = self.execute_query(sqlString, cValues)
        else:
            oCursor = self.execute_query("SELECT " + sGet + " FROM " + sTable)
        if not oCursor:
            return False

        return oCursor

    # Average API level
    def sql_get_id(self, sTable, sID, sColumns, cValues):
        """ Looks for ID of the row by value(s) of table column(s).

        :param sTable: Table name as string.
        :param sID: Name of the column of the table by which to search.
        :param sColumns: Names of columns of the table by which to search.
        :param cValues: Value(s) as tuple for search.
        :return: ID as Number in the row cell, or 0, if the row not found.
        """
        sCol = get_columns(sColumns)
        sqlString = "SELECT " + sID + " FROM " + sTable + " WHERE " + sCol
        oCursor = self.execute_query(sqlString, cValues)
        if not oCursor:
            return False
        else:
            row = oCursor.fetchall()

            if not row:
                return 0
            else:
                return row[0][0]

    def sql_get_all(self, sTable):
        """ Gets all records in database table.

        :param sTable: Table name as string where records should be received.
        :return: Tuple of all rows of table.
        """
        oCursor = self.execute_query("SELECT * FROM " + sTable)
        if not oCursor:
            return False

        return oCursor.fetchall()

    def sql_count(self, sTable):
        """ Counts number of records in database table.

        :param sTable: Table name as string where records should be count.
        :return: Number of found records.
        """
        # sTable, sGet, sWhere, cValues, sFunc=None
        oCursor = self.select(sTable, '*', None, None, 'Count')
        if not oCursor:
            return False

        row = oCursor.fetchall()
        return row[0][0]

    def sql_table_clean(self, lTable):
        """ Cleans up the table.

        :param lTable: Table names as list or tuple of string, or
                       table name as string where cleaning is need to do.
        """
        if type(lTable) == str:
            lTable = [lTable]

        for sTable in lTable:
            bDel = self.delete_row(sTable)
            if not bDel:
                return False

        return True

    # High API level
    def q_get_id_book(self, sValue):
        """ Returns book id from Book table by book name.

            :param sValue: Values of book name, book authors, and year.
            :return: A value from id_book column in selected row.
            """
        return self.sql_get_id("Book", 'id_book',
                               'book_name', (sValue,))

    def q_get_id_country(self, sValue):
        """ Returns country id from Country table by country name.

            :param sValue: Value of country name.
            :return: Number from id_country column in selected row.
            """
        return self.sql_get_id("Country", 'id_country',
                               'en_name_country', (sValue,))

    def q_get_id_dspln(self, sValue):
        """ Returns discipline id from Discipline table by discipline name.

            :param sValue: Value of discipline name.
            :return: Number from id_discipline column in selected row.
            """
        return self.sql_get_id('Discipline', 'id_discipline',
                               'discipline_name', (sValue,))

    def q_get_id_lang(self, sValue):
        """ Returns lang id from Lang table by lang name.

        :param sValue: Value of lang name.
        :return: Number from id_lang column in selected row.
        """
        sValue = sValue.strip().lower()
        return self.sql_get_id('Lang', 'id_lang', 'lang', (sValue,))

    def q_get_id_lang_by_name(self, sValue):
        """ Returns lang id from LangVariant table by lang name.

        :param sValue: Value of lang name.
        :return: number from id_lang column in selected row.
        """
        sValue = sValue.strip().lower()
        return self.sql_get_id('LangVariant', 'id_lang', 'lang', (sValue,))

    def q_get_id_publisher(self, sValue):
        """ Returns publisher id from Publisher table by lang name.

            :param sValue: Value of publisher name.
            :return: number from id_publisher column in selected row.
            """
        return self.sql_get_id('Publisher', 'id_publisher',
                               'publisher_name', (sValue,))

    # dspln is accepted abbreviation of word 'discipline'
    def q_insert_book_dspln(self, cValues):
        """ Inserts values into BookDiscipline table.

            :param cValues: Values which need to insert. This parameter
                should contain 2 values: either 2 int, or 1 int and 1 str,
                or 2 str. The first from them should be values of book,
                and the second is discipline.
                Otherwise, an exception will be thrown.
            :return: True, if inserting is successful. Otherwise, False is.
        """
        if type(cValues[0]) == int and type(cValues[1]) == str:
            iIDDspln = self.q_get_id_dspln(cValues[1])
            if not iIDDspln:
                raise NameError('The discipline value %s return bool (%s)'
                                ' value', cValues[1], iIDDspln)
            cValues = (cValues[0], iIDDspln,)

        elif type(cValues[0]) == str:
            iIDBook = self.q_get_id_book(cValues[0])
            if not iIDBook:
                raise NameError('The book values %s, %s, %s return bool (%s)'
                                ' value', cValues[0], iIDBook)

            if type(cValues[1]) == str:
                iIDDspln = self.q_get_id_dspln(cValues[1])
                if not iIDDspln:
                    raise NameError('The discipline value %s return bool (%s)'
                                    ' value', cValues[1], iIDDspln)
                cValues = (iIDBook, iIDDspln,)
            else:
                cValues = (iIDBook, cValues[1],)
        sColumns = 'id_book, id_discipline'

        return self.insert_row('BookDiscipline', sColumns, cValues)

    def q_insert_book_editor(self, lValues):
        """ Inserts values into Editor table.

            :param lValues: Values which need to insert. This parameter should
                            contain 2 values, otherwise will be call exception.
            :return: True if inserting is successful, otherwise False.
            """
        return self.insert_row('BookEditor', 'id_book, editor', lValues)

    def q_insert_book_lang(self, cValues):
        """ Inserts values into BookLang table.

            :param cValues: Values which need to insert. This parameter
                should contain 2 values: either 2 int, or 1 int and 1 str,
                or 2 str. The first from them should be values of book,
                and the second is Lang.
                Otherwise, an exception will be thrown.
            :return: True if inserting is successful, otherwise False.
            """
        if type(cValues[0]) == int and type(cValues[1]) == str:
            iIDLang = self.q_get_id_lang_by_name(cValues[1])
            if not iIDLang:
                raise NameError('The discipline value %s return bool (%s)'
                                ' value', cValues[1], iIDLang)
            cValues = (cValues[0], iIDLang,)

        elif type(cValues[0]) == str:
            iIDBook = self.q_get_id_book(cValues[0])
            if not iIDBook:
                raise NameError('The book values %s, %s, %s return bool (%s)'
                                ' value', cValues[0], iIDBook)

            if type(cValues[1]) == str:
                iIDLang = self.q_get_id_lang_by_name(cValues[1])
                if not iIDLang:
                    raise NameError('The discipline value %s return bool (%s)'
                                    ' value', cValues[1], iIDLang)
                cValues = (iIDBook, iIDLang,)
            else:
                cValues = (iIDBook, cValues[1],)

        return self.insert_row('BookLang', 'id_book, id_lang', cValues)

    def q_insert_dspln(self, lValues):
        """ Inserts values into Discipline table.

            :param lValues: Values which need to insert. This parameter should
                            contain 1 values, otherwise will be call exception.
            :return: True if inserting is successful, otherwise False.
            """
        return self.insert_row('Discipline',
                               'discipline_name, discipline_url', lValues)

    def q_insert_lang(self, cValues):
        """ Inserts values into Lang table.

            :param cValues: Values which need to insert. This parameter should
                            contain 8 values, otherwise will be call exception.
            :return: True if inserting is successful, otherwise False.
            """
        lValues = []
        if len(cValues) < 8:
            for Value in cValues:
                lValues.append(Value)
            while len(lValues) < 8:
                lValues.append('')
            cValues = tuple(lValues)
        sColumns = "lang, iso_639_1, iso_639_2, iso_639_3, " \
                   "iso_639_5, gost_7_75_lat, gost_7_75_rus, d_code "
        return self.insert_row('Lang', sColumns, cValues)

    def q_insert_lang_var(self, cValues):
        """ Inserts values into LangVariant table.

            :param cValues: Values which need to insert.This parameter should
                            contain 2 values, otherwise will be call exception.
            :return: True if inserting is successful, otherwise False.
            """
        return self.insert_row('LangVariant', 'id_lang, lang', cValues)

    def q_update_book(self, sSetUpdate, lValues):
        """ Update values into Book table by id_book.

            :param sSetUpdate: Column(s) where the value are needed to write
            :param lValues: value(s) as tuple for search corresponding rows.
            :return: True if the insert was successful, otherwise False.
            """
        return self.update('Book', sSetUpdate, 'id_book', lValues)

    def q_update_publisher(self, sSetUpdate, lValues):
        """ Update values into Publisher table.

            :param sSetUpdate: Column(s) where the value are needed to write
            :param lValues: value(s) as tuple for search corresponding rows.
            :return: True if the insert was successful, otherwise False.
            """
        return self.update('Publisher', sSetUpdate, 'id_publisher', lValues)
