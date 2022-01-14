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
""" Fills database by discipline of science journals and books. It takes little
    more garbage than can be hope (See: TODO)
    """
from lib.sqlmain import *
from lib.strmain import *
from lib.perfect_soup import *
import config


# TODO: Parsing of Headers collects string without since for dial
def get_dspln_from_h(sHeader):
    sName = clean_spaces(sHeader.get_text()).replace('[edit]', '').lower()
    sLink = ''
    if sHeader.find('href') != -1 and\
            sHeader.find('http') == -1 and sHeader.find('redlink') != -1:
        sLink = sHeader.get_text()
    if sName.find('outline') == -1 \
            and not oConnector.q_get_id_dspln(sName):
        oConnector.q_insert_dspln((sName, sLink,))


def get_discipline():
    """ Fills database by discipline of science journals and books. """
    bsObj = PerfectSoup(sWikiPages)
    # Take blocks where link lists are.
    lBlock = bsObj.findAll('div', {'class': 'div-col'})
    # TODO: It collects redlink to, but them don't need
    for sBlock in lBlock:
        lTagA = sBlock.findAll('a')
        for sTagA in lTagA:
            sName = clean_spaces(sTagA.get_text()).lower()
            sLink = get_wiki_url(sTagA.attrs['href'])
            if sName.find('outline') == -1\
                    and not oConnector.q_get_id_dspln(sName):
                oConnector.q_insert_dspln((sName, sLink,))

    lHeader2 = bsObj.findAll('h2')
    for sHeader2 in lHeader2:
        get_dspln_from_h(sHeader2)

    lHeader3 = bsObj.findAll('h3')
    for sHeader3 in lHeader3:
        get_dspln_from_h(sHeader3)


if __name__ == '__main__':
    sWikiPages = config.dspln_link
    db_file = get_file_patch(config.db_dir, config.db_file)
    oConnector = SQLmain(db_file)
    get_discipline()
