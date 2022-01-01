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

oConstructor = sqlite3.connect('./db/test_sql.db')
oCursor = oConstructor.cursor()

sTable = 'Journal'
sColumns = 'journal_name'

lColumn = sColumns.split(", ")
sSQL = ""
for name in lColumn:
    sSQL = sSQL + "?,"
sSQL = sSQL[:-1]

sValues = 'flds kdgnspk sdkv'
lValues = (sValues,)
sqlString = "INSERT INTO " + sTable + " (" + sColumns + ") VALUES (" + sSQL + ")"
try:
    oCursor.execute(sqlString, lValues)
except DatabaseError as e:
    print("Ошибка записи в базу данных" + "\n" + str(e))
else:
    oConstructor.commit()

oConstructor.close()
