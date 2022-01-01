#     This code is a part of program Science Jpurnal
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

import sqlite3
from sqlite3 import DatabaseError


# Provides a simple interface for working with a database with others scripts.
class Sqlmain():
    def __init__(self, sFileDB):
        self.oConnect = sqlite3.connect(sFileDB)

    def get_columns(self, sColumns):
        lColumn = sColumns.split(", ")
        sCol = ""
        for name in lColumn:
            sCol = sCol + str(name) + "=? AND "
        sCol = sCol[:-4]

        return sCol

    def sql_search_id(self, sTable, sID, sColumns, cValues):
        oCursor = self.oConnect.cursor()

        sCol = self.get_columns(sColumns)
        sqlString = "SELECT " + sID + " FROM " + sTable + " WHERE " + sCol + ""
        try:
            oCursor.execute(sqlString, cValues)
        except DatabaseError as e:
            print("An error has occurred: " + str(e) + "\nCan't find the id.")
        else:
            row = oCursor.fetchall()

            if not row:
                return 0
            else:
                return row[0][0]

    def sql_search(self, sTable, sColumns, cValues):
        oCursor = self.oConnect.cursor()

        sCol = self.get_columns(sColumns)
        sqlString = "SELECT " + sColumns + " FROM " + sTable + " WHERE " + sCol + ""
        try:
            oCursor.execute(sqlString, cValues)
        except DatabaseError as e:
            print("An error has occurred: " + str(e) + "\nCan't find the row.")
        else:
            rows = oCursor.fetchall()

            print(rows)
            for row in rows:
                print(row)
                return row
            else:
                return None

    def sql_count(self, sTable):
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
        oCursor = self.oConnect.cursor()

        lColumn = sColumns.split(", ")
        sSQL = ""
        for name in lColumn:
            sSQL = sSQL + "?,"
        sSQL = sSQL[:-1]

        sqlString = "INSERT INTO " + sTable + " (" + sColumns + ") VALUES (" + sSQL + ") "
        try:
            oCursor.execute(sqlString, cValues)
        except DatabaseError as e:
            print("An error has occurred: " + str(e) + "\nCan't insert the row.")
            return False

        self.oConnect.commit()
        return True

    def sql_update(self, sTable, sSetUpdate, sWhereUpdate, cValues):
        """

        :param oConect: An object for connecting with DB SQLite
        :param sTable:  A Table in DB where update is need to do
        :param sSetUpdate: A Column where the value will be writen
        :param sWhereUpdate: A row ID where the value will be writen
        :param cValues: A value
        :return:
        """
        oCursor = self.oConnect.cursor()
        sSetUpdate = sSetUpdate + "=?"
        sWhereUpdate = self.get_columns(sWhereUpdate)
        sqlString = "UPDATE " + sTable + " SET " + sSetUpdate + " WHERE " + sWhereUpdate + " "

        try:
            oCursor.execute(sqlString, cValues)
        except DatabaseError as e:
            print("An error has occurred: " + str(e) + "\nCan't update the row.")
            return False

        self.oConnect.commit()
        return True

    def sql_table_clean(self, sTable):
        oCursor = self.oConnect.cursor()

        sqlString = "DELETE FROM " + sTable + ""
        try:
            oCursor.execute(sqlString)
        except DatabaseError as e:
            print("An error has occurred: " + str(e) + "\nThe table is not cleared. ")
            return False

        return True

    def __del__(self):
        self.oConnect.close()
