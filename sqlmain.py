from sqlite3 import DatabaseError


def get_columns(sColumns):
    lColumn = sColumns.split(", ")
    sCol = ""
    for name in lColumn:
        sCol = sCol + str(name) + "=? AND "
    sCol = sCol[:-4]

    return sCol


def sql_search_id(oConstructor, sTable, sID, sColumns, cValues):
    oCursor = oConstructor.cursor()

    sCol = get_columns(sColumns)
    sqlString = "SELECT " + sID + " FROM " + sTable + " WHERE " + sCol + ""
    try:
        oCursor.execute(sqlString, cValues)
    except DatabaseError as e:
        print("Ошибка чтения из базы данных" + "\n" + str(e))
    else:
        row = oCursor.fetchall()

        if not row:
            return 0
        else:
            return row[0][0]


def sql_search(oConstructor, sTable, sColumns, cValues):
    oCursor = oConstructor.cursor()

    sCol = get_columns(sColumns)
    sqlString = "SELECT " + sColumns + " FROM " + sTable + " WHERE " + sCol + ""
    try:
        oCursor.execute(sqlString, cValues)
    except DatabaseError as e:
        print("Ошибка чтения из базы данных" + "\n" + str(e))
    else:
        rows = oCursor.fetchall()

        print(rows)
        for row in rows:
            print(row)
            return row
        else:
            return None


def sql_count(oConstructor, sTable):
    oCursor = oConstructor.cursor()

    sqlString = "SELECT Count(*) FROM " + sTable + ""
    try:
        oCursor.execute(sqlString)
        row = oCursor.fetchall()
        return row[0][0]
    except DatabaseError as e:
        print("Ошибка чтения из базы данных" + "\n" + str(e))
        return None


def sql_insert(oConstructor, sTable, sColumns, cValues):
    oCursor = oConstructor.cursor()

    lColumn = sColumns.split(", ")
    sSQL = ""
    for name in lColumn:
        sSQL = sSQL + "?,"
    sSQL = sSQL[:-1]

    sqlString = "INSERT INTO " + sTable + " (" + sColumns + ") VALUES (" + sSQL + ") "
    try:
        oCursor.execute(sqlString, cValues)
    except DatabaseError as e:
        print("Ошибка записи в базу данных" + "\n" + str(e))
    else:
        oConstructor.commit()


def sql_update(oConstructor, sTable, sSetUpdate, sWhereUpdate, cValues):

    oCursor = oConstructor.cursor()
    sSetUpdate = sSetUpdate + "=?"
    sWhereUpdate = get_columns(sWhereUpdate)
    sqlString = "UPDATE " + sTable + " SET " + sSetUpdate + " WHERE " + sWhereUpdate + " "

    try:
        oCursor.execute(sqlString, cValues)
    except DatabaseError as e:
        print("Ошибка записи в базу данных" + "\n" + str(e))
    else:
        oConstructor.commit()
