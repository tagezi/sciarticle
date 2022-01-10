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

from urllib.request import urlopen
from bs4 import BeautifulSoup
import time


def collect_links(sURL):
    sHTML = urlopen(sURL)
    bsObj = BeautifulSoup(sHTML, "lxml")
    lListURl = bsObj.find("div", {"id": "mw-pages"}).findAll("a")

    for URL in lListURl:
        if URL.get_text() == "next page":
            sURL = "https://en.wikipedia.org" + URL.attrs['href']
            f.write(sURL + '\n')
            print(sURL)
            time.sleep(5)
            collect_links(sURL)
            return

    return


f = open('wikilinks.txt', 'w')
sURL = "https://en.wikipedia.org/w/index.php?title=Category:English" \
       "-language_journals&pagefrom=African+Journal+of+Traditional%2C" \
       "+Complementary+and+Alternative+Medicines#mw-pages"
html = urlopen(sURL)
f.write(sURL + '\n')

bsObj = BeautifulSoup(html, "lxml")
lListURl = bsObj.find("div", {"id": "mw-pages"}).findAll("a")

for URL in lListURl:
    if URL.get_text() == "next page":
        sURL = "https://en.wikipedia.org" + URL.attrs['href']
        f.write(sURL + '\n')
        time.sleep(5)
        print(sURL)
        collect_links(sURL)

f.close()
