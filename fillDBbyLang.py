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
    You can run this module as a program or use its functionality from the main module.
"""

import argparse
import csv

from sqlmain import *
from strmain import *
from perfectSoup import *
import var


def clean_lang_tables(oConnector):
    """ Cleans LangValiant and Lang tables"""
    lTableClean = ('LangVariant', 'Lang')
    for sTable in lTableClean:
        oConnector.sql_table_clean(sTable)


def get_lang_var_to_file(sFileName, sDelimiter):
    """ Gets data from LangVariant table and creates csv file with it

        :param sFileName: a string, which contains file patch and name, where is saved data
        :param sDelimiter: a string, which contains delimiter for parsing csv file
        """
    sFileName = get_filename_time(sFileName)

    with open(sFileName, 'w', newline='') as csvfile:
        oWriter = csv.writer(csvfile,
                             delimiter=sDelimiter,
                             quotechar='"',
                             quoting=csv.QUOTE_MINIMAL)

        tRow = oConnector.sql_get_all('LangVariant')
        lRow = ""
        lValue = []
        for rRow in tRow:
            if rRow[1] != lRow:
                if lRow:
                    oWriter.writerow(lValue)
                    lValue = []
                lRow = rRow[1]
                lValue.append(rRow[2])
            else:
                lValue.append(rRow[2])


def get_lang_to_file(sFileName, sDelimiter):
    """ Gets data from Lang table and creates csv file with it

        :param sFileName: a string, which contains file patch and name, where is saved data
        :param sDelimiter: a string, which contains delimiter for parsing csv file
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

        :param sFileName: a string, which contains file patch and name, where is taken data
        :param sDelimiter: a string, which contains delimiter for parsing csv file
        """
    print(sDelimiter)
    with open(sFileName, newline='') as csvfile:
        oReader = csv.reader(csvfile,
                             delimiter=sDelimiter,
                             quotechar='"')
        for lRow in oReader:
            sName = clean_spaces(lRow[0])
            for sRow in lRow:
                iLang = oConnector.get_id_lang_by_name(sRow)
                if iLang == 0 and sRow:
                    iLang = oConnector.sql_search_id('Lang', 'id_lang', 'en_name', (sName,))
                    sOtherName = clean_spaces(sRow)
                    oConnector.sql_insert('LangVariant', 'id_lang, lang', (iLang, sOtherName,))


def fill_lang_from_file(sFileName, sDelimiter):
    """ Gets data from file and fills Lang and LangVariant table in database

        :param sFileName: a string, which contains file patch and name, where is taken data
        :param sDelimiter: a string, which contains delimiter for parsing csv file
        """
    with open(sFileName, newline='') as csvfile:
        oReader = csv.reader(csvfile,
                             delimiter=sDelimiter,
                             quotechar='"')
        for lRow in oReader:
            lValues = []
            for i in lRow:
                lValues.append(clean_spaces(i))

            iLang = oConnector.get_id_lang_by_name(lValues[0])
            if iLang == 0 and lValues[0]:
                sColumns = "en_name, iso_639_1, iso_639_2, iso_639_3, iso_639_5, gost_7_75_lat, gost_7_75_rus, d_code"
                oConnector.sql_insert('Lang', sColumns, lValues)
                iLang = oConnector.sql_search_id('Lang', 'id_lang', 'en_name', (lValues[0],))
                oConnector.sql_insert('LangVariant', 'id_lang, lang', (iLang, lValues[0],))


def fill_lang_from_wiki(url_wiki_pages):
    """ Gets data from Wikipedia and fills Lang and LangVariant table in database

        :param url_wiki_pages: a string, which contains Wikipedia URL, where is taken data
        """
    bsObj = get_html(url_wiki_pages)
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
            i = 0
            for Name in lName:
                Name = clean_parens(Name)
                if i == 0:
                    sName = Name
                    sColumns = "en_name, iso_639_1, iso_639_2, iso_639_3, iso_639_5"
                    lValues = (Name, sISO639_1, sISO639_2, sISO369_3, sISO369_5,)
                    oConnector.sql_insert('Lang', sColumns, lValues)

                iID = oConnector.sql_search_id('Lang', 'id_lang', 'en_name', (sName,))
                if Name.find(',') != -1 and Name.find("Nynorsk") == -1 and Name.find("Norwegian") == -1:
                    templName = Name.split(", ")
                    newName = templName[1] + " " + templName[0]
                    oConnector.sql_insert('LangVariant', 'id_lang, lang', (iID, newName))

                if Name.find(' languages') != -1:
                    newName = Name.replace(" languages", "")
                    oConnector.sql_insert('LangVariant', 'id_lang, lang', (iID, newName))

                oConnector.sql_insert('LangVariant', 'id_lang, lang', (iID, Name))

                i = i + 1

            print("Lang name:" + sName + "\nsISO639_1: " + sISO639_1 + "\nsISO639_2: " +
                  sISO639_2 + "\nsISO369_3: " + sISO369_3 + "\nsISO369_5: " + sISO369_5 + "\n")


def get_lang_argument(oParser):
    """ Creates a description of command line arguments for use and help.

        :param oParser: a argparse object
        """
    oParser.add_argument('--clean-lang-tab',
                         dest='cleanlangtab',
                         action='store_true',
                         help='Removes all data from all Lang tables.'
                         )
    oParser.add_argument('--lang-from-wiki',
                         dest='langfromwiki',
                         action='store_true',
                         help='takes data from Wikipedia about languages and enters them into a table.'
                         )
    oParser.add_argument('--lang-from-file',
                         dest="langfromfile",
                         metavar="FILE",
                         nargs='?',
                         const=sLangFromFile,
                         type=str,
                         help='takes data from file about languages and enters them into a table. You can specify '
                              'the filename into which will data placed.'
                         )
    oParser.add_argument('--lang-variant',
                         dest="langvariant",
                         metavar="FILE",
                         nargs='?',
                         const=sLangVariants,
                         type=str,
                         help='takes data from file about languages variants and enters them into a table. You '
                              'shoud specify the filename into which will data placed.'
                         )
    oParser.add_argument('--lang-to-file',
                         dest="langtofile",
                         metavar="FILE",
                         nargs='?',
                         const=sLangToFile,
                         type=str,
                         help='takes data from database about languages and save them into a file. You can specify '
                              'the filename into which will data placed.'
                         )
    oParser.add_argument('--langvar-to-file',
                         dest="langvartofile",
                         metavar="FILE",
                         nargs='?',
                         const=sLangVariants,
                         type=str,
                         help='takes data from database about languages and save them into a file. You can specify '
                              'the filename into which will data placed.'
                         )


def get_action_fo_lang(oArgs, oParser):
    """ Creates a description of command line arguments for use and help.

        :param oArgs: command line argument value
        :param oParser: a argparse object
        """
    if oArgs.langfromwiki and oArgs.langfromfile:
        print("You mast choose from --lang-from-wiki or --lang-from-file. Read halp.\n")
        oParser.print_help()
    else:
        sDelimiter = '|'
        if oArgs.cleanlangtab:
            clean_lang_tables(oConnector)
        if oArgs.langfromwiki:
            fill_lang_from_wiki(wiki_pages)
        if oArgs.langfromfile:
            if oArgs.delimiter:
                sDelimiter = oArgs.delimiter
            fill_lang_from_file(oArgs.langfromfile, sDelimiter)
        if oArgs.langvariant:
            if oArgs.delimiter:
                sDelimiter = oArgs.delimiter
            fill_lang_variant(oArgs.langvariant, sDelimiter)
        if oArgs.langtofile:
            if oArgs.delimiter:
                sDelimiter = oArgs.delimiter
            get_lang_to_file(oArgs.langtofile, sDelimiter)
        if oArgs.langvartofile:
            if oArgs.delimiter:
                sDelimiter = oArgs.delimiter
            get_lang_var_to_file(oArgs.langvartofile, sDelimiter)
        if not oArgs.langfromwiki and oArgs.langfromfile is None and oArgs.langvariant is None and \
                oArgs.langtofile is None and oArgs.langvartofile is None:
            oParser.print_help()


wiki_pages = "https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes"
db_file = get_filename_patch(var.dir_db, var.db_file)
sLangFromFile = get_filename_patch(var.dir_files, var.lang_file)
sLangVariants = get_filename_patch(var.dir_files, var.lang_var_file)
sLangToFile = get_filename_patch(var.dir_files, var.lang_backup)
sLangVarToFile = get_filename_patch(var.dir_files, var.lang_var_backup)
oConnector = Sqlmain(db_file)

if __name__ == '__main__':
    oParser = argparse.ArgumentParser(description='The script allows you to work with tables information about '
                                                  'languages: fill, update and dump.',
                                      epilog='(c) tagezi. Licensed under the GPL 3.0',
                                      )
    oParser.add_argument('--delimiter',
                         dest="delimiter",
                         nargs='?',
                         const="|",
                         type=str,
                         help='Allows you to enter a delimiter that will be used'
                              'when creating and/or reading a csv-file.'
                         )
    get_lang_argument(oParser)
    oArgs = oParser.parse_args()
    get_action_fo_lang(oArgs, oParser)
