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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp

from sciarticle.gui.combobox_toolbar import ComboBoxToolBar
from sciarticle.gui.file_dialogs import OpenFileDialog
from sciarticle.gui.help_dialog import About
from sciarticle.gui.setting_dialog import SettingDialog
from sciarticle.gui.tab_widget import CentralTabWidget
from sciarticle.gui.table_view import TableView
from sciarticle.lib.config import ConfigProgram
from sciarticle.lib.sqlmain import SQLmain


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        sTitleProgram = 'Science Article Orderless'
        self.setWindowTitle(sTitleProgram)

        oConfig = ConfigProgram()
        self.sFilePath = oConfig.get_config_value('DB', 'filepath')

        sDefaultTableName = 'Table 1'

        self.oTable = TableView(self, sDefaultTableName)
        self.oCentralTabWidget = CentralTabWidget(self, sDefaultTableName)
        self.oCentralTabWidget.add_tab(self.oTable)
        self.setCentralWidget(self.oCentralTabWidget)

        self.create_actions()
        self.connect_actions()
        self.set_menu_bar()
        self.set_tool_bar()
        self.set_status_bar()

        self.showMaximized()

    def create_actions(self):
        """ Method collect all actions which can do from GUI of program. """
        # File menu
        self.oOpenDB = QAction('Open &DataBase...', self)
        self.oImportCSV = QAction('Import &CSV...')
        self.oImportBibTex = QAction('Import from BibTex...')
        self.oImportJSON = QAction('Import from JSON...')
        self.oImportPubmed = QAction('Import from PubMed nbib...')
        self.oImportEndNote = QAction('Import from EndNote...')
        self.oImportRefMan = QAction('Import from RefMan...')
        self.oPrint = QAction('P&rint...')
        self.oSetting = QAction('&Setting...')
        self.oExitAct = QAction(QIcon.fromTheme('SP_exit'), '&Exit', self)
        self.oExitAct.setShortcut('Ctrl+Q')
        self.oExitAct.setStatusTip('Exit application')

        # Edit
        self.oUndo = QAction('Undo', self)
        self.oUndo.setShortcut('Ctrl+Z')
        self.oRedo = QAction('Redo', self)
        self.oRedo.setShortcut('Ctrl+Z')
        self.oCut = QAction('Cut', self)
        self.oCut.setShortcut('Ctrl+X')
        self.oCopy = QAction('Copy', self)
        self.oCopy.setShortcut('Ctrl+C')
        self.oPaste = QAction('Copy', self)
        self.oPaste.setShortcut('Ctrl+V')
        self.oDelete = QAction('Delete', self)
        self.oDelete.setShortcut('Del')
        self.oSelectAll = QAction('Select All', self)
        self.oSelectAll.setShortcut('Ctrl+A')
        self.oFind = QAction('Find...', self)
        self.oFind.setShortcut('Ctrl+F')
        self.oFindReplace = QAction('Find and Replace...', self)
        self.oFind.setShortcut('Ctrl+F')

        # Help
        self.oOpenHelp = QAction('&Help', self)
        self.oAbout = QAction('&About', self)

    def set_menu_bar(self):
        """ Method create Menu Bar on main window of program GUI. """
        oMenuBar = self.menuBar()

        # Create file menu
        oFileMenu = oMenuBar.addMenu('&File')
        oFileMenu.addAction(self.oOpenDB)
        oFileMenu.addAction(self.oImportCSV)
        oFileMenu.addAction(self.oImportBibTex)
        oFileMenu.addAction(self.oImportJSON)
        oFileMenu.addAction(self.oImportPubmed)
        oFileMenu.addAction(self.oImportEndNote)
        oFileMenu.addAction(self.oImportRefMan)
        oFileMenu.addSeparator()
        oFileMenu.addAction(self.oPrint)
        oFileMenu.addSeparator()
        oFileMenu.addAction(self.oSetting)
        oFileMenu.addSeparator()
        oFileMenu.addAction(self.oExitAct)

        # Create Edit menu
        oEdit = oMenuBar.addMenu('&Edit')
        oEdit.addAction(self.oUndo)
        oEdit.addAction(self.oRedo)
        oEdit.addSeparator()
        oEdit.addAction(self.oCut)
        oEdit.addAction(self.oCopy)
        oEdit.addAction(self.oPaste)
        oEdit.addAction(self.oDelete)
        oEdit.addSeparator()
        oEdit.addAction(self.oFind)
        oEdit.addAction(self.oFindReplace)

        # Create View menu
        oView = oMenuBar.addMenu('&View')

        # Create Tool menu
        oTools = oMenuBar.addMenu('&Tools')

        # Create Help menu
        oHelpMenu = oMenuBar.addMenu('&Help')
        oHelpMenu.addAction(self.oOpenHelp)
        oHelpMenu.addAction(self.oAbout)

    def set_tool_bar(self):
        self.oConnector = SQLmain(str(self.sFilePath))
        self.oComboBoxSets = ComboBoxToolBar(self, self.oConnector)
        self.oToolbar = self.addToolBar('Exit')
        self.oToolbar.addAction(self.oExitAct)
        self.oToolbar.addSeparator()
        self.oToolbar.addWidget(self.oComboBoxSets)

    def set_status_bar(self, sMassage='Ready'):
        """ Method create Status Bar on main window of program GUI. """
        self.oStatusBar = self.statusBar().showMessage(sMassage)

    def connect_actions(self):
        """ It is PyQt5 slots or other words is connecting from GUI element to
            method or function in program. """
        self.oOpenDB.triggered.connect(self.onOpenDB)
        self.oImportCSV.triggered.connect(self.onImportCSV)
        self.oImportBibTex.triggered.connect(self.onImportBibTex)
        self.oImportJSON.triggered.connect(self.onImportJSON)
        self.oImportPubmed.triggered.connect(self.onImportPubmed)
        self.oImportEndNote.triggered.connect(self.onImportEndNote)
        self.oImportRefMan.triggered.connect(self.onImportRefMan)
        self.oSetting.triggered.connect(self.onOpenSetting)
        self.oExitAct.triggered.connect(qApp.quit)
        self.oAbout.triggered.connect(self.onDisplayAbout)

    def onOpenDB(self):
        dParameter = {'name': 'Open Database', 'filter': 'DB file (*.db)'}
        oOpenDBFile = OpenFileDialog(self, dParameter)
        sFileNameDB = oOpenDBFile.exec()
        if sFileNameDB is not None:
            sFilePath = sFileNameDB[0]
            self.oConnector = SQLmain(str(sFilePath))
            self.oComboBoxSets.set_connector(self.oConnector)
            self.oComboBoxSets.update_combobox()

    def onImportCSV(self):
        dParameter = {'name': 'Open CSV File', 'filter': 'CSV file (*.csv)'}
        oOpenCSVFile = OpenFileDialog(self, dParameter)
        self.sFileNameCSV = oOpenCSVFile.exec()
        print(str(self.sFileNameCSV[0]))

    def onImportBibTex(self):
        dParameter = {'name': 'Open BibTex File',
                      'filter': 'BibTex file (*.bib)'}
        oOpenBibTexFile = OpenFileDialog(self, dParameter)
        self.sFileNameBibTex = oOpenBibTexFile.exec()
        oTable = TableView(self, 'Import BibTex')
        self.oCentralTabWidget.add_tab(oTable)
        iIndexTab = self.oCentralTabWidget.count() - 1
        self.oCentralTabWidget.update_tab_name(iIndexTab, 'Import BibTex')
        self.oCentralTabWidget.setCurrentIndex(iIndexTab)

    def onImportJSON(self):
        dParameter = {'name': 'Open JSON File', 'filter': 'JSON file (*.json)'}
        oOpenJSONFile = OpenFileDialog(self, dParameter)
        self.sFileNameJSON = oOpenJSONFile.exec()
        print(str(self.sFileNameJSON[0]))

    def onImportPubmed(self):
        dParameter = {'name': 'Open Pubmed File',
                      'filter': 'NBIB file (*.nbib)'}
        oOpenNBIBFile = OpenFileDialog(self, dParameter)
        self.sFileNameNBIB = oOpenNBIBFile.exec()
        print(str(self.sFileNameNBIB[0]))

    def onImportEndNote(self):
        dParameter = {'name': 'Open EndNote File',
                      'filter': 'EndNote file (*.txt)'}
        oOpenEndNoteFile = OpenFileDialog(self, dParameter)
        self.sFileNameEndNote = oOpenEndNoteFile.exec()
        print(str(self.sFileNameEndNote[0]))

    def onImportRefMan(self):
        dParameter = {'name': 'Open RefMan File',
                      'filter': 'RefMan file (*.txt)'}
        oOpenEndNoteFile = OpenFileDialog(self, dParameter)
        self.sFileNameEndNote = oOpenEndNoteFile.exec()
        print(str(self.sFileNameEndNote[0]))

    def onOpenSetting(self):
        oSettingDialog = SettingDialog(self)
        oSettingDialog.exec_()

    def onDisplayAbout(self):
        """ Method open dialog window with information about the program. """
        oAbout = About(self)
        oAbout.exec_()


if __name__ == '__main__':
    pass
