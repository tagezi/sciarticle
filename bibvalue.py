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

from langcode import get_lang_by_code


def get_record_type(dArticle):
    try:
        sRecordType = dArticle.get('ENTRYTYPE')
        if sRecordType == "article":
            sRecordType = "статья"
        if sRecordType == "inproceedings":
            sRecordType = "глава книги"
        if sRecordType == "book":
            sRecordType = "книга"
        if sRecordType == "booklet":
            sRecordType = "буклет"
        if sRecordType == "conference":
            sRecordType = "тезис конференции"
        if sRecordType == "inbook":
            sRecordType = "глава книги"
        if sRecordType == "incollection":
            sRecordType = "тезис конференции"
        if sRecordType == "manual":
            sRecordType = "техническая документация"
        if sRecordType == "mastersthesis":
            sRecordType = "магистерская дисертация"
        if sRecordType == "misc":
            sRecordType = "что-то странное"
        if sRecordType == "phdthesis":
            sRecordType = "кандидатская дисертация"
        if sRecordType == "proceedings":
            sRecordType = "сборник тезисов конференции"
        if sRecordType == "techreport":
            sRecordType = "отчет организации"
        if sRecordType == "unpublished":
            sRecordType = "рукопись"
    except KeyError:
        sRecordType = ""

    return sRecordType


def get_lang(dArticle):
    try:
        sLang = dArticle.get('lang')
    except KeyError:
        try:
            sLang = dArticle.get('language')
        except KeyError:
            sLang = ""
    else:
        if sLang is None:
            sLang = "английский"

    sLang = get_lang_by_code(sLang)

    return sLang


def get_book(dArticle):
    try:
        sBook = dArticle.get('journal')
    except KeyError:
        try:
            sBook = dArticle.get('booktitle')
        except KeyError:
            sBook = ""

    return sBook


def get_value(dArticle, sAttrebute):
    """

    :param dArticle:
    :param sAttrebute:
    :return:
    """
    try:
        sValue = dArticle.get(sAttrebute)
    except KeyError:
        sValue = ""
    else:
        if sValue is None:
            sValue = ""

    return sValue


def get_keywords(dArticle):
    try:
        sKeywords = dArticle.get('keywords')
        if sKeywords is None:
            sKeywords = ""
        else:
            sKeywords = str(sKeywords).lower()
    except KeyError:
        sKeywords = ""

    return sKeywords


def get_abstract(dArticle):
    try:
        sAbstract = dArticle.get('abstract')
    except KeyError:
        sAbstract = ""
    try:
        sAddendum = dArticle.get('addendum')
    except KeyError:
        sAddendum = ""
    try:
        sAnnote = dArticle.get('annote')
    except KeyError:
        sAnnote = ""
    try:
        sNote = dArticle.get('note')
    except KeyError:
        sNote = ""

    if sAbstract is not None:
        if sNote is not None:
            sAbstract = sAbstract + "\n\n" + sNote
        if sAddendum is not None:
            sAbstract = sAbstract + "\n\n" + sAddendum
        if sAnnote is not None:
            sAbstract = sAbstract + "\n\n" + sAnnote
    else:
        if sNote is not None:
            sAbstract = sNote
            if sAddendum is not None:
                sAbstract = sAbstract + "\n\n" + sAddendum
            if sAnnote is not None:
                sAbstract = sAbstract + "\n\n" + sAnnote
        else:
            if sAddendum is not None:
                sAbstract = sAddendum
                if sAnnote is not None:
                    sAbstract = sAbstract + "\n\n" + sAnnote
            else:
                if sAnnote is not None:
                    sAbstract = sAnnote
                else:
                    sAbstract = ''

    return sAbstract


def get_authors(dArticle):
    """

    :param dArticle:
    :return:
    """
    try:
        sSecondAuthor = ""
        sThirdAuthor = ""
        sAuthor = dArticle.get('author')
    except KeyError:
        sFirstAuthor = ""
        sSecondAuthor = ""
        sThirdAuthor = ""
    else:
        iBool = sAuthor.find(" and ")

        if 1 < iBool:
            lAuthors = sAuthor.split(" and ")
            sFirstAuthor = lAuthors[0]
            sSecondAuthor = lAuthors[1]

            iCountAuthors = len(lAuthors)
            n = 2
            if iCountAuthors > n:
                sThirdAuthor = lAuthors[n]

                n = n + 1
                while iCountAuthors != n:
                    sThirdAuthor = sThirdAuthor + ", " + lAuthors[n]
                    n = n + 1
        else:
            sFirstAuthor = sAuthor

    return sFirstAuthor, sSecondAuthor, sThirdAuthor
