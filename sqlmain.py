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

import sqlite3
from sqlite3 import DatabaseError


def get_columns(sColumns):
    """ Method of parsing a string, accepts a list of table columns separated
    by commas and returns this list with =? AND as separator

    :param sColumns: a string with a list of table columns separated by commas
    :return: the string with a list of table columns separated by '=? AND'
    """
    return sColumns.replace(", ", "=? AND") + "=?"


class Sqlmain():
    """
    Provides a simple interface for working with database with others scripts.

      **methods**:
        * __init__: method initializes a cursor of sqlite database
        * sql_search_id: method looks for a id of the row by value(s) of table
                         column(s)
        * sql_search: method looks for a row by value(s) of table column(s)
        * sql_count: method counts number of records in database table
        * sql_insert: method inserts a record in the database table
        * sql_update: method update value(s) in record of the database table
        * sql_table_clean: method cleans up the table
        * __del__: method closes the cursor of sqlite database
    """

    def __init__(self, sFileDB):
        """ Initializes connect with database

        :param sFileDB: path to database as string
        """
        self.oConnect = sqlite3.connect(sFileDB)

    def query_execute(self, sqlString, cValues, sFunc):
        oCursor = self.oConnect.cursor()
        try:
            oCursor.execute(sqlString, cValues)
        except DatabaseError as e:
            print("An error has occurred: '" + str(e) + "'.\nMethod: " + sFunc)
            return False

        return oCursor

    def sql_search_id(self, sTable, sID, sColumns, cValues):
        """ Looks for ID of the row by value(s) of table column(s)

        :param sTable: table name as string
        :param sID: a name of the column of the table by which to search
        :param sColumns: names of columns of the table by which to search
        :param cValues: value(s) as tuple for search
        :return: a number of ID in the row cell or 0, if the row not found
        """
        sCol = get_columns(sColumns)
        sqlString = "SELECT " + sID + " FROM " + sTable + " WHERE " + sCol + ""

        oCursor = self.query_execute(sqlString, cValues, 'sql_search_id')
        if not oCursor:
            return False
        else:
            row = oCursor.fetchall()

            if not row:
                return 0
            else:
                return row[0][0]

    def sql_search(self, sTable, sColumns, cValues):
        """ Looks for a row by value(s) of table column(s)

        :param sTable: table name as string
        :param sColumns: names of columns of the table by which to search
        :param cValues: value(s) as tuple for search
        :return: the first row or None, if the row not found
        """
        sCol = get_columns(sColumns)
        sqlString = "SELECT " + sColumns + " FROM " + sTable + " WHERE " + sCol
        oCursor = self.query_execute(sqlString, cValues, 'sql_search')
        if not oCursor:
            return False
        else:
            rows = oCursor.fetchall()

        for row in rows:
            return row
        else:
            return None

    def sql_get_all(self, sTable):
        """ Gets all records in database table

        :param sTable: table name as string where records should be received
        :return: tuple of rows
        """
        oCursor = self.oConnect.cursor()

        sqlString = "SELECT * FROM " + sTable + ""
        try:
            oCursor.execute(sqlString)
        except DatabaseError as e:
            print("An error has occurred: " + str(e) + "\nCan't get rows.")
            return None

        return oCursor.fetchall()

    def sql_count(self, sTable):
        """ Counts number of records in database table

        :param sTable: table name as string where records should be count
        :return: number of records
        """
        oCursor = self.oConnect.cursor()

        sqlString = "SELECT Count(*) FROM " + sTable + ""
        try:
            oCursor.execute(sqlString)
        except DatabaseError as e:
            print("An error has occurred: " + str(e) + "\nCan't count rows.")
            return None

        row = oCursor.fetchall()

        return row[0][0]

    def sql_insert(self, sTable, sColumns, cValues):
        """ Inserts a record in the database table

        :param sTable: table name as string
        :param sColumns: names of columns of the table by which to search
        :param cValues: value(s) as tuple for search
        :return: True if the insert was successful, otherwise False
        """
        sSQL = ("?, " * len(sColumns.split(", ")))[:-2]
        sqlString = "INSERT INTO "\
                    + sTable + " (" + sColumns + ") VALUES (" + sSQL + ") "
        oCursor = self.query_execute(sqlString, cValues, 'sql_insert')
        if not oCursor:
            return False

        self.oConnect.commit()
        return True

    def sql_update(self, sTable, sSetUpdate, sWhereUpdate, cValues):
        """ Updates value(s) in the record of the database table

        :param sTable: A Table  as string in DB where update is need to do
        :param sSetUpdate: Column(s) where the value are writen
        :param sWhereUpdate: A row where values correspond to the required
        :param cValues: value(s) as tuple for search
        :return: True if the insert was successful, otherwise False
        """
        oCursor = self.oConnect.cursor()
        sSetUpdate = sSetUpdate + "=?"
        sWhereUpdate = get_columns(sWhereUpdate)
        sqlString = "UPDATE " + sTable + " SET " + sSetUpdate + \
                    " WHERE " + sWhereUpdate + " "
        oCursor = self.query_execute(sqlString, cValues, 'sql_update')
        if not oCursor:
            return False

        self.oConnect.commit()
        return True

    def sql_table_clean(self, sTable):
        """ Cleans up the table

        :param sTable: A Table as string in DB where cleaning is need to do
        :return: True if cleaning was successful, otherwise False
        """
        oCursor = self.oConnect.cursor()

        sqlString = "DELETE FROM " + sTable
        try:
            oCursor.execute(sqlString)
        except DatabaseError as e:
            print("An error has occurred: " + str(e) + "\n. ")
            return False

        self.oConnect.commit()
        return True

    def get_id_lang_by_name(self, sLang):
        """ Return ID of Lang from the table LangVariant by Lang name

        :param sLang: a string of lang name
        :return: number from id_lang column in selected row
        """
        sLang = sLang.strip().lower()
        return self.sql_search_id('LangVariant', 'id_lang', 'lang', (sLang,))

    def get_id_lang_by_639_2(self, sCode):
        """ Return ID of Lang from the table Lang using a value of ISO 639-2

        :param sCode: a string of ISO 639-2 code in low register
        :return: number from id_lang column in selected row
        """
        return self.sql_search_id('Lang', 'id_lang', 'iso_639_2', (sCode,))

    def __del__(self):
        """ Closes connection with the database"""
        self.oConnect.close()
