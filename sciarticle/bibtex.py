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

from config.config import BIBTEX_DIR, BIBTEX_FILE, DB_DIR, DB_FILE
from sciarticle.lib.bibvalue import BibtexValue, bibtex_load
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import get_file_patch


def bibtex_parser(fBibFile=None):
    with open(fBibFile) as fBibtexFile:
        oBibDatabase = bibtex_load(fBibtexFile)

    # Gets all records and counts their number.
    dBibDB = oBibDatabase.entries_dict
    lKeysBibDB = list(dBibDB)
    iCountKeys = len(lKeysBibDB)

    i = 0
    while i < iCountKeys:
        dArticle = dBibDB.get(lKeysBibDB[i])
        i += 1

        oArticle = BibtexValue(dArticle)
        if not oArticle.is_there_book():
            tValues = oArticle.get_publication()
            iIDPubl = oConnector.insert_row('Publications',
                                            'id_publ_type, publ_name, '
                                            'abstract, doi, id_book, year, '
                                            'volume, number, pages', tValues)

            if oArticle.tAuthors:
                for sAuthor in oArticle.tAuthors:
                    iIDAuthor = oConnector.q_get_id_author(sAuthor)
                    oConnector.q_insert_publ_author((iIDPubl, iIDAuthor,))

            if oArticle.tKeywords:
                for sKeyword in oArticle.tKeywords:
                    iIDKeyword = oConnector.q_get_id_keyword(sKeyword)
                    if not iIDKeyword:
                        iIDKeyword = oConnector.q_insert_keyword(sKeyword)
                    oConnector.q_insert_publ_keywords((iIDPubl, iIDKeyword,))

            if oArticle.tLang:
                for sLang in oArticle.tLang:
                    iIDLang = oConnector.q_get_id_lang_by_name(sLang)
                    if iIDLang:
                        oConnector.q_insert_publ_lang((iIDPubl, iIDLang,))

            oConnector.q_insert_publ_url((iIDPubl, oArticle.lURL,))


oConnector = SQLmain(get_file_patch(DB_DIR, DB_FILE))

if __name__ == '__main__':
    oConnector.sql_table_clean(('PublicationAuthor',
                                'PublicationKeywords', 'Keywords',
                                'PublicationLang', 'PublicationUrl',
                                'Publications', 'Author'))
    bibtex_parser(get_file_patch(BIBTEX_DIR, BIBTEX_FILE))
