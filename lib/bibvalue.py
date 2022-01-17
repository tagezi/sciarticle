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

from config import DB_DIR, DB_FILE
from lib.sqlmain import *
from lib.strmain import *

logging = start_logging()


def bibtex_load(fBibtexFile):
    return bibtexparser.load(fBibtexFile)


def get_bibtex_record(dArticle, sAttribute):
    try:
        sRecord = dArticle.get(sAttribute)
    except KeyError as e:
        logging.exception('An error has occurred: %s.\n'
                          'Attribute: %s \n', e, sAttribute)
        return None

    return sRecord


def get_bibtex_record_type(dArticle):
    return get_bibtex_record(dArticle, 'ENTRYTYPE')


# In fact, there are many ways to separate authors, shorten their names, etc.
def get_bibtex_authors(dArticle):
    return get_values(get_bibtex_record(dArticle, 'author'))


# Almost always only one language is used, but BASE sometimes has entries
# even in three languages
def get_bibtex_lang(dArticle):
    try:
        sLang = dArticle.get('lang')
    except KeyError as e:
        logging.exception('An error has occurred: %s.\n'
                          'Attribute: %s \n', e, 'lang')
        try:
            sLang = dArticle.get('language')
        except KeyError as e:
            sLang = None
            logging.exception('An error has occurred: %s.\n'
                              'Attribute: %s \n', e, 'language')
    if sLang is None:
        return None

    return tuple(get_values(sLang),)


def get_bibtex_book(dArticle):
    try:
        sBook = dArticle.get('journal')
    except KeyError as e:
        logging.exception('An error has occurred: %s.\n'
                          'Attribute: %s \n', e, 'journal')
        try:
            sBook = dArticle.get('booktitle')
        except KeyError as e:
            logging.exception('An error has occurred: %s.\n'
                              'Attribute: %s \n', e, 'booktitle')
            return None

    return sBook


def get_bibtex_value(dArticle, sAttribute):
    try:
        sValue = dArticle.get(sAttribute)
    except KeyError as e:
        logging.exception('An error has occurred: %s.\n'
                          'Attribute: %s \n', e, sAttribute)
        return None

    if sValue is None:
        return None

    return sValue


def get_bibtex_keywords(dArticle):
    try:
        sKeywords = dArticle.get('keywords')
    except KeyError as e:
        sKeywords = None
        logging.exception('An error has occurred: %s.\n'       
                          'Attribute: %s \n', e, 'keywords')
    if sKeywords is None:
        return None

    return tuple(get_values(str(sKeywords).lower()),)


def get_bibtex_abstract(dArticle):
    try:
        sAbstract = dArticle.get('abstract')
    except KeyError:
        sAbstract = ""
    try:
        sAddendum = dArticle.get('addendum')
    except KeyError:
        sAddendum = ""
    try:
        # An annotation for annotated bibliography styles (not typical)
        sAnnote = dArticle.get('annote')
    except KeyError:
        sAnnote = ""
    try:
        # Miscellaneous extra information
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


class BibtexValue:

    def __init__(self, dArticle):
        self.oConnector = SQLmain(get_file_patch(DB_DIR, DB_FILE))

        self.sAbstract = get_bibtex_abstract(dArticle)
        # Publisher's address (usually just the city, but can be the full
        # address for lesser-known publishers)
        self.sAddress = get_bibtex_value(dArticle, 'address')
        # The name(s) of the author(s) (in the case of more than one author,
        # usually separated by and. But, there are issue...)
        self.lAuthors = get_bibtex_authors(dArticle)
        # The title of the book, if only part of it is being or
        # the journal or magazine the work was published in
        self.sBook = get_bibtex_book(dArticle)
        # The chapter number
        self.sChapter = get_bibtex_value(dArticle, 'charter')
        # The key of the cross-referenced entry
        self.sCrossref = get_bibtex_value(dArticle, 'crossref')
        # digital object identifier
        self.sDOI = get_bibtex_value(dArticle, 'doi')
        # The edition of a book, long form (such as "First" or "Second")
        self.sEdition = get_bibtex_value(dArticle, 'edition')
        # The name(s) of the editor(s)
        self.sEditor = get_bibtex_value(dArticle, 'edition')
        # The email of the author(s)
        self.sEmail = get_bibtex_value(dArticle, 'email')
        self.sEprint = get_bibtex_value(dArticle, 'eprint')
        # How it was published, if the publishing method is nonstandard
        self.sHowPublished = get_bibtex_value(dArticle, 'howpublished')
        # The institution that was involved in the publishing, but not
        # necessarily the publisher
        self.sInstitution = get_bibtex_value(dArticle, 'institution')
        self.sISBN = get_bibtex_value(dArticle, 'isbn')
        self.sISSN = get_bibtex_value(dArticle, 'issn')
        # A hidden field used for specifying or overriding the alphabetical
        # order of entries (when the "author" and "editor" fields are
        # missing). This is very different from the key (mentioned  just
        # after this list) that is used to cite or cross-reference the entry.
        self.sKey = get_bibtex_value(dArticle, 'key')
        # Keywords for the paper
        self.lKeywords = get_bibtex_keywords(dArticle)
        # Language(s) in which the paper is written
        self.lLang = get_bibtex_lang(dArticle)
        # The month of publication (or, if unpublished, the month of creation)
        self.sMonth = get_bibtex_value(dArticle, 'month')
        # The "(issue) number" of a journal, magazine, or tech-report. Note
        # that this is not the "article number" assigned by some journals.
        self.sNumber = get_bibtex_value(dArticle, 'number')
        # The conference sponsor
        self.sOrganization = get_bibtex_value(dArticle, 'organization')
        # Page numbers, separated either by commas or double-hyphens.
        self.sPages = get_bibtex_value(dArticle, 'pages')
        # The publisher's name
        self.sPublisher = get_bibtex_value(dArticle, 'publisher')
        # The field overriding the default type of publication
        self.sRecordType = get_bibtex_record_type(dArticle)
        # The school where the thesis was written
        self.sSchool = get_bibtex_value(dArticle, 'school')
        # The series of books the book was published in
        self.sSeries = get_bibtex_value(dArticle, 'series')
        # The title of the work
        self.sTitle = get_bibtex_value(dArticle, 'title')
        # URL(s) where paper stored
        self.lURL = get_bibtex_value(dArticle, 'url')
        # The volume of a journal or multi-volume book
        self.sVolume = get_bibtex_value(dArticle, 'volume')
        # The year of publication (or, if unpublished, the year of creation)
        self.sYear = get_bibtex_value(dArticle, 'year')

    def is_there_book(self):
        return self.oConnector.q_get_id_publication((self.sTitle,
                                                     self.sYear, self.sBook,))

    def get_publication(self):
        iIDType = self.oConnector.q_get_id_publ_type(self.sRecordType)
        iIDBook = self.oConnector.q_get_id_book(self.sBook)
        if not iIDBook:
            iIDBook = self.oConnector.q_insert_book((self.sBook, self.sISBN,))

        tValues = (iIDType, self.sTitle, self.sAbstract, self.sDOI, iIDBook,
                   self.sYear, self.sVolume, self.sNumber, self.sPages)
        return tuple(tValues)
