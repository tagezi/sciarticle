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
""" The module collects information about journals and publishers on Wikipedia
    and enters them into a database. """

# TODO: This monster should be separated into two classes, and all check ID are
#       transport to SQLmain class
import re
import time

from config.config import DB_DIR, DB_FILE, FILES_DIR, WIKI_SOURCE
from sciarticle.lib.perfect_soup import PerfectSoup
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import *


def set_update(sValue, iID, sTable, sColumnValue, sColumnID):
    cValues = (sValue, iID,)
    oConnect.update(sTable, sColumnValue, sColumnID, cValues)


def set_dspln(sString, iID):
    lDspln = get_values(sString)
    for sDspln in lDspln:
        sDspln = clean_spaces(sDspln.lower())
        if not oConnect.q_get_id_dspln(sDspln):
            oConnect.q_insert_dspln((sDspln,))
            oConnect.q_insert_book_dspln((iID, sDspln,))


def set_book_lang(sString, iID):
    lLang = get_values(sString)
    for sLang in lLang:
        oConnect.q_insert_book_lang((iID, clean_spaces(sLang.lower()),))


def set_book_link(link, sColumn, iID):
    sLink = str(link.find("a").attrs['href'])
    oConnect.q_update_book(sColumn, (sLink, iID,))


def set_book_year(sString, iID):
    nums = re.findall(r'\d+', sString)
    iYear = [int(i) for i in nums]
    oConnect.q_update_book('creation_year', (iYear[0], iID,))


def set_editor(sString, iID):
    lEdited = get_values(sString)
    for sEdited in lEdited:
        oConnect.q_insert_book_editor((iID, sEdited,))


def set_issn(sProperty, iID):
    lISSN = sProperty.findAll("a")
    sISSN = lISSN[0].get_text()
    oConnect.q_update_book('issn_print', (sISSN, iID,))

    if len(lISSN) == 2:
        sISSN = lISSN[1].get_text()
        oConnect.q_update_book('issn_web', (sISSN, iID,))


def get_parameters(sStringURL, sName, sShortName, sDBTable, iDBID, sDBName):
    time.sleep(1)

    bsWikiPage = PerfectSoup(sStringURL)
    if bsWikiPage is None:
        return None
    if sName is None:
        sName = clean_parens(bsWikiPage.get_title_h1())

    iID = oConnect.sql_get_id(sDBTable, iDBID, sDBName, (sName,))
    if not iID:
        oConnect.insert_row(sDBTable, sDBName, (sName,))
        iID = oConnect.sql_get_id(sDBTable, iDBID, sDBName, (sName,))
        set_update(sStringURL, iID, sDBTable, 'wiki_url', iDBID)
        if sShortName is not None:
            set_update(sShortName, iID, sDBTable, 'short_name', iDBID)

    # TODO: During script work does mistake.
    #       This is now bypassed, but not resolved
    # https://en.wikipedia.org/wiki/Kyoto_University
    # https://en.wikipedia.org/wiki/Sophia_University
    if sName == 'Kyoto University' or sName == 'Sophia University':
        return None

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

    print(sName)
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
    sListAPub = sPub.findAll("a")
    # Sometimes a link points to external page, but here is internal needed
    sAPub = sListAPub
    if sListAPub:
        for sAPub in sListAPub:
            if sAPub.get_text().find('http') != -1:
                break
    # Sometimes Publisher name is shorter or longer then it is :)
    # And sometimes it's not there at all.
    if sAPub and sPubName.find(sAPub.get_text()) != -1:
        # Publisher is not Country name. Yes, in wikipedia it can be.
        if not oConnect.q_get_id_country(sAPub.get_text()):
            sPubName = clean_parens(sAPub.get_text())
            # If a link is in <a> tag, and it isn't redlink.
            if str(sAPub).find("href") != -1 \
                    and str(sAPub).find("http") == -1 \
                    and str(sAPub).find("redlink") == -1:
                sPubURL = get_wiki_url(str(sAPub.attrs['href']))

                bsPubPage = PerfectSoup(sPubURL)
                if bsPubPage is not None:
                    partHTML = bsPubPage.find(
                        "div", {"class": "mw-parser-output"}
                    ).findAll(
                        "p", {'class': None})
                    lBolsTag = []
                    for sPTag in partHTML:
                        lBolsTag = sPTag.findAll("b")
                        if lBolsTag:
                            break

                    k = int(0)
                    for sBold in lBolsTag:
                        try:
                            if int(k) == int(0):
                                sPubName = sBold.get_text()

                            elif int(k) == int(1):
                                if len(sPubName) < len(sBold.string):
                                    sShortPubName = sPubName
                                    sPubName = sBold.string
                                else:
                                    sShortPubName = sBold.string
                        except ValueError as e:
                            print(e)
                        k = k + 1

    if not oConnect.q_get_id_publisher(sPubName):
        if sPubURL is not None:
            get_pub_parameters(sPubURL, sPubName, sShortPubName)
        else:
            oConnect.insert_row('Publisher', 'full_name',
                                (sPubName,))

    return sPubName


def get_pub_parameters(sPublURL, sPublName, sShortPublName):
    dValues = get_parameters(sPublURL, sPublName, sShortPublName, 'Publisher',
                             'id_publisher', 'full_name')

    if dValues is None:
        return

    i = 0
    for sProperty in dValues['ListValues']:

        iID = dValues['ID']
        if dValues['ListName'][i] == ("Parent company" or "Owner(s)"):
            sPubName = get_pub_name(sProperty)
            iPubID = oConnect.q_get_id_publisher(sPubName)
            oConnect.q_update_publisher('parent_company',
                                        (iPubID, iID))

        elif dValues['ListName'][i] == "Founded":
            lFounded = get_values(sProperty.get_text())
            sCFounded = lFounded[(len(lFounded) - 1)]
            sFounded = lFounded[0]
            if len(sFounded) > 4:
                lFounded = sFounded.split(" ")
                sFounded = clean_parens(lFounded[(len(lFounded) - 1)])

            oConnect.q_update_publisher('creation_year', (sFounded, iID,))
            iIdCo = oConnect.q_get_id_country(sCFounded)
            if iIdCo:
                oConnect.q_update_publisher('creation_country', (iIdCo, iID,))

        elif dValues['ListName'][i] == "Headquarters location":
            lCountry = dValues["ListName"][i].split(", ")
            iIdCo = oConnect.q_get_id_country(lCountry[len(lCountry) - 1])
            if iIdCo:
                oConnect.q_update_publisher('id_country', (iIdCo, iID,))

        elif dValues['ListName'][i] == "Country of origin":
            iIdCo = oConnect.q_get_id_country(sProperty.get_text())
            if iIdCo:
                oConnect.q_update_publisher('creation_country', (iIdCo, iID,))

        elif dValues['ListName'][i] == ("Official website" or "Website"):
            sLink = str(sProperty.find("a").attrs['href'])
            oConnect.q_update_publisher('website', (sLink, iID))

        elif dValues['ListName'][i] == "Status":
            sStatus = sProperty.get_text()
            oConnect.q_update_publisher('status', (sStatus, iID))

        elif dValues['ListName'][i] == "Founder":
            sFounder = sProperty.get_text()
            oConnect.q_update_publisher('founder', (sFounder, iID))

        i = i + 1


def get_book_parameters(sBookURL):
    dValues = get_parameters(sBookURL, None, None,
                             'Book', 'id_book', 'book_name')
    if dValues is None or dValues['HTML'] is None:
        return

    iID = dValues['ID']
    for link in dValues['HTML']:
        if link.get_text() == 'Journal homepage':
            set_book_link(link, 'book_homepage', iID)
        elif link.get_text().find('access') != -1:
            set_book_link(link, 'online_access', iID)
        elif link.get_text().find('archive') != -1:
            set_book_link(link, 'online_archive', iID)

    i = 0
    for sProperty in dValues['ListValues']:

        # dspln is accepted abbreviation of word 'discipline'
        if dValues['ListName'][i] == "Discipline":
            set_dspln(sProperty.get_text(), iID)

        elif dValues['ListName'][i] == "Language":
            set_book_lang(sProperty.get_text(), iID)

        elif dValues['ListName'][i] == "Edited by":
            set_editor(sProperty.get_text(), iID)

        elif dValues['ListName'][i] == "History":
            set_book_year(sProperty.get_text(), iID)

        elif dValues['ListName'][i] == "Publisher":
            sPubName = get_pub_name(sProperty)
            iPubID = oConnect.q_get_id_publisher(sPubName)
            oConnect.q_update_book('publisher', (iPubID, iID,))

        elif dValues['ListName'][i] == "Frequency":
            sFrequency = sProperty.get_text()
            oConnect.q_update_book('book_frequency', (sFrequency, iID,))

        elif dValues['ListName'][i] == "ISO 4":
            sISO4 = sProperty.get_text()
            oConnect.q_update_book('iso_4', (sISO4, iID,))

        elif dValues['ListName'][i] == "ISSN":
            set_issn(sProperty, iID)

        elif dValues['ListName'][i] == "LCCN":
            sLCCN = sProperty.get_text()
            oConnect.q_update_book('lccn', (sLCCN, iID,))

        elif dValues['ListName'][i] == "OCLC no.":
            sOCLC = sProperty.get_text()
            oConnect.q_update_book('oclc_no', (sOCLC, iID,))

        i = i + 1


if __name__ == '__main__':
    wiki_sources = get_file_patch(FILES_DIR, WIKI_SOURCE)
    oConnect = SQLmain(get_file_patch(DB_DIR, DB_FILE))
    # lDeleted = ['BookLang', 'BookEditor',
    #             'BookDiscipline', 'Book', 'Publisher']
    # for sDel in lDeleted:
    #     oConnect.delete_row(sDel)

    with open(wiki_sources, "r") as f:
        for sPageListURL in f:
            bsObj = PerfectSoup(sPageListURL)
            if bsObj is None:
                continue
            lListURl = bsObj.get_link_from_list()
            for sPartURL in lListURl:
                get_book_parameters(get_wiki_url(sPartURL))
