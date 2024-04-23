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

from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout


class CentralTabWidget(QTabWidget):
    def __init__(self, oParent, sName):
        super().__init__(oParent)
        self.oLayout = QVBoxLayout(self)
        self.sName = sName

        self.setMovable(True)
        self.setTabPosition(QTabWidget.TabPosition.South)
        # self.setTabShape(QTabWidget.TabPosition.Triangular)

        # Add tabs to widget
        self.oLayout.addWidget(self)
        self.setLayout(self.oLayout)

    def add_tab(self, oWidget, sName=''):
        if not sName:
            sName = self.sName
        # Initialize tab screen
        self.oTab = QWidget()

        # Add tabs
        self.addTab(self.oTab, sName)

        # Create first tab
        self.oTab.layout = QVBoxLayout(self)
        self.oTab.layout.addWidget(oWidget)
        self.oTab.setLayout(self.oTab.layout)

        iIndexTab = self.count() - 1
        self.update_tab_name(iIndexTab, sName)
        self.setCurrentIndex(iIndexTab)

    def update_tab_name(self, iTabIndex=0, sTabName='Table 1'):
        self.setTabText(iTabIndex, sTabName)


if __name__ == '__main__':
    pass
