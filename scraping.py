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
from strmain import *
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import re
import time


def get_parametrs(sURL, sName, sDBTable, iDBID, sDBName):
    time.sleep(3)

    try:
        htmlPublisher = urlopen(iriToUri(sURL))
    except (URLError, HTTPError) as e:
        print("Ошибка в урле: " + str(e) + "\nУРЛ: " + str(sURL))
        return None

    bsWikiPage = BeautifulSoup(htmlPublisher, "html5lib")
    if sName is None:
        sName = bsWikiPage.find("h1").get_text()
        sName = clean_parens(sName)

    oConnect.sql_insert(sDBTable, sDBName, (sName,))
    iID = oConnect.sql_search_id(sDBTable, iDBID, sDBName, (sName,))

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


def get_publisher_name(sPublisher):
    print(sPublisher.get_text())
    sPublisherName = clean_parens(sPublisher.get_text())
    sPublisherURL = None
    sAPublisher = sPublisher.find("a")
    if sAPublisher is not None:
        isNotName = oConnect.sql_search('Country', 'en_name_country', (sAPublisher.get_text(),))
        if isNotName is None:
            sPublisherName = clean_parens(sAPublisher.get_text())
            if str(sAPublisher).find("href") != -1:
                sPublisherURL = "https://en.wikipedia.org" + str(sAPublisher.attrs['href'])

    qPublisher = oConnect.sql_search('Publisher', 'publisher_name', (sPublisherName,))
    if qPublisher is None:
        if sPublisherURL is not None:
            get_publisher_parametrs(sPublisherURL, sPublisherName)
        else:
            lValues = (sPublisherName,)
            oConnect.sql_insert('Publisher', 'publisher_name', lValues)

    return sPublisherName


def get_publisher_parametrs(sURLPublisher, sPublisherName):
    dValues = get_parametrs(sURLPublisher, sPublisherName, 'Publisher', 'id_publisher', 'publisher_name')

    if dValues is None:
        return

    i = 0
    for sProperty in dValues['ListValues']:

        if dValues['ListName'][i] == "Parent company" or dValues['ListName'][i] == "Owner(s)":
            sPublisherName = get_publisher_name(sProperty)
            iPublisherID = oConnect.sql_search_id("Publisher", 'id_publisher', 'publisher_name', (sPublisherName,))
            cValues = (iPublisherID, dValues['ID'],)
            oConnect.sql_update('Publisher', 'mother_company', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Founded":
            lFounded = get_values(sProperty.get_text())
            sCountryFouded = lFounded[(len(lFounded) - 1)]
            sFounded = lFounded[0]
            if len(sFounded) > 4:
                lFounded = sFounded.split(" ")
                sFounded = lFounded[(len(lFounded) - 1)]

            cValues = (clean_parens(sFounded), dValues['ID'],)
            oConnect.sql_update('Publisher', 'creation_year', 'id_publisher', cValues)
            iIdCountry = oConnect.sql_search_id("Country", 'id_country', 'en_name_country', (sCountryFouded,))

            if iIdCountry != 0:
                cValues = (iIdCountry, dValues['ID'],)
                oConnect.sql_update('Publisher', 'creation_country', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Headquarters location":
            lCountry = dValues["ListName"][i].split(", ")
            iIdCountry = oConnect.sql_search_id("Country", 'id_country', 'en_name_country', (lCountry[len(lCountry)-1],))

            if iIdCountry != 0:
                cValues = (iIdCountry, dValues['ID'],)
                oConnect.sql_update('Publisher', 'id_country', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Country of origin":
            iIdCountry = oConnect.sql_search_id("Country", 'id_country', 'en_name_country', (sProperty.get_text(),))

            if iIdCountry != 0:
                cValues = (iIdCountry, dValues['ID'],)
                oConnect.sql_update('Publisher', 'creation_country', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Official website" or dValues['ListName'][i] == "Website":
            cValues = (str(sProperty.find("a").attrs['href']), dValues['ID'],)
            oConnect.sql_update('Publisher', 'website', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Status":
            cValues = (sProperty.get_text(), dValues['ID'],)
            oConnect.sql_update('Publisher', 'status', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Founder":
            cValues = (sProperty.get_text(), dValues['ID'],)
            oConnect.sql_update('Publisher', 'founder', 'id_publisher', cValues)

        i = i + 1


def get_journal_parametrs(sURL):
    dValues = get_parametrs(sURL, None, 'Journal', 'id_journal', 'journal_name')

    if dValues is None or dValues['HTML'] is None:
        return

    print(dValues['HTML'])
    for link in dValues['HTML']:
        if link.get_text() == "Journal homepage":
            cValues = (str(link.find("a").attrs['href']), dValues['ID'],)
            oConnect.sql_update('Journal', 'journal_homepage', 'id_journal', cValues)

        if link.get_text() == "Online access":
            cValues = (str(link.find("a").attrs['href']), dValues['ID'],)
            oConnect.sql_update('Journal', 'online_access', 'id_journal', cValues)

        if link.get_text() == "Online archive":
            cValues = (str(link.find("a").attrs['href']), dValues['ID'],)
            oConnect.sql_update('Journal', 'online_archive', 'id_journal', cValues)

    i = 0
    for sProperty in dValues['ListValues']:

        if dValues['ListName'][i] == "Discipline":
            sDiscipline = sProperty.get_text()
            lDiscipline = get_values(sDiscipline)
            for sDiscipline in lDiscipline:
                iDiscipline = oConnect.sql_search_id('Discipline', 'id_discipline', 'discipline_name', (sDiscipline,))
                if iDiscipline == 0:
                    oConnect.sql_insert('Discipline', 'discipline_name', (sDiscipline,))
                cValues = (dValues['ID'], iDiscipline,)
                oConnect.sql_insert('JournalDiscipline', 'id_journal, id_discipline', cValues)

        if dValues['ListName'][i] == "Language":
            sLang = sProperty.get_text()
            lLang = get_values(sLang)
            for sLang in lLang:
                iLang = oConnect.sql_search_id('Lang', 'id_lang', 'en_name', (sLang,))
                oConnect.sql_insert('JournalLang', 'id_journal, id_lang', (dValues['ID'], iLang,))

        if dValues['ListName'][i] == "Edited by":
            sEdited = sProperty.get_text()
            lEdited = get_values(sEdited)
            for sEdited in lEdited:
                oConnect.sql_insert('JournalEditor', 'id_journal, editor', (dValues['ID'], sEdited,))

        if dValues['ListName'][i] == "History":
            nums = re.findall(r'\d+', sProperty.get_text())
            iYear = [int(i) for i in nums]
            cValues = (clean_parens(iYear[0]), dValues['ID'],)
            oConnect.sql_update('Journal', 'creation_year', 'id_journal', cValues)

        if dValues['ListName'][i] == "Publisher":
            sPublisherName = get_publisher_name(sProperty)
            iPublisherID = oConnect.sql_search_id('Publisher', 'id_publisher', 'publisher_name', (sPublisherName,))
            cValues = (iPublisherID, dValues['ID'],)
            oConnect.sql_update('Journal', 'publisher', 'id_journal', cValues)

        if dValues['ListName'][i] == "Frequency":
            cValues = (sProperty.get_text(), dValues['ID'],)
            oConnect.sql_update('Journal', 'journal_frequency', 'id_journal', cValues)

        if dValues['ListName'][i] == "ISO 4":
            cValues = (sProperty.get_text(), dValues['ID'],)
            oConnect.sql_update('Journal', 'iso_4', 'id_journal', cValues)

        if dValues['ListName'][i] == "ISSN":
            lISSN = sProperty.findAll("a")
            sISSN = lISSN[0].get_text()
            cValues = (sISSN, dValues['ID'],)
            oConnect.sql_update('Journal', 'issn_print', 'id_journal', cValues)
            if len(lISSN) == 2:
                sISSN = lISSN[1].get_text()
                cValues = (sISSN, dValues['ID'],)
                oConnect.sql_update('Journal', 'issn_web', 'id_journal', cValues)

        if dValues['ListName'][i] == "LCCN":
            cValues = (sProperty.get_text(), dValues['ID'],)
            oConnect.sql_update('Journal', 'lccn', 'id_journal', cValues)

        if dValues['ListName'][i] == "OCLC no.":
            cValues = (sProperty.get_text(), dValues['ID'],)
            oConnect.sql_update('Journal', 'oclc_no', 'id_journal', cValues)

        i = i + 1


oConnect = Sqlmain('./db/test_sql.db')

oConnect.sql_table_clean('Publisher')
oConnect.sql_table_clean('JournalLang')
oConnect.sql_table_clean('JournalEditor')
oConnect.sql_table_clean('JournalDiscipline')
oConnect.sql_table_clean('Journal')

with open("file.backup/wiki.txt", "r") as f:
    for line in f:
        print(line)
        try:
            html = urlopen(iriToUri(line))
        except (URLError, HTTPError) as e:
            print("Ошибка в основной программе: " + str(e) + "\nУРЛ: " + str(line))
        else:
            bsObj = BeautifulSoup(html, "html5lib")
            lListURl = bsObj.find("div", {"mw-category"}).findAll("a")

            for URL in lListURl:
                sURL = "https://en.wikipedia.org" + str(URL.attrs['href'])
                get_journal_parametrs(sURL)
