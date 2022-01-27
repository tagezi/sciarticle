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

from config.config import DB_DIR, DB_FILE
from perfect_soup import PerfectSoup
from sqlmain import SQLmain
from strmain import *


class JournalValue:

    def __init__(self, sPageURL):
        self.oConnector = SQLmain(
            os.path.abspath(get_file_patch(DB_DIR, DB_FILE)))
        self.oPS = PerfectSoup(sPageURL)

        dNames = self.oPS.get_name_from_bold()
        # Name of journal
        self.sFullName = dNames['FullName']
        # Any former name or names of the journal
        self.sFormerName = self.former_names('Former name(s)')
        # The ISO 4 abbreviation for journal.
        self.sISO4 = self.journal_value('ISO 4')
        # Topic of the journal.
        self.sDiscipline = self.dspl_values('Discipline')
        self.sPeerReviewe = self.journal_value('Peer-reviewed')
        # It can be more than one
        self.sLang = self.values_without_url('Language')
        # It can be more than one
        self.sEditor = self.values_without_url('Edited\xa0by')
        # self.sPublisher = self.get_publisher('Publisher')
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
        self.LCCN = self.journal_value('LCCN')
        # The Online Computer Library Center number.
        self.OCLC = self.journal_value('OCLC\xa0no.')
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
        sNo = self.oPS.dBlock.get(sValue)
        if sNo:
            sISSN = clean_parens(sNo[0])
            if sValue == 'ISSN':
                sNo = clean_spaces(sISSN).split(' ')[0]
            else:
                if sISSN:
                    sNo = clean_spaces(sISSN).split(' ')[1]

        return sNo

    def former_names(self, Values):
        return str_to_list(self.oPS.dBlock.get('Former name(s)'))

    def values_without_url(self, sValues):
        lData = self.oPS.dBlock.get(sValues)
        if lData and type(lData) != str and len(lData) > 1:
            for sData in lData:
                if sData.find('http') == -1:
                    sValues = sData
        else:
            sValues = lData

        return sValues

    def year_value(self, sValue):
        return str_to_year(self.oPS.dBlock.get(sValue))[0]

    def dspl_values(self, sValues):
        return self.oPS.dBlock.get(sValues)

    def get_publisher(self, sValue):
        return self.oPS.dBlock.get(sValue)


if __name__ == '__main__':
    sURL = 'https://en.wikipedia.org/wiki/AACN_Advanced_Critical_Care'
    dJournal = JournalValue(sURL)