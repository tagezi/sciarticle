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

""" The module contains functions for processing strings: get_value,
    clean_parens, iriToUri
    """
import re
from os.path import splitext, join, normcase
from time import localtime, strftime
from urllib.parse import urlparse, quote, urlunparse


def get_values(sString):
    """ Parses string by dividing it by signs: comma, semicolon, and word 'and'

    :param sString: a String which need to divide and create list
    :return: list of strings
    """
    sString = sString.replace(" and ", ",")
    sString = sString.replace("and ", ",")
    sString = sString.replace("; ", ", ")
    sString = sString.replace(";", ",")
    sString = sString.replace(",,", ",")
    sString = sString.replace("  ", " ")
    sString = sString.replace(", ", ",")
    lString = sString.split(",")

    return lString


def clean_spaces(sString):
    """ Returns a string of non-breaking space (\xa0) and spaces in the start
        and the end of string.

        :param: any string
        :return: the string of non-breaking space (\xa0) and spaces in
                 the start and the end of string.
        """
    return sString.replace("\xa0", " ").strip()


def clean_parens(sString):
    """ Removes parentheses with their contents and removes spaces at
        the beginning and end of the string.

    :param sString: a String in which need to remove parentheses
    :type sString: can be string or int types
    :return: the string without brackets
    :rtype: string
    """
    if type(sString) == int:
        sString = str(sString)

    return re.sub(r'\([^()]*\)', '', sString).strip()


def iri_to_uri(iri):
    """ The function replaces all non-ascii characters to the corresponding
        unicode values and removes end of line


    :param iri: A string with url
    :return: url converted to ascii
    ..:note::: This function does not provide converting for url
               with additional parameters
    """
    iri = re.sub(r'\n|\s+$', '', iri)

    if len(iri) != len(iri.encode()):
        parts = urlparse(iri)
        partUri = quote(parts[2], safe='/')
        listParamUri = (
            parts[0], parts[1], partUri, parts[3], parts[4], parts[5])
        try:
            uri = urlunparse(listParamUri)
        except ValueError as e:
            print("An error has occurred: " + str(e))
            return None

        return uri

    return iri


def get_filename_time(sFileName):
    """ Adds into name of file current date and time

        :param sFileName: a string, which contain patch to file and its name
        :return: the patch to file and file name of the kind
                 patch/filename_YYYYMMDDhhmmss.csv.
                 OS rules are used for the path.
        """
    oTime = localtime()
    sTime = strftime("%Y%m%d%H%M%S", oTime)
    lDirAndFile = splitext(sFileName)

    return lDirAndFile[0] + "_" + sTime + lDirAndFile[-1]


def get_filename_patch(sDir, sFile):
    """ Concatenates file path and file name based on OS rules.

        :return: Patch to file based on OS rules
        """
    return normcase(join(sDir, sFile))


def get_wiki_url(sPartURL):
    return "https://en.wikipedia.org" + sPartURL
