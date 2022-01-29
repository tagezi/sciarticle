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
""" Module provide interface for Publisher values. """
import csv
import os

from config.config import DB_DIR, DB_FILE
from sciarticle.lib.perfect_soup import PerfectSoup
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import *
from sciarticle.get_link import collect_links


def save_publisher_to_csv(sFile):
    """ Saves information about publishers into csv file

        :param sFile: File name as string.
        :type sFile: str
        """
    with open(sFileName, 'w', newline='') as csvfile:
        oWriter = csv.writer(csvfile,
                             delimiter='|',
                             quotechar='"',
                             quoting=csv.QUOTE_MINIMAL)
        oROW = ('sFullName', 'sShortName', 'ParentCompany', 'Status',
                'Predecessor', 'sFounder', 'CountryOfOrigin',
                'Headquarters', 'PublicationTypes', 'Owner', 'sWebsite',
                'OtherName', 'FormerName', 'Type', 'ParentInstitution',
                'AcademicAffiliation', 'Location', 'Country', 'Language',
                'WikiURL',)
        oWriter.writerow(oROW)

        for sURL in lURL:
            oP = PublisherValue(sURL)
            oROW = (oP.sFullName, oP.sShortName, oP.ParentCompany,
                    oP.Status, oP.Predecessor, oP.sFounder,
                    oP.CountryOfOrigin, oP.Headquarters, oP.PublicationTypes,
                    oP.Owner, oP.sWebsite, oP.OtherName, oP.FormerName,
                    oP.Type, oP.ParentInstitution, oP.AcademicAffiliation,
                    oP.Location, oP.Country, oP.Language, oP.WikiURL,)
            print(oROW)
            oWriter.writerow(oROW)


class PublisherValue:
    """ Class provides methods and members for using for saving information
        from Wikipedia about Publishers. """
    def __init__(self, sPageURL):
        """ Creates members form which can be taken values about publishers

            :param sPageURL: URL as string.
            :type sPageURL: str
            """
        self.oPS = PerfectSoup(sPageURL)

        self.sFullName = self.get_name('FullName')
        # common name
        self.sShortName = self.get_name('ShortName')
        self.ParentCompany = self.get_company('Parent company')
        # or
        self.ParentInstitution = self.get_value('Parent Institution')
        # Active or Inactive
        self.Status = self.get_activity()
        self.Predecessor = self.get_value('Predecessor')
        self.sCreationYear = self.get_year()
        self.sFounder = self.get_founder('Founder')
        # Books,journals, technical report, e.g.
        self.PublicationTypes = self.get_publication_type('Publication types')
        self.Owner = self.get_owner()
        # if it is
        self.OtherName = self.get_value('Other Name')
        self.FormerName = self.get_value('Former Name')
        # non-profit, private, e.g.
        self.Type = self.get_type('Type')
        self.AcademicAffiliation = self.get_value('Academic Affiliation')
        self.CountryOfOrigin = self.get_location('Country of origin')
        self.Headquarters = self.get_location('Headquarters location')
        self.Location = self.get_location('Location')
        self.Language = self.get_value('Language')
        # Official Website
        self.sWebsite = self.get_url()
        self.WikiURL = sPageURL

    def get_value(self, sValue):
        """ Returns a value from a dictionary of values by its key.

            :param sValue: A key of values in dict as string.
            :type sValue: str
            :return: A value from the dictionary by key.
            :rtype: str or tuple
            """
        return self.oPS.dBlock.get(sValue)

    def get_name(self, sValue):
        """ Returns a name of the publisher that showed in a bold part of the
            string. If the bold string is nothing, the name is taken from
            title of the page.

            :param sValue: A key of ShortName or FullName.
            :type: str
            :return: The name of the publisher.
            :rtype: str
            """
        sNames = self.oPS.get_name_from_bold()
        sName = sNames.get(sValue)
        if sValue == 'FullName' and not sName:
            sName = self.oPS.get_title_h1()

        return sName

    def get_owner(self):
        """ Returns an owner name of the publisher.

            :return: The name of the publisher.
            :rtype: str
            """
        sOwner = self.get_value('Owner(s)')
        if sOwner and type(sOwner) != str:
            return sOwner[0]

        return sOwner

    def get_activity(self):
        """ Returns an activity of the publisher, if it is pointed.

            :return: An activity of the publisher.
            :rtype: str
            """
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
        """ Returns an url of official publisher website.

            :return: An URL of the publisher website.
            :rtype: str
            """
        lURL = self.oPS.dBlock.get('Official website')
        if not lURL:
            lURL = self.oPS.dBlock.get('Website')
        if lURL:
            if type(lURL) != str:
                return lURL[1]

        return lURL

    def get_year(self):
        """ Returns creation year of the publisher from the dictionary.

            :return: Year of creation.
            :rtype: int
            """
        iYear = str_to_year(self.get_value('Founded'))
        if iYear:
            return iYear[0]
        else:
            iYear = str_to_year(self.get_value('Founded'))
            if iYear:
                return iYear[0]
        if not iYear:
            iYear = ''

        return iYear

    def get_company(self, sValue):
        """ Returns a name of the parent company of the publisher.

            :return: The name of company.
            :rtype: str
            """
        lCompany = self.get_value(sValue)
        if lCompany and type(lCompany) != str:
            return clean_string(lCompany[0])

        return lCompany

    def get_location(self, sValue):
        """ Returns an origin or headquarters country of the publisher by key.

            :param sValue: A key 'Headquarters location' or 'Country of origin'
            :type sValue: str
            :return: A name of the publisher.
            :type: str
            """
        lLocation = self.get_value(sValue)
        if lLocation and type(lLocation) != str:
            return lLocation[0]

        return lLocation

    def get_publication_type(self, sValues):
        """ Returns a type of publications which the publisher publishes. :)

            :param sValues: The key Publication types of the dictionary.
            :type sValues: str
            :return: A type of the publication.
            :type: str or tuple
            """
        lType = self.get_value(sValues)
        if lType:
            if type(lType) != str:
                lType = lower_list_values(str_to_list(lType[0]))
            else:
                lType = lower_list_values(str_to_list(lType))

        return lType

    def get_founder(self, sValue):
        """ Returns a name of the publisher.

            :param sValue: The key of the dictionary.
            :type sValue: str
            :return: The name of the publisher.
            :rtype: str or tuple
            """
        lFounder = self.get_value(sValue)
        if lFounder:
            if type(lFounder) != str:
                lFounder = lFounder[0]
            lFounder = clean_list_values(get_values(lFounder))

        return lFounder

    def get_type(self, sValue):
        """ Return a type of publisher.

            :param sValue: The key of the dictionary.
            :type sValue: str
            :return: The type of publisher.
            :rtype: str
            """
        lType = self.get_value(sValue)
        if lType:
            if type(lType) != str:
                lType = lType[0]
            lType = clean_list_values(get_values(lType))

        return lType


if __name__ == '__main__':
    lURL = collect_links()

    sFileName = get_filename_time('../../files/file.backup/publisher.csv')
    save_publisher_to_csv(sFileName)
