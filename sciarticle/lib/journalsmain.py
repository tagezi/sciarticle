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
import re

from config.config import DB_FILE, pach_path
from sciarticle.lib.perfect_soup import PerfectSoup
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import *
from sciarticle.publisher import publisher

oConnector = SQLmain(os.path.abspath(get_file_patch(pach_path(), DB_FILE)))


class JournalValue:

    def __init__(self, sPageURL):
        self.oPS = PerfectSoup(sPageURL)

        dNames = self.oPS.get_name_from_bold()
        # Name of journal
        self.sFullName = dNames['FullName']
        # Any former name or names of the journal
        self.sFormerName = self.former_names('Former name(s)')
        # The ISO 4 abbreviation for journal.
        self.sISO4 = self.journal_value('ISO 4')
        # Topic of the journal.
        self.tDiscipline = self.dspl_values('Discipline')
        self.sPeerReviewe = self.journal_value('Peer-reviewed')
        # It can be more than one
        self.sLang = self.lang_value('Language')
        # It can be more than one
        self.lEditor = self.editor_value('Edited\xa0by')
        if not self.lEditor:
            self.lEditor = self.editor_value('Edited by')
        self.sPublisher = self.get_publisher('Publisher')
        # Year of foundation
        self.iYear = self.year_value('History')
        self.sOpenAccess = self.journal_value('Open access')
        # # License on paper
        self.sLicense = self.values_without_url('License')
        # The Bluebook abbreviation for law journal.
        self.sBluebook = self.journal_value('Bluebook')
        # The MathSciNet abbreviation.
        self.sMathSciNet = self.journal_value('MathSciNet')
        # The NLM abbreviation.
        self.sNML = self.journal_value('NLM')
        # International Standard Serial Number.
        self.sISSN = self.sissn_value('ISSN')
        # ISSN for online version.
        self.sEISSN = self.sissn_value('EISSN')
        # Six character, alphanumeric bibliographic code.
        self.sCODEN = self.journal_value('CODEN')
        # Journal STORage.
        self.JSTOR = self.journal_value('JSTOR')
        # The Library of Congress Control Number.
        self.sLCCN = self.journal_value('LCCN')
        # The Online Computer Library Center number.
        self.sOCLC = self.journal_value('OCLC\xa0no.')
        if not self.sOCLC:
            self.sOCLC = self.journal_value('OCLC no.')
        # Amazon Standard Identification Number
        self.sASIN = self.journal_value('asin')
        # Book Item and Component Identifier
        self.sBICI = self.journal_value('bici')
        # English Short Title Catalogue
        self.sESTC = self.journal_value('estc')
        # Electronic Textbook Track Number
        self.sETTN = self.journal_value('ettn')
        # International Standard Text Code
        self.sISTC = self.journal_value('istc')
        # Serial Item and Contribution Identifier
        self.sSICI = self.journal_value('sici')
        # Journal homepage
        self.sURL = self.get_url('Journal homepage')
        # Online access of journal
        self.sOnlineAccessURL = self.get_url('Online access')
        # Online archive of papers
        self.sOnlineArchiveURL = self.get_url('Online archive')
        self.sFrequency = self.journal_value('Frequency')
        self.sWikiURL = sPageURL

    def journal_value(self, sValue):
        sNo = self.oPS.dBlock.get(sValue)
        if sNo and type(sNo) != str:
            return sNo[0]

        return sNo

    def get_url(self, sValue):
        return self.oPS.dBlock.get(sValue)

    def sissn_value(self, sValue):
        sNo = self.oPS.dBlock.get('ISSN')
        if sNo:
            if type(sNo) != str:
                sNo = sNo[0]

            sISSN = clean_parens(sNo)
            if sValue == 'ISSN':
                sNo = clean_spaces(sISSN).split(' ')[0]
            else:
                if len(clean_spaces(sISSN).split(' ')) == 2:
                    sNo = clean_spaces(sISSN).split(' ')[1]

        return sNo

    def former_names(self, Values):
        sFormerNme = self.oPS.dBlock.get(Values)
        if sFormerNme:
            if type(sFormerNme) == str:
                return str_to_list(sFormerNme)

            return str_to_list(sFormerNme[0])

        return sFormerNme

    def editor_value(self, sValue):
        lEditor = self.oPS.dBlock.get(sValue)
        if type(lEditor) == tuple:
            lEditor = lEditor[0]
        if lEditor:
            lEditor = clean_list_values(get_values(lEditor))

        return lEditor

    def values_without_url(self, sValues):
        lData = self.oPS.dBlock.get(sValues)
        if lData and type(lData) != str and len(lData) > 1:
            for sData in lData:
                if sData.find('http') == -1 and sData.find('wiki') == -1:
                    sValues = sData
        elif lData:
            sValues = clean_list_values(get_values(lData))
        else:
            sValues = lData

        return sValues

    def lang_value(self, sValue):
        lLang = self.oPS.dBlock.get(sValue)
        if type(lLang) == tuple:
            lLang = lLang[0]
        if lLang:
            lLang = get_values(lLang)

        return lLang

    def year_value(self, sValue):
        iYear = self.oPS.dBlock.get(sValue)
        if type(iYear) == tuple:
            iYear = iYear[0]
        if iYear:
            iYear = re.search(r'\d{4}', iYear)
        if iYear:
            iYear = iYear[0]

        return iYear

    def dspl_values(self, sValues):
        tDisciplines = self.oPS.dBlock.get(sValues)
        if tDisciplines and type(tDisciplines) == tuple:
            tDisciplines = tDisciplines[0]
        if tDisciplines:
            return clean_list_values(str_to_list(tDisciplines))

        return tDisciplines

    def get_publisher(self, sValue):
        tPublisher = self.oPS.dBlock.get(sValue)
        if not tPublisher or type(tPublisher) == str:
            return tPublisher

        if oConnector.q_get_id_publisher(tPublisher[0]):
            return tPublisher[0]

        sPublisher = tPublisher[2]
        sPublisherName = clean_parens(sPublisher.get_text())
        sListAPub = sPublisher.findAll("a")
        # Sometimes a link points to external page, but here is internal needed
        sAPub = sListAPub
        if sListAPub:
            for sAPub in sListAPub:
                if sAPub.get_text().find('http') != -1:
                    break
        # Sometimes Publisher name is shorter or longer then it is :)
        # And sometimes it's not there at all.
        if sAPub and sPublisherName.find(sAPub.get_text()) != -1:
            # Publisher is not Country name. Yes, in wikipedia it can be.
            if not oConnector.q_get_id_country(sAPub.get_text()):
                sPublisherName = clean_parens(sAPub.get_text())
                # If a link is in <a> tag, and it isn't redlink.
                if str(sAPub).find("href") != -1 \
                        and str(sAPub).find("http") == -1 \
                        and str(sAPub).find("redlink") == -1:
                    sPubURL = get_wiki_url(str(sAPub.attrs['href']))

                    return publisher(sPubURL)

        # If we cannot find a link to a Wikipedia page with a description of
        # the publisher, then we return what we have
        return sPublisherName

    def is_journal_exist(self):
        return oConnector.q_get_id_book(self.sFullName, self.sISSN)

    def get_journal_values(self):
        iPublisher = oConnector.q_get_id_publisher(self.sPublisher)
        if self.sPublisher and not iPublisher:
            iPublisher = oConnector.q_insert_publisher(self.sPublisher)

        tValues = (self.sFullName, self.iYear, iPublisher, self.sFrequency,
                   self.sISO4, self.sISSN, self.sEISSN, '', self.sURL,
                   self.sOnlineAccessURL, self.sOnlineArchiveURL,
                   self.sWikiURL)

        return tValues

    def is_journal_code_exist(self):
        if self.sBluebook or self.sMathSciNet or self.sNML or self.sCODEN or \
                self.JSTOR or self.sLCCN or self.sOCLC or self.sASIN or \
                self.sBICI or self.sESTC or self.sETTN or self.sISTC or \
                self.sSICI:
            return True

        return False

    def get_journal_code(self, iIDJournal):
        return (iIDJournal, self.sBluebook, self.sMathSciNet, self.sNML,
                self.sCODEN, self.JSTOR, self.sLCCN, self.sOCLC, self.sASIN,
                self.sBICI, self.sESTC, self.sETTN, self.sISTC, self.sSICI,)


if __name__ == '__main__':
    sURL = 'https://en.wikipedia.org/wiki/AACN_Advanced_Critical_Care'
    dJournal = JournalValue(sURL)
