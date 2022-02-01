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

from logging import basicConfig
import logging
import sys

from config.config import log_path, LOG_FILE
from sciarticle.lib.strmain import get_file_patch


def start_logging():
    sFilename = get_file_patch(log_path(), LOG_FILE)
    basicConfig(filename=sFilename,
                format='%(asctime)s %(levelname)s: %(message)s',
                datefmt='%m.%d.%Y %H:%M:%S',
                level=logging.DEBUG)
    oStream = logging.StreamHandler(sys.stdout)

    return logging.getLogger(__name__).addHandler(oStream)
