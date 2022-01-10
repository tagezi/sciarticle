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

import time

from lib.sqlmain import *
from lib.strmain import *
from lib.perfect_soup import *
import config


def set_update(sValue, iID, sTable, sColumnValue, sColumnID):
    cValues = (sValue, iID,)
    oConnect.sql_update(sTable, sColumnValue, sColumnID, cValues)


def get_parameters(sURL, sName, sShortName, sDBTable, iDBID, sDBName):
    time.sleep(2)

    bsWikiPage = get_html(sURL)
    if bsWikiPage is None:
        return None
    if sName is None:
        sName = bsWikiPage.find("h1").get_text()
        sName = clean_parens(sName)
        if sName == 'Monumenta Nipponica':
            return None
        print(sName)

    iID = oConnect.sql_search_id(sDBTable, iDBID, sDBName, (sName,))
    if iID == 0:
        oConnect.sql_insert(sDBTable, sDBName, (sName,))
        iID = oConnect.sql_search_id(sDBTable, iDBID, sDBName, (sName,))
        set_update(sURL, iID, sDBTable, 'wiki_url', iDBID)
        if sShortName is not None:
            set_update(sShortName, iID, sDBTable, 'short_name', iDBID)

    lHtmlListName = bsWikiPage.findAll("th", {"infobox-label"})
    lHtmlListValues = bsWikiPage.findAll("td", {"infobox-data"})
    sHTML = bsWikiPage.find("table", {"infobox hproduct"})
    if sHTML is not None:
        sHTML = sHTML.find("td", {"infobox-full-data"})
        if sHTML:
            sHTML = sHTML.findAll("li")

    lListName = []
    for name in lHtmlListName:
        lListName.append(name.get_text())

    dValues = dict()
    dValues['Name'] = sName
    dValues['ID'] = iID
    dValues['ListName'] = lListName
    dValues['ListValues'] = lHtmlListValues
    dValues['HTML'] = sHTML

    return dValues


def get_pub_name(sPub):
    sPubName = clean_parens(sPub.get_text())
    sPubURL = None
    sShortPubName = None
    sAPub = sPub.find("a")
    if sAPub is not None and sPubName.find(sAPub.get_text()) == 0:
        isCountry = oConnect.sql_search('Country', 'en_name_country',
                                        (sAPub.get_text(),))
        if isCountry is None:
            sPubName = clean_parens(sAPub.get_text())
            if str(sAPub).find("href") != -1 and \
                    str(sAPub).find("redlink") == -1:
                sPubURL = "https://en.wikipedia.org" + str(sAPub.attrs['href'])

                bsPubPage = get_html(sPubURL)
                if bsPubPage is not None:
                    partHTML = bsPubPage.find("div", {
                        "class": "mw-parser-output"}).findAll("p",
                                                              {'class': None})
                    lBolsTag = []
                    for sPTag in partHTML:
                        lBolsTag = sPTag.findAll("b")
                        if lBolsTag:
                            break

                    k = int(0)
                    for sBold in lBolsTag:
                        try:
                            if int(k) == int(0):
                                sPubName = sBold.string

                            elif int(k) == int(1):
                                if len(sPubName) < len(sBold.string):
                                    sShortPubName = sPubName
                                    sPubName = sBold.string
                                else:
                                    sShortPubName = sBold.string
                        except ValueError as e:
                            print(e)
                        k = k + 1

    qPub = oConnect.sql_search('Publisher', 'publisher_name', (sPubName,))
    if qPub is None:
        if sPubURL is not None:
            get_pub_parameters(sPubURL, sPubName, sShortPubName)
        else:
            oConnect.sql_insert('Publisher', 'publisher_name',
                                (sPubName,))

    return sPubName


def get_pub_parameters(sURLPubl, sPublName, sShortPublName):
    dValues = get_parameters(sURLPubl, sPublName, sShortPublName, 'Publisher',
                             'id_publisher', 'publisher_name')

    if dValues is None:
        return

    i = 0
    for sProperty in dValues['ListValues']:

        if dValues['ListName'][i] == ("Parent company" or "Owner(s)"):
            sPubName = get_pub_name(sProperty)
            iPubID = oConnect.sql_search_id("Publisher", 'id_publisher',
                                            'publisher_name', (sPubName,))
            set_update(iPubID, dValues['ID'], 'Publisher',
                       'mother_company', 'id_publisher')

        if dValues['ListName'][i] == "Founded":
            lFounded = get_values(sProperty.get_text())
            sCFouded = lFounded[(len(lFounded) - 1)]
            sFounded = lFounded[0]
            if len(sFounded) > 4:
                lFounded = sFounded.split(" ")
                sFounded = lFounded[(len(lFounded) - 1)]

            set_update(clean_parens(sFounded), dValues['ID'], 'Publisher',
                       'creation_year', 'id_publisher')
            iIdCountry = oConnect.sql_search_id("Country", 'id_country',
                                                'en_name_country', (sCFouded,))
            if iIdCountry != 0:
                set_update(iIdCountry, dValues['ID'], 'Publisher',
                           'creation_country', 'id_publisher')

        if dValues['ListName'][i] == "Headquarters location":
            lCountry = dValues["ListName"][i].split(", ")
            iIdCountry = oConnect.sql_search_id("Country", 'id_country',
                                                'en_name_country',
                                                (lCountry[len(lCountry) - 1],))
            if iIdCountry != 0:
                set_update(iIdCountry, dValues['ID'], 'Publisher',
                           'id_country', 'id_publisher')

        if dValues['ListName'][i] == "Country of origin":
            iIdCountry = oConnect.sql_search_id("Country", 'id_country',
                                                'en_name_country',
                                                (sProperty.get_text(),))
            if iIdCountry != 0:
                set_update(iIdCountry, dValues['ID'], 'Publisher',
                           'creation_country', 'id_publisher')

        if dValues['ListName'][i] == ("Official website" or "Website"):
            set_update(str(sProperty.find("a").attrs['href']), dValues['ID'],
                       'Publisher', 'website', 'id_publisher')

        if dValues['ListName'][i] == "Status":
            set_update(sProperty.get_text(), dValues['ID'], 'Publisher',
                       'status', 'id_publisher')

        if dValues['ListName'][i] == "Founder":
            set_update(sProperty.get_text(), dValues['ID'], 'Publisher',
                       'founder', 'id_publisher')

        i = i + 1


def get_book_parametrs(sURL):
    dValues = get_parameters(sURL, None, None, 'Book', 'id_book', 'book_name')

    if dValues is None or dValues['HTML'] is None:
        return

    for link in dValues['HTML']:
        if link.get_text() == ("Journal homepage" or
                               "Online access" or "Online archive"):
            set_update(str(link.find("a").attrs['href']), dValues['ID'],
                       'Book', 'book_homepage', 'id_book')

    i = 0
    for sProperty in dValues['ListValues']:

        if dValues['ListName'][i] == "Discipline":
            sDiscipline = sProperty.get_text()
            lDiscipline = get_values(sDiscipline)
            for sDiscipline in lDiscipline:
                iDiscipline = oConnect.sql_search_id('Discipline',
                                                     'id_discipline',
                                                     'discipline_name',
                                                     (sDiscipline,))
                if iDiscipline == 0:
                    oConnect.sql_insert('Discipline', 'discipline_name',
                                        (sDiscipline,))
                cValues = (dValues['ID'], iDiscipline,)
                oConnect.sql_insert('BookDiscipline', 'id_book, id_discipline',
                                    cValues)

        if dValues['ListName'][i] == "Language":
            sLang = sProperty.get_text()
            lLang = get_values(sLang)
            for sLang in lLang:
                iLang = oConnect.sql_search_id('Lang', 'id_lang', 'en_name',
                                               (sLang,))
                oConnect.sql_insert('BookLang', 'id_book, id_lang',
                                    (dValues['ID'], iLang,))

        if dValues['ListName'][i] == "Edited by":
            sEdited = sProperty.get_text()
            lEdited = get_values(sEdited)
            for sEdited in lEdited:
                oConnect.sql_insert('BookEditor', 'id_book, editor',
                                    (dValues['ID'], sEdited,))

        if dValues['ListName'][i] == "History":
            nums = re.findall(r'\d+', sProperty.get_text())
            iYear = [int(i) for i in nums]
            set_update(clean_parens(iYear[0]), dValues['ID'], 'Book',
                       'creation_year', 'id_book')

        if dValues['ListName'][i] == "Publisher":
            sPubName = get_pub_name(sProperty)
            iPubID = oConnect.sql_search_id('Publisher', 'id_publisher',
                                            'publisher_name', (sPubName,))
            set_update(iPubID, dValues['ID'], 'Book', 'publisher', 'id_book')

        if dValues['ListName'][i] == "Frequency":
            set_update(sProperty.get_text(), dValues['ID'], 'Book',
                       'book_frequency', 'id_book')

        if dValues['ListName'][i] == "ISO 4":
            set_update(sProperty.get_text(), dValues['ID'],
                       'Book', 'iso_4', 'id_book')

        if dValues['ListName'][i] == "ISSN":
            lISSN = sProperty.findAll("a")
            sISSN = lISSN[0].get_text()
            set_update(sISSN, dValues['ID'], 'Book', 'issn_print', 'id_book')
            if len(lISSN) == 2:
                sISSN = lISSN[1].get_text()
                set_update(sISSN, dValues['ID'], 'Book', 'issn_web', 'id_book')

        if dValues['ListName'][i] == "LCCN":
            set_update(sProperty.get_text(), dValues['ID'],
                       'Book', 'lccn', 'id_book')

        if dValues['ListName'][i] == "OCLC no.":
            set_update(sProperty.get_text(), dValues['ID'],
                       'Book', 'oclc_no', 'id_book')

        i = i + 1


oConnect = Sqlmain(var.db_file)

# lTableClean = ('Publisher', 'BookLang',
#                'BookEditor', 'BookDiscipline', 'Book')
# for sTableC in lTableClean:
#     oConnect.sql_table_clean(sTableC)

with open("files/file.backup/wiki.txt", "r") as f:
    for sURL in f:
        bsObj = get_html(sURL)
        if bsObj is None:
            continue
        lListURl = bsObj.find("div", {"mw-category"}).findAll("a")
        for URL in lListURl:
            sURL = "https://en.wikipedia.org" + str(URL.attrs['href'])
            get_book_parametrs(sURL)