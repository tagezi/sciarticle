import sqlite3
from sqlmain import *
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse, urlunparse, quote
from bs4 import BeautifulSoup
import re
import time


def get_values(sString):
    sString = sString.replace(" and ", ", ")
    sString = sString.replace("; ", ", ")
    sString = sString.replace(",,", ", ")
    sString = sString.replace("  ", " ")
    lString = sString.split(", ")

    return lString


def iriToUri(iri):
    parts = urlparse(iri)
    partUri = quote(parts[2], safe='/')
    listParamUri = (parts[0], parts[1], partUri, parts[3], parts[4], parts[5])
    try:
        uri = urlunparse(listParamUri)
    except ValueError as e:
        print("не пахает, потому что " + str(e))
        return None

    return uri


def get_parametrs(oConstructor, sURL, sName, sDBTable, iDBID, sDBName):
    time.sleep(3)

    try:
        htmlPublisher = urlopen(iriToUri(sURL))
    except (URLError, HTTPError) as e:
        print("Ошибка в урле: " + str(e) + "\nУРЛ: " + str(sURL))
        return None
    else:
        bsObjWikiPage = BeautifulSoup(htmlPublisher, "html5lib")
        if sName is None:
            sName = bsObjWikiPage.find("h1").get_text()

        sql_insert(oConstructor, sDBTable, sDBName, (sName,))
        iID = sql_search_id(oConstructor, sDBTable, iDBID, sDBName, (sName,))

        lHtmlListName = bsObjWikiPage.findAll("th", {"infobox-label"})
        lHtmlListValues = bsObjWikiPage.findAll("td", {"infobox-data"})
        lListName = []
        for name in lHtmlListName:
            lListName.append(name.get_text())

        dValues = dict()
        dValues['Name'] = sName
        dValues['ID'] = iID
        dValues['ListName'] = lListName
        dValues['ListValues'] = lHtmlListValues
        dValues['HTML'] = bsObjWikiPage

        return dValues


def get_publisher_parametrs(sURLPublisher, sPublisherName):
    dValues = get_parametrs(oConstructor, sURLPublisher, sPublisherName, 'Publisher', 'id_publisher', 'publisher_name')

    if dValues is None:
        return

    i = 0
    for name in dValues['ListValues']:

        if dValues['ListName'][i] == "Parent company" or dValues['ListName'][i] == "Owner(s)":
            sAPublisher = name.find("a")
            sPublisher = sAPublisher.get_text()
            sURLPublisher = "https://en.wikipedia.org" + str(sAPublisher.attrs['href'])
            print(sURLPublisher)

            if sPublisher != "":
                qPublisher = sql_search(oConstructor, 'Publisher', 'publisher_name', (sPublisher,))

                if qPublisher is None:
                    get_publisher_parametrs(sURLPublisher, sPublisher)

                iIdCountry = sql_search_id(oConstructor, "Publisher", 'id_publisher', 'publisher_name', (sPublisher,))
                cValues = (iIdCountry, dValues['ID'],)
                sql_update(oConstructor, 'Publisher', 'mother_company', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Founded":
            lFounded = get_values(name.get_text())
            sCountryFouded = lFounded[(len(lFounded) - 1)]
            sFounded = lFounded[0]
            if len(sFounded) > 4:
                lFounded = sFounded.split(" ")
                sFounded = lFounded[(len(lFounded) - 1)]

            cValues = (sFounded, dValues['ID'],)
            sql_update(oConstructor, 'Publisher', 'creation_year', 'id_publisher', cValues)
            iIdCountry = sql_search_id(oConstructor, "Country", 'id_country',
                                       'en_name_country', (sCountryFouded,))

            if iIdCountry != 0:
                cValues = (iIdCountry, dValues['ID'],)
                sql_update(oConstructor, 'Publisher', 'creation_country', 'id_publisher', cValues)
        else:
            print("A country is not found for the publisher" + sPublisherName + ".")

        if dValues['ListName'][i] == "Country of origin":
            iIdCountry = sql_search_id(oConstructor, "Country", 'id_country', 'en_name_country', (name.get_text(),))

            if iIdCountry != 0:
                cValues = (iIdCountry, dValues['ID'],)
                sql_update(oConstructor, 'Publisher', 'id_country', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Official website" or dValues['ListName'][i] == "Website":
            cValues = (str(name.find("a").attrs['href']), dValues['ID'],)
            sql_update(oConstructor, 'Publisher', 'website', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Status":
            cValues = (name.get_text(), dValues['ID'],)
            sql_update(oConstructor, 'Publisher', 'status', 'id_publisher', cValues)

        if dValues['ListName'][i] == "Founder":
            cValues = (name.get_text(), dValues['ID'],)
            sql_update(oConstructor, 'Publisher', 'founder', 'id_publisher', cValues)

        i = i + 1


def get_journal_parametrs(sURL):
    dValues = get_parametrs(oConstructor, sURL, None, 'Journal', 'id_journal', 'journal_name')

    i = 0
    for name in dValues['ListValues']:

        if dValues['ListName'][i] == "Discipline":
            sDiscipline = name.get_text()
            lDiscipline = get_values(sDiscipline)
            for sDiscipline in lDiscipline:
                iDiscipline = sql_search_id(oConstructor, 'Discipline', 'id_discipline', 'discipline_name',
                                            (sDiscipline,))
                if iDiscipline == 0:
                    sql_insert(oConstructor, 'Discipline', 'discipline_name', (sDiscipline,))
                cValues = (dValues['ID'], iDiscipline,)
                sql_insert(oConstructor, 'JournalDiscipline', 'id_journal, id_discipline', cValues)

        if dValues['ListName'][i] == "Language":
            sLang = name.get_text()
            lLang = get_values(sLang)
            for sLang in lLang:
                iLang = sql_search_id(oConstructor, 'Lang', 'id_lang', 'en_name', (sLang,))
                sql_insert(oConstructor, 'JournalLang', 'id_journal, id_lang', (dValues['ID'], iLang,))

        if dValues['ListName'][i] == "Edited by":
            sEdited = name.get_text()
            lEdited = get_values(sEdited)
            for sEdited in lEdited:
                sql_insert(oConstructor, 'JournalEditor', 'id_journal, editor', (dValues['ID'], sEdited,))

        if dValues['ListName'][i] == "History":
            nums = re.findall(r'\d+', name.get_text())
            iYear = [int(i) for i in nums]
            cValues = (iYear[0], dValues['ID'],)
            sql_update(oConstructor, 'Journal', 'creation_year', 'id_journal', cValues)

        if dValues['ListName'][i] == "Publisher":
            print(name.get_text())
            sAPublisher = name.find("a")
            if sAPublisher is not None:
                sPublisher = sAPublisher.get_text()
                sURLPublisher = "https://en.wikipedia.org" + str(sAPublisher.attrs['href'])
            else:
                sPublisher = name.get_text()

            qPublisher = sql_search(oConstructor, 'Publisher', 'publisher_name', (sPublisher,))
            if qPublisher is None:
                if sAPublisher is not None:
                    get_publisher_parametrs(sURLPublisher, sPublisher)
                else:
                    lValues = (sPublisher,)
                    sql_insert(oConstructor, 'Publisher', 'publisher_name', lValues)

        if dValues['ListName'][i] == "Frequency":
            cValues = (name.get_text(), dValues['ID'],)
            sql_update(oConstructor, 'Journal', 'journal_frequency', 'id_journal', cValues)

        if dValues['ListName'][i] == "ISO 4":
            cValues = (name.get_text(), dValues['ID'],)
            sql_update(oConstructor, 'Journal', 'iso_4', 'id_journal', cValues)

        if dValues['ListName'][i] == "ISSN":
            lISSN = name.findAll("a")
            sISSN = lISSN[0].get_text()
            cValues = (sISSN, dValues['ID'],)
            sql_update(oConstructor, 'Journal', 'issn_print', 'id_journal', cValues)
            if len(lISSN) == 2:
                sISSN = lISSN[1].get_text()
                cValues = (sISSN, dValues['ID'],)
                sql_update(oConstructor, 'Journal', 'issn_web', 'id_journal', cValues)

        if dValues['ListName'][i] == "LCCN":
            cValues = (name.get_text(), dValues['ID'],)
            sql_update(oConstructor, 'Journal', 'lccn', 'id_journal', cValues)

        if dValues['ListName'][i] == "OCLC no.":
            cValues = (name.get_text(), dValues['ID'],)
            sql_update(oConstructor, 'Journal', 'oclc_no', 'id_journal', cValues)

        i = i + 1

        lHtmlListValues = dValues['HTML'].find("table", {"infobox hproduct"}).find("td", {"infobox-full-data"})
        llinks = lHtmlListValues.findAll("li")
        for link in llinks:
            if link.get_text() == "Journal homepage":
                cValues = (str(link.find("a").attrs['href']), dValues['ID'],)
                sql_update(oConstructor, 'Journal', 'journal_homepage', 'id_journal', cValues)

            if link.get_text() == "Online access":
                cValues = (str(link.find("a").attrs['href']), dValues['ID'],)
                sql_update(oConstructor, 'Journal', 'online_access', 'id_journal', cValues)

            if link.get_text() == "Online archive":
                cValues = (str(link.find("a").attrs['href']), dValues['ID'],)
                sql_update(oConstructor, 'Journal', 'online_archive', 'id_journal', cValues)


oConstructor = sqlite3.connect('./db/test_sql.db')

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
