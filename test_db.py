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
