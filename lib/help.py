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

""" The module provides functions for displaying help and processing arguments
    """
from config import FILES_DIR, LANG_FILE, LANGVAR_FILE, LANG_BACKUP,\
    LANGVAR_BACKUP, DELIMITER_CSV
from lib.strmain import get_file_patch

sLangFromFile = get_file_patch(FILES_DIR, LANG_FILE)
sLangVariants = get_file_patch(FILES_DIR, LANGVAR_FILE)
sLangToFile = get_file_patch(FILES_DIR, LANG_BACKUP)
sLangVarToFile = get_file_patch(FILES_DIR, LANGVAR_BACKUP)


def get_delimiter_csv(oParser):
    sHelp = 'Allows you to enter delimiter that will be used' \
                'when creating and/or reading a csv-file.'
    oParser.add_argument('--delimiter',
                         dest="delimiter_csv",
                         metavar="CHAR",
                         nargs='?',
                         const=DELIMITER_CSV,
                         type=str,
                         help=sHelp
                         )
    return oParser


def get_lang_argument(oParser):
    """ Creates a description of command line arguments for use and help.

        :param oParser: argparse object
        """
    sHelp = 'Removes all data from all Lang tables.'
    oParser.add_argument('--clean-lang-tab',
                         dest='cleanlangtab',
                         action='store_true',
                         help=sHelp
                         )
    sHelp = 'Takes data from Wikipedia about languages and enters them into ' \
            'table database.\nNote, if you use this argument, ' \
            'the --lang-from-file argument will give an error and print help.'
    oParser.add_argument('--lang-from-wiki',
                         dest='langfromwiki',
                         action='store_true',
                         help=sHelp
                         )
    sHelp = 'Takes data from file about languages and enters them into a ' \
            'table. You can specify the filename into which data placed.\n ' \
            'Note, if you use this argument, the --lang-from-wiki argument ' \
            'will give an error and print a help. '
    oParser.add_argument('--lang-from-file',
                         dest="langfromfile",
                         metavar="FILE",
                         nargs='?',
                         const=sLangFromFile,
                         type=str,
                         help=sHelp
                         )
    sHelp = 'takes data from file about languages variants and enters them ' \
            'into a table. You should specify the filename into which will ' \
            'data placed. '
    oParser.add_argument('--lang-variant',
                         dest="langvariant",
                         metavar="FILE",
                         nargs='?',
                         const=sLangVariants,
                         type=str,
                         help=sHelp
                         )
    sHelp = 'takes data from database about languages and save them into a ' \
            'file. You can specify the filename into which will data placed. '
    oParser.add_argument('--lang-to-file',
                         dest="langtofile",
                         metavar="FILE",
                         nargs='?',
                         const=sLangToFile,
                         type=str,
                         help=sHelp
                         )
    sHelp = 'takes data from database about languages and save them into a ' \
            'file. You can specify the filename into which will data placed. '
    oParser.add_argument('--langvar-to-file',
                         dest="langvartofile",
                         metavar="FILE",
                         nargs='?',
                         const=sLangVariants,
                         type=str,
                         help=sHelp
                         )
    return oParser
