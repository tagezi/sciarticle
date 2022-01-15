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
from config import COLLECT_URL_LINK, FILES_DIR, WIKI_SOURCE
from lib.perfect_soup import *
from lib.strmain import *


def collect_links(sPageURL):
    """ Recursion function that collect links and write them to file.

    :param sPageURL: A link to page for start collection.
    :return: Nothing.
    """
    bsNewObj = PerfectSoup(sPageURL)
    # The DIV tag within ID "mw-pages" contains links to other pages with
    # English-language journals.
    lNewListURl = bsNewObj.find("div", {"id": "mw-pages"}).findAll("a")

    for URL in lNewListURl:
        if URL.get_text() == "next page":
            sURLtoBook = get_wiki_url(URL.attrs['href'])
            fFileSource.write(sURLtoBook + '\n')
            # Let's not load the servers of our favorite encyclopedia too much.
            time.sleep(1)
            collect_links(sURLtoBook)
            return

    return


if __name__ == '__main__':
    fFileSource = open(get_file_patch(FILES_DIR, WIKI_SOURCE), 'w')
    # Default: https://en.wikipedia.org/wiki/Category:English-language_journals
    sURLtoPage = COLLECT_URL_LINK
    fFileSource.write(sURLtoPage + '\n')
    collect_links(sURLtoPage)

    fFileSource.close()
