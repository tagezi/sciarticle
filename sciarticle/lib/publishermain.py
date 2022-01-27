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
import csv
import os

from config.config import DB_DIR, DB_FILE
from sciarticle.lib.perfect_soup import PerfectSoup
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import *
from sciarticle.get_link import collect_links


class PublisherValue:

    def __init__(self, sPageURL):
        self.oConnector = SQLmain(
            os.path.abspath(get_file_patch(DB_DIR, DB_FILE)))
        self.oPS = PerfectSoup(sPageURL)

        self.sFullName = self.get_name('FullName')
        self.sShortName = self.get_name('ShortName')
        self.ParentCompany = self.get_company('Parent company')
        self.Status = self.get_activate()
        self.Predecessor = self.get_value('Predecessor')
        self.sFounded = self.get_year()
        self.sFounder = self.get_founder('Founder')
        self.CountryOfOrigin = self.get_location('Country of origin')
        self.Headquarters = self.get_location('Headquarters location')
        self.PublicationTypes = self.get_publication_type('Publication types')
        self.Owner = self.get_owner('Owner(s)')
        self.OfficialWebsite = self.get_url()
        self.sWebsite = self.get_url()
        self.OtherName = self.get_value('Other Name')
        self.FormerName = self.get_value('Former Name')
        self.Type = self.get_type('Type')
        self.ParentInstitution = self.get_value('Parent Institution')
        self.AcademicAffiliation = self.get_value('Academic Affiliation')
        self.Location = self.get_value('Location')
        self.Country = self.get_location('country')
        self.Language = self.get_value('Language')
        self.WikiURL = sPageURL

    def get_value(self, sValue):
        return self.oPS.dBlock.get(sValue)

    def get_name(self, sValue):
        sNames = self.oPS.get_name_from_bold()
        sName = sNames.get(sValue)
        if sValue == 'FullName' and not sName:
            sName = self.oPS.get_title_h1()

        return sName

    def get_owner(self, sValue):
        sOwner = self.get_value('Owner(s)')
        if sOwner and type(sOwner) != str:
            return sOwner[0]

        return sOwner

    def get_activate(self):
        sActiv = self.get_value('Status')
        if not sActiv:
            sActiv = self.get_value('Active')
        if sActiv:
            if type(sActiv) != str:
                sActiv = sActiv[0]
            if type(sActiv) == str:
                sActiv = clean_spaces(sActiv)
            if sActiv != 'Active':
                sActiv = 'Inactive'

        return sActiv

    def get_url(self):
        lURL = self.oPS.dBlock.get('Official website')
        if not lURL:
            lURL = self.oPS.dBlock.get('Website')
        if lURL:
            if type(lURL) != str:
                return lURL[1]

        return lURL

    def get_year(self):
        lYear = str_to_year(self.get_value('Founded'))
        if lYear:
            return lYear[0]
        else:
            lYear = str_to_year(self.get_value('Founded'))
            if lYear:
                return lYear[0]
        if not lYear:
            lYear = ''

        return lYear

    def get_company(self, sValue):
        lCompany = self.get_value(sValue)
        if lCompany and type(lCompany) != str:
            return clean_string(lCompany[0])

        return lCompany

    def get_location(self, sValue):
        lLocation = self.get_value(sValue)
        if lLocation and type(lLocation) != str:
            return lLocation[0]

        return lLocation

    def get_publication_type(self, sValues):
        lType = self.get_value(sValues)
        if lType:
            if type(lType) != str:
                lType = lower_list_values(str_to_list(lType[0]))
            else:
                lType = lower_list_values(str_to_list(lType))

        return lType

    def get_founder(self, sValue):
        lFounder = self.get_value(sValue)
        if lFounder:
            if type(lFounder) != str:
                lFounder = lFounder[0]
            lFounder = clean_list_values(get_values(lFounder))

        return lFounder

    def get_type(self, sValue):
        lType = self.get_value(sValue)
        if lType:
            if type(lType) != str:
                lType = lType[0]
            lType = clean_list_values(get_values(lType))

        return lType


if __name__ == '__main__':
    lURL = collect_links()

    sFileName = get_filename_time('../../files/file.backup/publisher.csv')
    with open(sFileName, 'w', newline='') as csvfile:
        oWriter = csv.writer(csvfile,
                             delimiter='|',
                             quotechar='"',
                             quoting=csv.QUOTE_MINIMAL)
        oROW = ('sFullName', 'sShortName', 'ParentCompany', 'Status',
                'Predecessor', 'sFounded', 'sFounder', 'CountryOfOrigin',
                'Headquarters', 'PublicationTypes', 'Owner', 'sWebsite',
                'OtherName', 'FormerName', 'Type', 'ParentInstitution',
                'AcademicAffiliation', 'Location', 'Country', 'Language',
                'WikiURL',)
        oWriter.writerow(oROW)

        for sURL in lURL:
            oP = PublisherValue(sURL)
            oROW = (oP.sFullName, oP.sShortName, oP.ParentCompany,
                    oP.Status, oP.Predecessor, oP.sFounded, oP.sFounder,
                    oP.CountryOfOrigin, oP.Headquarters, oP.PublicationTypes,
                    oP.Owner, oP.sWebsite, oP.OtherName, oP.FormerName,
                    oP.Type, oP.ParentInstitution, oP.AcademicAffiliation,
                    oP.Location, oP.Country, oP.Language, oP.WikiURL,)
            print(oROW)
            oWriter.writerow(oROW)
