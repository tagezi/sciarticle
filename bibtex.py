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

import bibtexparser

import var
from bibvalue import *
from sqlmain import *
from strmain import *

db_file = get_filename_patch(var.dir_db, var.db_file)

oConnector = Sqlmain(db_file)

with open('bib.backup/mountain01.bib') as bibtex_file:
    oBibDatabase = bibtexparser.load(bibtex_file)

bibtex_file.close()

dBibDB = oBibDatabase.entries_dict
lKeysBibDB = list(oBibDatabase.entries_dict)

i = 0
iCountKeys = len(lKeysBibDB)

while i < iCountKeys:
    dArticle = dBibDB.get(lKeysBibDB[i])
    print(dArticle)
    i += 1

    sRecordType = get_record_type(dArticle)
    sBook = get_book(dArticle)
    sAbstract = get_abstract(dArticle)
    sKeywords = get_keywords(dArticle)
    sAuthors = get_authors(dArticle)
    sLang = get_lang(dArticle)
    sVolume = get_value(dArticle, 'volume')
    sISSN = get_value(dArticle, 'issn')
    sISBN = get_value(dArticle, 'isbn')
    sTitle = get_value(dArticle, 'title')
    sPages = get_value(dArticle, 'pages')
    sURL = get_value(dArticle, 'url')
    sDOI = get_value(dArticle, 'doi')
    sYear = get_value(dArticle, 'year')
    sMonth = get_value(dArticle, 'month')
    sEmail = get_value(dArticle, 'email')
    sAddress = get_value(dArticle, 'address')
    sChapter = get_value(dArticle, 'charter')
    sCrossref = get_value(dArticle, 'crossref')
    sEdition = get_value(dArticle, 'edition')
    sEditor = get_value(dArticle, 'edition')
    sEprint = get_value(dArticle, 'eprint')
    sHowpublished = get_value(dArticle, 'howpublished')
    sInstitution = get_value(dArticle, 'institution')
    sKey = get_value(dArticle, 'key')
    sNumber = get_value(dArticle, 'number')
    sOrganization = get_value(dArticle, 'organization')
    sPublisher = get_value(dArticle, 'publisher')
    sSchool = get_value(dArticle, 'school')
    sSeries = get_value(dArticle, 'series')

    sSQLSearch = oConnector.sql_search(sYear, sTitle, sBook)
    if sSQLSearch is None:
        oConnector.sql_insert(sRecordType, sEprint, sCrossref, sBook, sSeries,
                              sEdition, sVolume, sNumber, sYear, sMonth,
                              sChapter, sPages, sOrganization, sPublisher,
                              sInstitution, sSchool, sAddress, sISSN, sISBN,
                              sTitle, sAbstract, sLang, sEditor, sAuthors,
                              sEmail, sKeywords, sURL, sDOI, sHowpublished,
                              sKey)
        print("данные внесены")
    else:
        print("Статья уже есть в базе")

del oConnector
