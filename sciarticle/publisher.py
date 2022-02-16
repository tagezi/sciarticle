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
    oPublisherValue = PublisherValue(sURLPage)

    if not oPublisherValue.is_publisher_exist():
        tValues = oPublisherValue.get_publisher()
        iIDPublisher = oConnector.q_insert_publisher(tValues)

        if oPublisherValue.OtherName:
            for sName in oPublisherValue.OtherName:
                oConnector.q_insert_publisher_names((iIDPublisher, sName,))

        if oPublisherValue.FormerName:
            for sName in oPublisherValue.FormerName:
                oConnector.q_insert_publisher_names((iIDPublisher, sName,))

        if oPublisherValue.PublicationTypes:
            for sPType in oPublisherValue.PublicationTypes:
                oConnector.q_insert_publisher_type((iIDPublisher, sPType,))

        if oPublisherValue.sFounder:
            for sFounder in oPublisherValue.sFounder:
                oConnector.q_insert_publisher_founder(
                    (iIDPublisher, sFounder,))

    return oPublisherValue.sFullName


if __name__ == '__main__':
    lListPublisher = [
        'Category:University_presses_of_the_United_States',
        'Category:University_presses_of_the_United_Kingdom',
        'Category:University_presses_of_Switzerland',
        'Category:University_presses_of_Sweden',
        'Category:University_presses_of_Spain',
        'Category:University_presses_of_South_Korea',
        'Category:University_presses_of_Singapore',
        'Category:University_presses_of_Poland',
        'Category:University_presses_of_the_Philippines',
        'Category:University_presses_of_Peru',
        'Category:University_presses_of_New_Zealand',
        'Category:University_presses_of_the_Netherlands',
        'Category:University_presses_of_Lithuania',
        'Category:University_presses_of_Japan',
        'Category:University_presses',
        'Category:University_presses_of_the_United_States',
        'Category:Academic publishing companies']

    lURL = collect_links(lListPublisher)
    for sURL in lURL:
        publisher(sURL)
