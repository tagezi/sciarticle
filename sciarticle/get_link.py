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

from sciarticle.lib.strmain import get_wiki_url, get_file_patch


def collect_links(lListCategories=''):
    if not lListCategories:
        return

    oSession = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    lURLPages = []
    bIsContinue = True
    for sCategory in lListCategories:
        PARAMS = {
            "action": "query",
            "cmtitle": sCategory,
            "cmtype": "page",
            "cmlimit": "500",
            "list": "categorymembers",
            "format": "json"
        }

        while bIsContinue:
            oRequest = oSession.get(url=URL, params=PARAMS)
            oData = oRequest.json()
            lPages = oData['query']['categorymembers']

            for sPage in lPages:
                if sPage.get('ns') == 0 and\
                        sPage.get('title').find('List') == -1:
                    sURL = get_wiki_url(
                        '/wiki/' + sPage.get('title').replace(' ', '_'))
                    print(sURL)
                    lURLPages.append(sURL)

            try:
                PARAMS.update(oData['continue'])
            except KeyError:
                bIsContinue = False

    return lURLPages


if __name__ == '__main__':
    collect_links()
