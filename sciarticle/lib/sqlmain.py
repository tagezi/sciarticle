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

""" The module provides an API for working with the database. It creates a
    multi-level API that can be used in other modules to create requests using
    a minimum of transmitted data.

    Using:
    Foo = SQLmain(_DataBaseFile_)
    """

import logging
import sqlite3
from sqlite3 import DatabaseError

from sciarticle.lib.logmain import start_logging


def get_columns(sColumns):
    """ Method of parsing a string, accepts a list of table columns separated
    by commas and returns this list with =? AND as separator.

    :param sColumns: a string with a list of table columns separated by commas.
    :return: the string with a list of table columns separated by '=? AND'.
    """
    return sColumns.replace(", ", "=? AND ") + "=?"


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
            :type sFileDB: str
            """
        try:
            self.oConnector = sqlite3.connect(sFileDB)
        except DatabaseError as e:
            logging.exception('An error has occurred: %s.\n'
                              'String of query: %s \n', e, sFileDB)
        self.logging = start_logging()

    def __del__(self):
        """ Closes connection with the database. """
        self.oConnector.close()

    # Low methods level
    def export_db(self):
        """ Method exports from db to sql script. """
        return self.oConnector.iterdump()

    def execute_script(self, SQL):
        """ Method executes sql script.

        The main difference from the method is the ability to execute
        several commands at the same time. For example, using this method,
        you can restore the database from sql dump.

        :param SQL: SQL Script as string.
        :type SQL: str
        :return: True if script execution is successful, otherwise False.
        :rtype: bool
        """
        oCursor = self.oConnector.cursor()
        try:
            oCursor.executescript(SQL)
        except DatabaseError as e:
            logging.exception('An error has occurred: %s.\n'
                              'String of query: %s \n', e, SQL)
            return False

        return True

    def execute_query(self, sqlString, tValues=None):
        """ Method executes sql script.

        :param sqlString: SQL query as string.
        :type sqlString: str
        :param tValues: value(s) that need to safe inserting into query
            (by default, None).
        :type tValues: tuple
        :return: True if script execution is successful, otherwise False.
        :rtype: obj, bool
        """
        oCursor = self.oConnector.cursor()
        try:
            if tValues is None:
                oCursor.execute(sqlString)
            else:
                oCursor.execute(sqlString, tValues)
        except DatabaseError as e:
            logging.exception('An error has occurred: %s.\n'
                              'String of query: %s \n'
                              'Parameters^ %s', e, sqlString, tValues)
            return False

        return oCursor

    def insert_row(self, sTable, sColumns, tValues):
        """ Inserts a record in the database table.

        :param sTable: Table name as string.
        :type sTable: str
        :param sColumns: Columns names of the table by where needs inserting.
        :type sColumns: str
        :param tValues: Value(s) as tuple for inserting.
        :type tValues: tuple
        :return: ID of an inserted row  if the insert was successful.
            Otherwise, False.
        :rtype: int, str
        """
        sSQL = ("?, " * len(sColumns.split(", ")))[:-2]
        sqlString = "INSERT INTO " +\
                    sTable + " (" + sColumns + ") VALUES (" + sSQL + ") "
        oCursor = self.execute_query(sqlString, tValues)
        if not oCursor:
            return False

        self.oConnector.commit()
        return oCursor.lastrowid

    def delete_row(self, sTable, sColumns=None, tValues=None):
        """ Deletes row in the database table by value(s).

        :param sTable: A table as string in where need to delete row.
        :type sTable: str
        :param sColumns: Column(s) where the value(s) will be found.
            (by default, None).
        :type sColumns: str
        :param tValues: value(s) as tuple for search of rows.
            (by default, None).
        :type tValues: tuple
        :return: True if the deletion is successful, otherwise False.
        :rtype: bool
        """
        if sColumns is not None:
            sqlString = 'DELETE FROM ' + sTable + ' WHERE ' +\
                        get_columns(sColumns)
            oCursor = self.execute_query(sqlString, tValues)
        else:
            sqlString = "DELETE FROM " + sTable
            oCursor = self.execute_query(sqlString)

        if not oCursor:
            return False

        self.oConnector.commit()
        return True

    def update(self, sTable, sSetUpdate, sWhereUpdate, tValues):
        """ Updates value(s) in the record of the database table.

        :param sTable: A Table as string where update is need to do.
        :type sTable: str
        :param sSetUpdate: Column(s) where the value are writen.
        :type sSetUpdate: str
        :param sWhereUpdate: A column where values correspond to the required.
        :type sWhereUpdate: str
        :param tValues: value(s) as tuple for search corresponding rows.
        :type tValues: tuple
        :return: True if the insert was successful, otherwise False.
        :rtype: bool
        """
        sSetUpdate = sSetUpdate + "=?"
        sWhereUpdate = get_columns(sWhereUpdate)
        sqlString = "UPDATE " + sTable + " SET " + sSetUpdate + \
                    " WHERE " + sWhereUpdate + " "
        oCursor = self.execute_query(sqlString, tValues)
        if not oCursor:
            return False

        self.oConnector.commit()
        return True

    def select(self, sTable, sGet, sWhere=None, tValues=None, sFunc=None):
        """ Looks for row by value(s) in table column(s).

        :param sTable: Table name as string.
        :type sTable: str
        :param sGet: Name of the column of the table, which will be returned.
        :type sGet: str
        :param sWhere: Names of columns of the table, by which to search
            (by default, None).
        :type sWhere: str, None
        :param tValues: Value(s) as tuple for search
            (by default, None).
        :type tValues: tuple, None
        :param sFunc: Function name of sqlite, which need to apply
            (by default, None). Note: Now, you can use only two sqlite
            functions: Count and DISTINCT.
        :type sFunc: str, None
        :return: Cursor object within rows that was found, or False,
            if the row not found.
        :rtype: obj, bool
        """
        if sFunc == 'Count':
            sGet = 'Count(' + sGet + ')'
        elif sFunc == 'DISTINCT':
            sGet = sFunc + ' ' + sGet

        if sWhere is not None:
            sCol = get_columns(sWhere)
            sqlString = "SELECT " + sGet + " FROM " + sTable + " WHERE " + sCol
            oCursor = self.execute_query(sqlString, tValues)
        else:
            oCursor = self.execute_query("SELECT " + sGet + " FROM " + sTable)
        if not oCursor:
            return False

        return oCursor

    # Average API level
    def sql_get_id(self, sTable, sID, sColumns, tValues):
        """ Looks for ID of the row by value(s) of table column(s).

        :param sTable: Table name as string.
        :type sTable: str
        :param sID: Name of the column of the table by which to search.
        :type sID: str
        :param sColumns: Names of columns of the table by which to search.
        :type sColumns: str
        :param tValues: Value(s) as tuple for search.
        :type tValues: tuple
        :return: ID as Number in the row cell, or 0, if the row not found.
        :rtype: int, bool
        """
        sCol = get_columns(sColumns)
        sqlString = "SELECT " + sID + " FROM " + sTable + " WHERE " + sCol
        oCursor = self.execute_query(sqlString, tValues)
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
        :type sTable: str
        :return: Tuple of all rows of table.
        :rtype: tuple, bool
        """
        oCursor = self.execute_query("SELECT * FROM " + sTable)
        if not oCursor:
            return False

        return oCursor.fetchall()

    def sql_count(self, sTable):
        """ Counts number of records in database table.

        :param sTable: Table name as string where records should be count.
        :type sTable: str
        :return: Number of found records.
        :rtype: int, bool
        """
        # sTable, sGet, sWhere, tValues, sFunc=None
        oCursor = self.select(sTable, '*', None, None, 'Count')
        if not oCursor:
            return False

        row = oCursor.fetchall()
        return row[0][0]

    def sql_table_clean(self, lTable):
        """ Cleans up the table.

        :param lTable: Table names as list or tuple of string, or table name
            as string where cleaning is need to do.
        :type lTable: tuple
        :return: True, if execution is successful. Otherwise, False.
            Note: False is returned even if cleaning the last table in
            the tuple was not successful.
        :rtype: bool
            """
        if type(lTable) == str:
            lTable = [lTable]

        for sTable in lTable:
            bDel = self.delete_row(str(sTable))
            if not bDel:
                return False

        return True

    # High API level
    def q_get_id_author(self, sValue):
        """ Returns author id from Author table by author name.

        :param sValue: Values of Author name.
        :type sValue: str
        :return: A value from id_author column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.sql_get_id("Author", 'id_author', 'author_name', (sValue,))

    def q_get_id_book(self, sValue):
        """ Returns book id from Book table by book name.

        :param sValue: Values of Book name.
        :type sValue: str
        :return: A value from id_book column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.sql_get_id("Book", 'id_book', 'book_name', (sValue,))

    def q_get_id_country(self, sValue):
        """ Returns country id from Country table by country name.

        :param sValue: Value of country name.
        :type sValue: str
        :return: Number from id_country column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.sql_get_id("Country", 'id_country',
                               'en_name_country', (sValue,))

    # dspln is accepted abbreviation of word 'discipline'
    def q_get_id_dspln(self, sValue):
        """ Returns discipline id from Discipline table by discipline name.

        :param sValue: Value of discipline name.
        :type sValue: str
        :return: Number from id_discipline column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.sql_get_id('Discipline', 'id_discipline',
                               'discipline_name', (sValue,))

    def q_get_id_keyword(self, sValue):
        """ Returns keyword id from Keyword table by keyword name.

        :param sValue: Value of keyword name.
        :type sValue: str
        :return: Number from id_keyword column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.sql_get_id('Keywords', 'id_keyword', 'keyword', (sValue,))

    def q_get_id_lang(self, sValue):
        """ Returns lang id from Lang table by lang name.

        :param sValue: Value of lang name.
        :type sValue: str
        :return: Number from id_lang column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        sValue = sValue.strip().lower()
        return self.sql_get_id('Lang', 'id_lang', 'lang', (sValue,))

    def q_get_id_lang_by_name(self, sValue):
        """ Returns lang id from LangVariant table by lang name.

        :param sValue: Value of lang name.
        :type sValue: str
        :return: number from id_lang column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        sValue = sValue.strip().lower()
        return self.sql_get_id('LangVariant', 'id_lang', 'lang', (sValue,))

    def q_get_id_publ_type(self, sValue):
        """ Returns lang id from LangVariant table by lang name.

        :param sValue: Value of lang name.
        :type sValue: str
        :return: number from id_lang column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.sql_get_id('PublicationType', 'id_publ_type',
                               'name_type', (sValue,))

    def q_get_id_publication(self, tValues):
        """ Returns publication id from Publications table by publication name.

        :param tValues: A tuple with values in form: title, year, book.
            The book value can be int or str.
        :type tValues: tuple
        :return: number from id_publ column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        if type(tValues[2]) == str:
            iIDBook = self.q_get_id_book(tValues[2])
            tValues = (tValues[0], tValues[1], iIDBook,)

        return self.sql_get_id('Publication', 'id_publ',
                               'year, publ_name, id_book', tValues)

    def q_get_id_publisher(self, sValue):
        """ Returns publisher id from Publisher table by publisher name.

        :param sValue: Value of publisher name.
        :type sValue: str
        :return: number from id_publisher column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.sql_get_id('Publisher', 'id_publisher',
                               'publisher_name', (sValue,))

    def q_insert_authors(self, sValue):
        """ Inserts values into Author table.

        :param sValue: Value of lang name.
        :type sValue: str
        :return: number from id_lang column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.insert_row('Author', 'author_name', (sValue,))

    def q_insert_book(self, tValues):
        """ Inserts book name and print issn into Book table.

        :param tValues: Value of book name and ISSN. ISSN can be omitted.
        :type tValues: tuple
        :return: Number from id_book column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        if len(tValues) == 1:
            tValues = (tValues[0], '')
        return self.insert_row('Book', 'book_name, issn_print', tValues)

    def q_insert_book_dspln(self, tValues):
        """ Inserts values into BookDiscipline table.

        :param tValues: Values which need to insert. This parameter
            should contain 2 values: either 2 int, or 1 int and 1 str,
            or 2 str. The first from them should be values of book,
            and the second is discipline.
            Otherwise, an exception will be thrown.
        :type tValues: tuple
        :return: A value from id_book_discipline column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        if type(tValues[0]) == int and type(tValues[1]) == str:
            iIDDspln = self.q_get_id_dspln(tValues[1])
            if not iIDDspln:
                raise NameError('The discipline value %s return bool (%s)'
                                ' value', tValues[1], iIDDspln)
            tValues = (tValues[0], iIDDspln,)

        elif type(tValues[0]) == str:
            iIDBook = self.q_get_id_book(tValues[0])
            if not iIDBook:
                raise NameError('The book values %s, %s, %s return bool (%s)'
                                ' value', tValues[0], iIDBook)

            if type(tValues[1]) == str:
                iIDDspln = self.q_get_id_dspln(tValues[1])
                if not iIDDspln:
                    raise NameError('The discipline value %s return bool (%s)'
                                    ' value', tValues[1], iIDDspln)
                tValues = (iIDBook, iIDDspln,)
            else:
                tValues = (iIDBook, tValues[1],)
        sColumns = 'id_book, id_discipline'

        return self.insert_row('BookDiscipline', sColumns, tValues)

    def q_insert_book_editor(self, tValues):
        """ Inserts values into Editor table.

        :param tValues: Values which need to insert. This parameter should
            contain 2 values, otherwise will be call exception.
        :type tValues: tuple
        :return: A value from id_book_editor column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.insert_row('BookEditor', 'id_book, editor', tValues)

    def q_insert_book_lang(self, tValues):
        """ Inserts values into BookLang table.

        :param tValues: Values which need to insert. This parameter
            should contain 2 values: either 2 int, or 1 int and 1 str,
            or 2 str. The first from them should be values of book,
            and the second is Lang.
            Otherwise, an exception will be thrown.
        :type tValues: tuple
        :return: A value from id_book_lang column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        if type(tValues[0]) == int and type(tValues[1]) == str:
            iIDLang = self.q_get_id_lang_by_name(tValues[1])
            if not iIDLang:
                raise NameError('The discipline value %s return bool (%s)'
                                ' value', tValues[1], iIDLang)
            tValues = (tValues[0], iIDLang,)

        elif type(tValues[0]) == str:
            iIDBook = self.q_get_id_book(tValues[0])
            if not iIDBook:
                raise NameError('The book values %s, %s, %s return bool (%s)'
                                ' value', tValues[0], iIDBook)

            if type(tValues[1]) == str:
                iIDLang = self.q_get_id_lang_by_name(tValues[1])
                if not iIDLang:
                    raise NameError('The discipline value %s return bool (%s)'
                                    ' value', tValues[1], iIDLang)
                tValues = (iIDBook, iIDLang,)
            else:
                tValues = (iIDBook, tValues[1],)

        return self.insert_row('BookLang', 'id_book, id_lang', tValues)

    def q_insert_dspln(self, tValues):
        """ Inserts values into Discipline table.

        :param tValues: Values which need to insert.
        :type tValues: tuple
        :return: A value from id_discipline column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        if len(tValues) == 1:
            tValues = (tValues, '',)
        return self.insert_row('Discipline',
                               'discipline_name, discipline_url', tValues)

    def q_insert_keyword(self, sValue):
        """ Inserts values into Keyword table.

        :param sValue: Values which need to insert. This parameter should
            contain 1 values, otherwise will be call exception.
        :type sValue: str
        :return: A value from id_keyword column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.insert_row('Keywords', 'keyword', (sValue,))

    def q_insert_lang(self, tValues):
        """ Inserts values into Lang table.

        :param tValues: Values which need to insert. If parameter contain
            less than 8 values, missing values will be added.
        :type tValues: tuple
        :return: A value from id_lang column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        lValues = []
        if len(tValues) < 8:
            for Value in tValues:
                lValues.append(Value)
            while len(lValues) < 8:
                lValues.append('')
            tValues = tuple(lValues)
        sColumns = "lang, iso_639_1, iso_639_2, iso_639_3, " \
                   "iso_639_5, gost_7_75_lat, gost_7_75_rus, d_code "
        return self.insert_row('Lang', sColumns, tValues)

    def q_insert_lang_var(self, tValues):
        """ Inserts values into LangVariant table.

        :param tValues: Values which need to insert.This parameter should
            contain 2 values, otherwise will be call exception.
        :type tValues: tuple
        :return: A value from id_lang_var column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.insert_row('LangVariant', 'id_lang, lang', tValues)

    def q_insert_publ_author(self, tValues):
        """ Inserts values into PublicationAuthors table.

        :param tValues: Values which need to insert. This parameter should
            contain 2 values, otherwise will be call exception.
        :type tValues: tuple
        :return: A value from id_lang_var column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.insert_row('PublicationAuthor',
                               'id_publ, id_author', tValues)

    def q_insert_publ_keywords(self, tValues):
        """ Inserts values into PublicationKeywords table.

        :param tValues: Values which need to insert. This parameter should
            contain 2 values, otherwise will be call exception.
        :type tValues: tuple
        :return: A value from id_publ_keywords column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.insert_row('PublicationKeywords',
                               'id_publ, id_keyword', tValues)

    def q_insert_publ_lang(self, tValues):
        """ Inserts values into PublicationLang table.

        :param tValues: Values which need to insert. This parameter should
            contain 2 values, otherwise will be call exception.
        :type tValues: tuple
        :return: A value from id_publ_lang column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.insert_row('PublicationLang', 'id_publ, id_lang', tValues)

    def q_insert_publ_url(self, tValues):
        """ Inserts values into PublicationUrl table.

        :param tValues: Values which need to insert. This parameter should
            contain 2 values, otherwise will be call exception.
        :type tValues: tuple
        :return: A value from id_publ_url column in selected row.
            If query isn't done, then is False.
        :rtype: int, bool
        """
        return self.insert_row('PublicationUrl', 'id_publ, url', tValues)

    def q_update_book(self, sSetUpdate, tValues):
        """ Update values into Book table by id_book.

        :param sSetUpdate: Column(s) where the value are needed to write.
        :type sSetUpdate: str
        :param tValues: value(s) as tuple for search corresponding rows.
        :type tValues: tuple
        :return: True if the insert was successful, otherwise False.
        :rtype: bool
        """
        return self.update('Book', sSetUpdate, 'id_book', tValues)

    def q_update_publisher(self, sSetUpdate, tValues):
        """ Update values into Publisher table.

        :param sSetUpdate: Column(s) where the value are needed to write
        :type sSetUpdate: str
        :param tValues: value(s) as tuple for search corresponding rows.
        :type tValues: tuple
        :return: True if the insert was successful, otherwise False.
        :rtype: bool
        """
        return self.update('Publisher', sSetUpdate, 'id_publisher', tValues)
