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

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTeg(url):
    
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    else:
        print(html)
    #try:
    #   bsObj = BeautifulSoup(html.read(), features="lxml")
     #   titel = bsObj.body.title
    #except AttributeError as e:
    #    return None
    #return titel

print("Старт!")
titel = getTeg("https://citeseerx.ist.psu.edu/search?q=mountaineering&submit.x=16&submit.y=15&sort=rlv&t=doc")
if titel == None:
    print("Titel could not be found")
else:
    print(titel)
