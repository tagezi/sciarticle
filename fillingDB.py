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
from sqlmain import *

# Заполняет таблицу Lang в базе данных
oConstructor = sqlite3.connect('/home/lera/project/scriping/test_sql.db')

with open('file.backup/lang.csv', "r") as oFile:
    iNumber = 1
    for oCountry in oFile:
        sLang = oCountry.replace("\n", "")
        lLang = sLang.split(",")

        sEnLang = lLang[0]
        sRuLang = lLang[1]
        sISO_1 = lLang[2]
        sISO_2 = lLang[3]
        sISO_3 = lLang[4]
        sGOST_1 = lLang[5]
        sGOST_2 = lLang[6]
        sCode = lLang[7]

        sColumns = "en_name, ru_name, iso_639_1, iso_639_2, iso_639_3, gost_7_75_lat, gost_7_75_rus, d_code"
        lValues = [(sEnLang, sRuLang, sISO_1, sISO_2, sISO_3, sGOST_1, sGOST_2, sCode)]
        sql_insert(oConstructor, 'Lang', sColumns, lValues)
        print("Занесли запись " + str(iNumber) + " : " + str(sEnLang))
        iNumber = iNumber + 1

oFile.close()
oConstructor.close()
