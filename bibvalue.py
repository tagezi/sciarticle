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

from strmain import *


def get_record(dArticle, sAtribut):
    try:
        sRecord = dArticle.get(sAtribut)
    except KeyError as e:
        print("Error: " + str(e))
        return None

    return sRecord


def get_record_type(dArticle):
    return get_record(dArticle, 'ENTRYTYPE')


def get_authors(dArticle):
    return get_record(dArticle, 'author')


def get_lang(dArticle):
    try:
        sLang = dArticle.get('lang')
    except KeyError as e:
        print("Error: " + str(e))
        try:
            sLang = dArticle.get('language')
        except KeyError as e:
            print("Error: " + str(e))
            return None

    if sLang is None:
        return None

    return get_values(sLang)


def get_book(dArticle):
    try:
        sBook = dArticle.get('journal')
    except KeyError as e:
        print("Error: " + str(e))
        try:
            sBook = dArticle.get('booktitle')
        except KeyError as e:
            print("Error: " + str(e))
            return None

    return sBook


def get_value(dArticle, sAttrebute):
    try:
        sValue = dArticle.get(sAttrebute)
    except KeyError as e:
        print("Error: " + str(e))
        return None

    if sValue is None:
        return None

    return sValue


def get_keywords(dArticle):
    try:
        sKeywords = dArticle.get('keywords')
    except KeyError as e:
        print("Error:" + str(e))
        return None

    if sKeywords is None:
        return None

    return get_values(str(sKeywords).lower())


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
