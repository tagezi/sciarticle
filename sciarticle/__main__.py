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

import argparse
import sys
from PyQt6.QtWidgets import QApplication

from lang import get_lang_argument, get_lang_action
from sciarticle.gui.main_window import MainWindow


def main(oArgs, oParser):
    if not oArgs.langfromwiki and not oArgs.cleanlangtab and \
                oArgs.langfromfile is None and oArgs.langvariant is None and \
                oArgs.langtofile is None and oArgs.langvartofile is None:
        app = QApplication(sys.argv)
        sheet = MainWindow()
        sys.exit(app.exec())
    else:
        get_lang_action(oArgs, oParser)


if __name__ == '__main__':
    sDis = 'The script allows you to work with tables information about '\
           'languages: fill, update and dump.'
    sEpilog = '(c) tagezi. Licensed under the GPL 3.0'
    oParser = argparse.ArgumentParser(description=sDis,
                                      epilog=sEpilog,
                                      )
    sHelp = 'Allows you to enter a delimiter that will be used when creating '\
            'and/or reading a csv-file.'
    oParser.add_argument('--delimiter',
                         dest="delimiter",
                         nargs='?',
                         const="|",
                         type=str,
                         help=sHelp
                         )
    get_lang_argument(oParser)
    oArgs = oParser.parse_args()
    main(oArgs, oParser)
