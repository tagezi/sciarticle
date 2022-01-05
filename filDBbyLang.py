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

from sqlmain import *
import var


def fill_lang_tab():
    db_file = var.db_file
    dump_file = var.lang_list
    oConnector = Sqlmain(db_file)

    with open(dump_file, "r") as oFile:
        for oLang in oFile:
            sLang = oLang.replace("\n", "").lower()
            lLang = sLang.split(",")

            """ Converts values to variables. Sometimes probes remain 
            at the beginning and at the end of the line, we delete them."""
            sEnLang = lLang[0].strip()
            sISO_1 = lLang[1].strip()
            sISO_2 = lLang[2].strip()
            sISO_3 = lLang[3].strip()
            sGOST_1 = lLang[4].strip()
            sGOST_2 = lLang[5].strip()
            sCode = lLang[6].strip()

            iLang = oConnector.get_id_lang_by_639_2(sISO_2)
            if iLang == 0:
                sColumns = "en_name, iso_639_1, iso_639_2, iso_639_3, gost_7_75_lat, gost_7_75_rus, d_code"
                lValues = (sEnLang, sISO_1, sISO_2, sISO_3, sGOST_1, sGOST_2, sCode,)
                oConnector.sql_insert('Lang', sColumns, lValues)
                iLang = oConnector.sql_search_id('Lang', 'id_lang', 'en_name', (sEnLang,))
                oConnector.sql_insert('LangVariant', 'id_lang, lang', (iLang, sEnLang))

    oFile.close()

    dump_file = var.lang_variant_list
    with open(dump_file, "r") as oFile:
        for oLang in oFile:
            sLang = oLang.replace("\n", "").lower()
            lLang = sLang.split(",")

            iLang = oConnector.get_id_lang_by_name(lLang[0])
            for Lang in lLang:
                Lang = Lang.strip()
                if oConnector.get_id_lang_by_name(Lang) == 0 and Lang != '':
                    oConnector.sql_insert('LangVariant', 'id_lang, lang', (iLang, Lang))

    oFile.close()
    del oConnector


if __name__ == '__main__':
    fill_lang_tab()
