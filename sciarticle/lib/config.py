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

from configparser import ConfigParser, NoSectionError


class ConfigProgram(ConfigParser):
    def __init__(self):
        super().__init__()

        self.sFilePath = '../config.ini'
        self.read(self.sFilePath)
        self.lSections = self.sections()

    def get_config_value(self, sSection, sOptions):
        return self.get(sSection, sOptions)

    def set_config_value(self, sSection, sOptions, sValue=''):
        try:
            self.set(sSection, sOptions, sValue)
        except NoSectionError:
            self.add_section(sSection)
            self.set(sSection, sOptions, sValue)

        with open(self.sFilePath, 'w') as fConfigFile:
            self.write(fConfigFile)


if __name__ == '__main__':
    pass
