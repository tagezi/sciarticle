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

""" The module provides an API for working with html code of Journal and
    Publisher pages on Wikipedia. The main functionality is performed by
    the PerfectSoup class, which inherits its capabilities from BeautifulSoup4.
    The class only parses the html code, and does not process the received data
    itself. If the data needs to be processed, it must be processed in
    the module where the class instance is located.

    Using:
      Foo = PerfectSoup(_URL_of_page_to_journal_or_publisher_in_Wikipedia_)
    """

import errno
import logging
import time
from bs4 import BeautifulSoup
from socket import error as SocketError
from urllib.error import URLError, HTTPError
from urllib.request import urlopen

from sciarticle.lib.strmain import iri_to_uri


def get_column_table(oTableInfo, sTag, sClass):
    """ Processing a table on page passes through column of table which
        usually on the top right on the page.

        :param oTableInfo: A html code of the table.
        :type oTableInfo: bs4.element.Tag
        :param sTag: A html tag which need to find. It can be one from tags:
            'th' for labels of the table, and 'td' for values the table.
        :type sTag: str
        :param sClass: A class which need to be in class field logging the tag.
            For the 'th' tag, it should be 'infobox-label' class, and for
            the 'td', it should be 'infobox-data'.
        :type sClass: str
        :return: list
        """
    lTempColumn = oTableInfo.findAll(sTag, {sClass})
    lColumn = []
    for sCell in lTempColumn:
        lColumn.append(sCell.get_text())

    return lColumn


class PerfectSoup(BeautifulSoup):
    """ Loads HTML at the specified address, gives members which can be used
        like interface for returning values from the Wikipedia pages.
        """
    def __init__(self, sPageURL, **kwargs):
        """ Loads HTML at the specified address, creates BeautifulSoup instance

            :param sPageURL: Contains URL.
            :type sPageURL: str
            :param **kwargs: Don't worry about this.
            """
        try:
            super().__init__(urlopen(iri_to_uri(sPageURL)),
                             "html5lib")
        except (URLError, HTTPError, SocketError) as e:
            logging.exception('An error has occurred: %s.\n'
                              'String of query: %s \n', e, sPageURL)

            if hasattr(e, 'ernno') and e.ernno == errno.ECONNRESET:
                time.sleep(360)
                self.__init__(sPageURL)
            else:
                exit(0)

    def get_link_from_list(self):
        """ Finds all links to articles on a Category page.

        :return: A list URLs
        :rtype: list
        """
        lListURl = self.find("div", {"mw-category"}).findAll("a")
        lURL = []
        for URL in lListURl:
            lURL.append(str(URL.attrs['href']))

        return lURL

    def get_title_h1(self):
        """ Fins h1 tage on the page, and returns text print it.

        :return: Text of page header.
        :rtype: str
        """
        return self.find("h1").get_text()

    def tableinfo_to_dict(self):
        """ Takes info-table from the article page, and returns labels and
            values of the table.

        :return: A dictionary within labels as keys, and values.
        :rtype: dict
        """
        oTableInfo = self.find("table", {"infobox"})

        dTable = {}
        if oTableInfo:
            lListLabel = get_column_table(oTableInfo, "th", "infobox-label")
            lListData = get_column_table(oTableInfo, "td", "infobox-data")
            dTable = dict(zip(lListLabel, lListData))

            sHTML = oTableInfo.find("td", {"infobox-full-data"})
            if sHTML:
                for link in sHTML.findAll("a"):
                    dTable[link.get_text()] = link.attrs['href']

        return dTable

    def get_name_from_bold(self):
        """ Finds on the page bold text in first paragraph and returns it as
            full and short names, if it can find.

        :return: A dictionary with names.
        :rtype: dict
        """
        partHTML = self.find(
            "div", {"class": "mw-parser-output"}
        ).findAll(
            "p", {'class': None})
        lBolsTag = []
        for sPTag in partHTML:
            lBolsTag = sPTag.findAll("b")
            if lBolsTag:
                break

        dNames = {}
        k = int(0)
        for sBold in lBolsTag:
            try:
                if int(k) == int(0):
                    dNames['FullName'] = sBold.get_text()

                elif int(k) == int(1):
                    if len(dNames.get('FullName')) < len(sBold.string):
                        dNames['ShortName'] = dNames.get('FullName')
                        dNames['FullName'] = sBold.string
                    else:
                        dNames['ShortName'] = sBold.string
            except ValueError as e:
                logging.exception('An error has occurred: %s.\n'
                                  'String of query: %s \n', e, sBold)
            k = k + 1

        return dNames


if __name__ == '__main__':
    sURL = 'https://en.wikipedia.org/'
    oPerfectSoup = PerfectSoup(sURL)

    if oPerfectSoup:
        print('I opened the page and created an instance of BeautifulSoup.\n'
              '...And closed it. :)\n'
              'Nothing to do. :р')
