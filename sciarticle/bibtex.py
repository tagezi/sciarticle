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

    dBibDB = oBibDatabase.entries_dict
    lKeysBibDB = list(dBibDB)

    i = 0
    iCountKeys = len(lKeysBibDB)
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

            if oArticle.lAuthors is not None:
                for sAuthor in oArticle.lAuthors:
                    iIDAuthor = oConnector.q_get_id_author(sAuthor)
                    if not iIDAuthor:
                        iIDAuthor = oConnector.q_insert_authors(sAuthor)
                    oConnector.q_insert_publ_author((iIDPubl, iIDAuthor,))

            if oArticle.lKeywords is not None:
                for sKeyword in oArticle.lKeywords:
                    iIDKeyword = oConnector.q_get_id_keyword(sKeyword)
                    if not iIDKeyword:
                        iIDKeyword = oConnector.q_insert_keyword(sKeyword)
                    oConnector.q_insert_publ_keywords((iIDPubl, iIDKeyword,))

            if oArticle.lLang is not None:
                for sLang in oArticle.lLang:
                    iIDLang = oConnector.q_get_id_lang_by_name(sLang)
                    if iIDLang:
                        oConnector.q_insert_publ_lang((iIDPubl, iIDLang,))

            for sURL in oArticle.lURL:
                oConnector.q_insert_publ_url((iIDPubl, sURL,))


oConnector = SQLmain(get_file_patch(DB_DIR, DB_FILE))

if __name__ == '__main__':
    bibtex_parser(get_file_patch(BIBTEX_DIR, BIBTEX_FILE))
