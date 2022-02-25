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


""" The module provides an interface for working with the language table.
    You can use this module as a program or functional from the main module.
    """

import argparse
import csv

from sciarticle.lib.help import get_lang_argument, get_delimiter_csv
from config.config import DB_FILE, DB_DIR, DELIMITER_CSV, EPILOG_HELP, \
    pach_path
from sciarticle.lib.perfect_soup import PerfectSoup
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import *


def get_lang_var_to_file(sFileName, sDelimiter):
    """ Gets data from LangVariant table and creates CSV file with it.

        :param sFileName: a string, which contains file patch and name,
                          where is saved data.
        :param sDelimiter: a string, which contains delimiter fo CSV file.
        """
    sFileName = get_filename_time(sFileName)

    with open(sFileName, 'w', newline='') as csvfile:
        oWriter = csv.writer(csvfile,
                             delimiter=sDelimiter,
                             quotechar='"',
                             quoting=csv.QUOTE_MINIMAL)

        tAnswerRow = oConnector.sql_get_all('LangVariant')
        lRow = ""
        lValue = []
        for tLangRow in tAnswerRow:
            if tLangRow[1] != lRow:
                if lRow:
                    oWriter.writerow(lValue)
                    lValue = []
                lRow = tLangRow[1]
                lValue.append(tLangRow[2])
            else:
                lValue.append(tLangRow[2])


def get_lang_to_file(sFileName, sDelimiter):
    """ Gets data from Lang table and creates CSV file with it

        :param sFileName: string, which contains file patch and name,
                          where is saved data.
        :param sDelimiter: string, which contains delimiter of CSV file.
        """
    sFileName = get_filename_time(sFileName)

    with open(sFileName, 'w', newline='') as csvfile:
        oWriter = csv.writer(csvfile,
                             delimiter=sDelimiter,
                             quotechar='"',
                             quoting=csv.QUOTE_MINIMAL)

        tRow = oConnector.sql_get_all('Lang')
        for rRow in tRow:
            oWriter.writerow(rRow[1:8])


def fill_lang_variant(sFileName, sDelimiter):
    """ Gets data from file and fills LangVariant table in database

        :param sFileName: string, which contains file patch and name,
                         where is taken data
        :param sDelimiter: string, which contains delimiter for parsing CSV
        """
    with open(sFileName, newline='') as csvfile:
        oReader = csv.reader(csvfile,
                             delimiter=sDelimiter,
                             quotechar='"')
        for lRow in oReader:
            sName = clean_spaces(clean_spaces(lRow[0])).lower()
            for sNewName in lRow:
                if oConnector.q_get_id_lang_by_name(sNewName) and sNewName:
                    iLang = oConnector.q_get_id_lang(sName)
                    sNewName = clean_spaces(clean_spaces(sNewName)).lower()
                    oConnector.q_insert_lang_var((iLang, sNewName,))


# TODO: It can't work for update ISO 639 and local values
def fill_lang_from_file(sFileName, sDelimiter):
    """ Gets data from file and fills Lang and LangVariant table in database.

        :param sFileName: a string, which contains file patch and name,
                          where is taken data
        :param sDelimiter: a string, which contains delimiter for parsing CSV
        """
    with open(sFileName, newline='') as csvfile:
        oReader = csv.reader(csvfile,
                             delimiter=sDelimiter,
                             quotechar='"')
        for lRow in oReader:
            lValues = []
            for i in lRow:
                lValues.append(clean_spaces(i))

            if oConnector.q_get_id_lang_by_name(lValues[0]) and lValues[0]:
                oConnector.q_insert_lang(tuple(lValues))
                iLang = oConnector.q_get_id_lang(lValues[0])
                oConnector.q_insert_lang_var((iLang, lValues[0],))


# TODO: It can't work for update ISO 639 and local values
def fill_lang_from_wiki(url_wiki_pages):
    """ Gets data from Wikipedia and fills Lang and LangVariant table in DB

        :param url_wiki_pages: string, which contains Wikipedia URL,
                               where is taken data
        """
    bsObj = PerfectSoup(url_wiki_pages)
    lListTR = bsObj.find("table", {"id": "iso-codes"}).findAll("tr")
    for tag in lListTR:
        tagTD = tag.findAll("td")
        if tagTD:
            sName = tagTD[4].get_text()
            sISO639_1 = tagTD[3].get_text().lower()
            sISO639_2 = tagTD[0].get_text().lower().replace("*", "")
            sISO369_3 = tagTD[1].get_text().lower()
            sISO369_5 = tagTD[2].get_text().lower()

            lName = sName.split("; ")
            sFirstName = lName[0]
            sFirstName = clean_spaces(clean_parens(sFirstName)).lower()
            if not oConnector.q_get_id_lang(sFirstName):
                lValues = (sFirstName, sISO639_1,
                           sISO639_2, sISO369_3, sISO369_5,)
                oConnector.q_insert_lang(lValues)

            for Name in lName:
                newName = clean_spaces(clean_parens(Name)).lower()
                if not oConnector.q_get_id_lang_by_name(newName):
                    iID = oConnector.q_get_id_lang(sFirstName)
                    oConnector.q_insert_lang_var((iID, newName))
                    if newName.find(' languages') != -1:
                        newName = newName.replace(" languages", "")
                        oConnector.q_insert_lang_var((iID, newName))


def get_lang_action(oArgs, oParser):
    """ Creates a description of command line arguments for use and help.

        :param oArgs: command line argument value
        :param oParser: argparse object
        """
    if oArgs.langfromwiki and oArgs.langfromfile:
        oParser.print_help()
    else:
        sDelimiter = DELIMITER_CSV
        if oArgs.cleanlangtab:
            oConnector.sql_table_clean(('LangVariant', 'Lang',))
        if oArgs.langfromwiki:
            fill_lang_from_wiki(wiki_pages)
        if oArgs.langfromfile:
            if oArgs.delimiter_csv:
                sDelimiter = oArgs.delimiter_csv
            fill_lang_from_file(oArgs.langfromfile, sDelimiter)
        if oArgs.langvariant:
            if oArgs.delimiter_csv:
                sDelimiter = oArgs.delimiter_csv
            fill_lang_variant(oArgs.langvariant, sDelimiter)
        if oArgs.langtofile:
            if oArgs.delimiter_csv:
                sDelimiter = oArgs.delimiter_csv
            get_lang_to_file(oArgs.langtofile, sDelimiter)
        if oArgs.langvartofile:
            if oArgs.delimiter_csv:
                sDelimiter = oArgs.delimiter_csv
            get_lang_var_to_file(oArgs.langvartofile, sDelimiter)
        if not oArgs.langfromwiki and not oArgs.cleanlangtab and \
                oArgs.langfromfile is None and oArgs.langvariant is None and \
                oArgs.langtofile is None and oArgs.langvartofile is None:
            oParser.print_help()


wiki_pages = "https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes"
db_file = get_file_patch(pach_path(), DB_FILE)
oConnector = SQLmain(db_file)

if __name__ == '__main__':
    sDescription = 'The script allows you to work with tables information ' \
                   'about languages: fill, update and dump.'
    oParser = argparse.ArgumentParser(description=sDescription,
                                      epilog=EPILOG_HELP,
                                      )

    oParser = get_delimiter_csv(oParser)
    oParser = get_lang_argument(oParser)
    oArgs = oParser.parse_args()
    get_lang_action(oArgs, oParser)
