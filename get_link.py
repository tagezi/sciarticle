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

import time

import config
from lib.perfect_soup import *
from lib.strmain import *


def collect_links(sPageURL):
    bsNewObj = PerfectSoup(sPageURL)
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
    fFileSource = open(get_filename_patch(config.files_dir,
                                          config.wiki_source), 'w')
    sURLtoPage = 'https://en.wikipedia.org/' \
                 'wiki/Category:English-language_journals'
    collect_links(sURLtoPage)

    fFileSource.close()
