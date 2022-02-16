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
import os

from config.config import DB_FILE, pach_path
from sciarticle.get_link import collect_links
from sciarticle.lib.journalsmain import JournalValue
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import get_file_patch

oConnector = SQLmain(os.path.abspath(get_file_patch(pach_path(), DB_FILE)))


def journal(sURLPage):
    oJournalValue = JournalValue(sURLPage)

    if not oJournalValue.is_journal_exist():
        tValues = oJournalValue.get_journal_values()
        iIDBook = oConnector.q_insert_book(tValues)

        if oJournalValue.is_journal_code_exist():
            tValues = oJournalValue.get_journal_code(iIDBook)
            oConnector.q_insert_book_code(tValues)

        if oJournalValue.tDiscipline:
            tDiscipline = oJournalValue.tDiscipline
            if type(tDiscipline) != str:
                for sDiscipline in tDiscipline:
                    if sDiscipline:
                        oConnector.q_insert_book_dspln((iIDBook,
                                                        sDiscipline.lower(),))
            else:
                oConnector.q_insert_book_dspln((iIDBook, tDiscipline.lower(),))

        if oJournalValue.lEditor:
            lEditor = oJournalValue.lEditor
            if type(lEditor) != str:
                for sEditor in oJournalValue.lEditor:
                    if sEditor != 'MD' or sEditor != 'PhD' or \
                            sEditor != 'FAAFP' or sEditor != 'MPH':
                        oConnector.q_insert_book_editor((iIDBook, sEditor,))
            else:
                oConnector.q_insert_book_editor((iIDBook, lEditor,))

        if oJournalValue.sLang:
            tLang = oJournalValue.sLang
            if type(tLang) != str:
                for sLang in tLang:
                    oConnector.q_insert_book_lang((iIDBook, sLang.lower(),))
            else:
                oConnector.q_insert_book_lang((iIDBook, tLang.lower(),))


if __name__ == '__main__':
    lListJournals = ['Category:English-language_journals']

    # journal('https://en.wikipedia.org/wiki/Archaeologia_Cambrensis')
    lURL = collect_links(lListJournals)
    for sURL in lURL:
        print(sURL)
        if not oConnector.sql_get_id('Book', 'id_book', 'wiki_url', (sURL,)):
            journal(sURL)
