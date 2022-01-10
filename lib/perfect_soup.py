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

from urllib.error import URLError, HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup

from lib.strmain import iri_to_uri


def get_html(sURL):
    """ Loads HTML at the specified address and gives BeautifulSoup4 object

        :param sURL: a string, which contains URL
        :return: html document
        """
    try:
        html = urlopen(iri_to_uri(sURL))
    except (URLError, HTTPError) as e:
        print("An error has occurred: " + str(e) + "\nURL: " + str(sURL))
        return None

    return BeautifulSoup(html, "html5lib")


if __name__ == '__main__':
    sURL = 'https://en.wikipedia.org/wiki/American_Journal_of_Law_%26_Medicine'
    print(type(get_html(sURL)))
