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

import logging
from bs4 import BeautifulSoup
from urllib.error import URLError, HTTPError
from urllib.request import urlopen


from lib.strmain import iri_to_uri


class PerfectSoup(BeautifulSoup):
    def __init__(self, sPageURL, **kwargs):
        """ Loads HTML at the specified address and gives BeautifulSoup4 object

            :param sURL: a string, which contains URL
            :return: html document
            """
        try:
            super().__init__(urlopen(iri_to_uri(sPageURL)), "html5lib")
        except (URLError, HTTPError) as e:
            logging.exception('An error has occurred: %s.\n'\
                              'String of query: %s \n', e, sPageURL)

    def get_link_from_list(self):
        lListURl = self.find("div", {"mw-category"}).findAll("a")
        lURL = []
        for URL in lListURl:
            lURL.append(str(URL.attrs['href']))

        return lURL

    def get_title_h1(self):
        return self.find("h1").get_text()


if __name__ == '__main__':
    sURL = 'https://en.wikipedia.org/wiki/American_Journal_of_Law_%26_Medicine'
    print(type(PerfectSoup(sURL)))
