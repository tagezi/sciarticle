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
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, \
    QCheckBox, QHBoxLayout, QWidget, QAction, QMenu, QAbstractItemView, \
    QApplication, QShortcut

LastStateRole = Qt.UserRole


class TableView(QTableWidget):
    def __init__(self, oParent, sTableName=None):
        super().__init__(oParent)

        self.lCeckedRow = []
        self.oSelectAll = ''
        self.oUnselectAll = ''
        self.oSaveAsSet = ''
        self.oExportSelecterCSV = ''
        self.oDeleteSelected = ''

        self.sTableName = sTableName
        self.set_table_view()
        self.set_actions()
        self.connection_actions()
        self.show()

    def set_table_view(self):
        self.setColumnCount(14)
        self.setRowCount(5)

        self.setHorizontalHeaderLabels(['Check ', ' ID', 'Type of\nrecord',
                                        'Language', 'Author', 'Title',
                                        'Abstract', 'Keywords', 'DOI',
                                        'Book/Jurnal name', 'Year', 'Volume',
                                        'Number', 'Pages'])

        oFont = QtGui.QFont()
        oFont.setBold(True)

        self.oHHeader = self.horizontalHeader()
        self.oHHeader.setDefaultAlignment(Qt.AlignCenter)
        stylesheet = "QHeaderView::section{margin-left:5px;margin-right:5px;}"
        self.oHHeader.setStyleSheet(stylesheet)
        self.oHHeader.styleSheet()
        self.oHHeader.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(9, QHeaderView.ResizeToContents)
        self.setColumnHidden(1, True)
        self.setColumnWidth(8, 100)
        self.oHHeader.setFont(oFont)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        oVHeader = self.verticalHeader()
        oVHeader.setDefaultAlignment(Qt.AlignCenter)
        oVHeader.setFont(oFont)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        for row in range(len(range(0, self.rowCount()))):
            oWidget = QWidget()
            oCheckBox = QCheckBox()
            oHLayuot = QHBoxLayout(oWidget)
            oHLayuot.addWidget(oCheckBox)
            oHLayuot.setAlignment(Qt.AlignCenter)
            oWidget.setLayout(oHLayuot)
            self.setCellWidget(row, 0, oWidget)

    def set_actions(self):
        self.oSelectAll = QAction('Select all rows')
        self.oUnselectAll = QAction('Unselect all rows')
        self.oSaveAsSet = QAction('Save as set')
        self.oExportSelecterCSV = QAction('Export selected to CSV')
        self.oDeleteSelected = QAction('Delete selected')

    def connection_actions(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenuShow)

        self.oSelectAll.triggered.connect(self.onSelectAll)
        self.oUnselectAll.triggered.connect(self.onUnselectAll)
        self.oSaveAsSet.triggered.connect(self.onSaveAsSet)
        self.oExportSelecterCSV.triggered.connect(self.onExportSelecterCSV)
        self.oDeleteSelected.triggered.connect(self.onDeleteSelected)

        self.cellClicked.connect(self.onCellWasClicked)
        # QShortcut(QKeySequence('Ctrl+C'), self).activated.connect(
        #     self.onKeyPressEvent)
        # QShortcut(QKeySequence('Ctrl+V'), self).activated.connect(
        #     self.onKeyPressEvent)

    def onSelectAll(self):
        for row in range(0, self.rowCount()):
            oWidget = self.cellWidget(row, 0)
            oCheckBox = oWidget.findChildren(QCheckBox)[0]
            iState = oCheckBox.checkState()
            if iState == Qt.Unchecked:
                oCheckBox.setCheckState(Qt.Checked)

    def onUnselectAll(self):
        for row in range(0, self.rowCount()):
            oWidget = self.cellWidget(row, 0)
            oCheckBox = oWidget.findChildren(QCheckBox)[0]
            iState = oCheckBox.checkState()
            if iState == Qt.Checked:
                oCheckBox.setCheckState(Qt.Unchecked)

    def onSaveAsSet(self):
        print('Ok! Saving Done!')

    def onExportSelecterCSV(self):
        print('Ok! Exporting Done!')

    def onDeleteSelected(self):
        print('Ok! Deleting Done!')

    def onContextMenuShow(self, pos):
        menu = QtWidgets.QMenu()
        menu.addAction(self.oSelectAll)
        menu.addAction(self.oUnselectAll)
        menu.addSeparator()
        menu.addAction(self.oSaveAsSet)
        menu.addAction(self.oExportSelecterCSV)
        menu.addAction(self.oDeleteSelected)
        menu.exec_(self.viewport().mapToGlobal(pos))

    def onKeyPressEvent(self, event):
        clipboard = QApplication.clipboard()
        if event.matches(QKeySequence.Copy):
            print('Copy')
            clipboard.setText("some text")
        if event.matches(QKeySequence.Paste):
            print('Paste')

    def onCellWasClicked(self, row, column):
        item = self.itemAt(row, column)
        if item:
            self.ID = item.text()
            print(self.ID)

    def get_checked_row(self):
        for row in range(0, self.rowCount()):
            self.lCeckedRow.append(self.item(row, 0).checkState())

        print(self.lCeckedRow)

    def set_table_content(self, lContent):
        iRow = 0
        iColumns = len(lContent[0]) + 1
        for lRecord in lContent:
            for iColumn in range(1, iColumns):
                sValue = lRecord[iColumn - 1]
                oItem = QTableWidgetItem(str(sValue))
                self.setItem(iRow, iColumn, oItem)
            iRow += 1

        self.oHHeader.setStretchLastSection(False)
        self.setColumnWidth(6, 500)
        self.oHHeader.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(8, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(9, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(10, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(11, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(12, QHeaderView.ResizeToContents)
        self.oHHeader.setSectionResizeMode(13, QHeaderView.ResizeToContents)
        self.resizeRowsToContents()

        self.setWordWrap(True)
        print(self.columnWidth(6))

    def new_table(self, lContent):
        oParent = self.parentWidget()


if __name__ == '__main__':
    pass
