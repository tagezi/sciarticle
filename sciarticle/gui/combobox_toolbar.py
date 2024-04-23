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
from PyQt6.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem, \
    QTabWidget

from config.config import pach_path, DB_FILE
from sciarticle.lib.sqlmain import SQLmain
from sciarticle.lib.strmain import get_file_patch


class ComboBoxToolBar(QComboBox):
    def __init__(self, oParent, oConnector):
        super().__init__(oParent)

        self.oParent = oParent
        self.lAnswerDB = []

        self.currentIndexChanged.connect(self.onSelectNewItem)
        if oConnector:
            self.oConnector = oConnector
            self.update_combobox()
        else:
            self.first_start()

    def first_start(self):
        self.addItem('Not Selected')

    def update_combobox(self):
        self.clear()
        self.addItem('Not Selected')
        self.addItem('All articles')
        oCursor = self.oConnector.select('SetNames', '*')
        self.lAnswerDB = oCursor.fetchall()
        for lRow in self.lAnswerDB:
            self.addItem(lRow[1])

    def update_table_widget(self, sTabName, lListRecords):
        oTabWidget = self.oParent.findChildren(QTabWidget)[0]
        iTabIndex = oTabWidget.currentIndex()
        oTableWidget = self.oParent.findChildren(QTableWidget)[0]
        oTableWidgetItem = oTableWidget.item(0, 2)
        if oTableWidgetItem is None or oTableWidgetItem.text() == '':
            oTabWidget.update_tab_name(iTabIndex, sTabName)
        oTableWidget.set_table_content(lListRecords)

    def set_connector(self, oConnector):
        self.oConnector = oConnector

    def select_all_publications(self, sTabName):
        lPublication = self.oConnector.q_get_publications()
        self.update_table_widget(sTabName, lPublication)

    def onSelectNewItem(self, index):
        sText = self.itemText(index)
        if sText == 'Not Selected':
            return
        elif sText == 'All articles':
            self.select_all_publications('All articles')


if __name__ == '__main__':
    pass
