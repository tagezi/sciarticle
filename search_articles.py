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

from scholarly import scholarly

#search_query = scholarly.search_pubs('снегоступинг')
#scholarly.pprint(next(search_query))

search_query = scholarly.search_pubs('backpacking')
dic1 = next(search_query)
dic2 = dic1.get('bib')
print(dic2)
print(dic2.get('title'))
print(dic2.get('author')[0])
print(dic2.get('pub_year'))



#{'author_id': [''],
# 'bib': {'abstract': 'Backpacking, a relatively little studied form of '
#                     'tourism, is a rapidly expanding phenomenon. This article '
#                     'follows the transition from the tramp to the drifter, '
#                     'and from the latter to the contemporary backpacker, and '
#                     'points to the diversity within this general category of '
#                     'tourists',
#         'author': ['E Cohen'],
#         'pub_year': '2003',
#         'title': 'Backpacking: Diversity and change',
#         'venue': 'Journal of tourism and cultural change'},
# 'citedby_url': '/scholar?cites=15036604105184777659&as_sdt=5,33&sciodt=0,33&hl=en',
# 'filled': False,
# 'gsrank': 1,
# 'num_citations': 515,
# 'pub_url': 'https://www.tandfonline.com/doi/abs/10.1080/14766820308668162',
# 'source': 'PUBLICATION_SEARCH_SNIPPET',
# 'url_add_sclib': '/citations?hl=en&xsrf=&continue=/scholar%3Fq%3Dbackpacking%26hl%3Den%26as_sdt%3D0,33&citilm=1&update_op=library_add&info=uxW4LcS_rNAJ&ei=NPWhYdiLHuPUsQKZ27PQDg&json=',
# 'url_related_articles': '/scholar?q=related:uxW4LcS_rNAJ:scholar.google.com/&scioq=backpacking&hl=en&as_sdt=0,33',
# 'url_scholarbib': '/scholar?q=info:uxW4LcS_rNAJ:scholar.google.com/&output=cite&scirp=0&hl=en'}
