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
""" Module contains links to pages with English-language journals.

    **Function**
    :collect_links: Recursion function that collect links and
            write them to file.
    """
import requests
import time

from sciarticle.lib.strmain import get_wiki_url, get_file_patch


def collect_links():
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "cmtitle": "Category:Academic_publishing_companies",
        "cmtype": "page",
        "cmlimit": "500",
        "list": "categorymembers",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA['query']['categorymembers']

    lURLPages = []
    for page in PAGES:
        if page.get('ns') == 0 and page.get('title').find('List') == -1:
            sURL = get_wiki_url('/wiki/' + page.get('title').replace(' ', '_'))
            lURLPages.append(sURL)

    return lURLPages


if __name__ == '__main__':
    collect_links()
