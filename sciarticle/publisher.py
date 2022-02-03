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

from sciarticle.get_link import collect_links
from config.config import pach_path, DB_FILE
from sciarticle.lib.publishermain import PublisherValue
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import get_file_patch


oConnector = SQLmain(get_file_patch(pach_path(), DB_FILE))


def publisher(sURLPage):
    print(sURLPage)
    oPublisherValue = PublisherValue(sURLPage)

    if not oPublisherValue.is_publisher_exist():
        tValues = oPublisherValue.get_publisher()
        print(tValues)
        iIDPublisher = oConnector.q_insert_publisher(tValues)

        if oPublisherValue.OtherName:
            for sName in oPublisherValue.OtherName:
                print((iIDPublisher, sName,))
                oConnector.q_insert_publisher_names((iIDPublisher, sName,))

        if oPublisherValue.FormerName:
            for sName in oPublisherValue.FormerName:
                print((iIDPublisher, sName,))
                oConnector.q_insert_publisher_names((iIDPublisher, sName,))

        if oPublisherValue.PublicationTypes:
            for sPType in oPublisherValue.PublicationTypes:
                print((iIDPublisher, sPType,))
                oConnector.q_insert_publisher_type((iIDPublisher, sPType,))

        if oPublisherValue.sFounder:
            for sFounder in oPublisherValue.sFounder:
                print((iIDPublisher, sFounder,))
                oConnector.q_insert_publisher_founder(
                    (iIDPublisher, sFounder,))


if __name__ == '__main__':
    lURL = collect_links()
    for sURL in lURL:
        publisher(sURL)
