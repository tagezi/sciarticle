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

from scholarly import scholarly

# search_query = scholarly.search_pubs('снегоступинг')
# scholarly.pprint(next(search_query))

search_query = scholarly.search_pubs('backpacking')
dic1 = next(search_query)
dic2 = dic1.get('bib')
print(dic2)
print(dic2.get('title'))
print(dic2.get('author')[0])
print(dic2.get('pub_year'))
