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

import logging
from logging import basicConfig, debug, info, warning, error

import config
from lib.strmain import get_filename_patch


def start_login():
    sFilename = get_filename_patch(config.logging_dir, config.log_file)
    return basicConfig(filename=sFilename,
                       filemode='w',
                       format='%(asctime)s %(levelname)s: %(message)s',
                       datefmt='%m.%d.%Y %H:%M:%S',
                       level=logging.DEBUG)