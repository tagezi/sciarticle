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

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, \
    QLineEdit

from sciarticle.gui.file_dialogs import OpenFileDialog
from sciarticle.lib.config import ConfigProgram


class SettingDialog(QDialog):
    def __init__(self, oParent=None):
        super(SettingDialog, self).__init__(oParent)
        self.oConfigProgram = ConfigProgram()
        self.init_UI()
        self.connect_actions()

    def init_UI(self):
        self.setWindowTitle('Setting')
        self.setModal(True)
        self.oButtonApply = QPushButton('Apply', self)
        self.oButtonOk = QPushButton('Ok', self)
        self.oButtonCancel = QPushButton('Cancel', self)
        self.oButtonOpenFile = QPushButton('...', self)
        oVLayout = QVBoxLayout()
        oHLayoutFiledPath = QHBoxLayout()
        oHLayoutButtons = QHBoxLayout()
        sFileNameDB = self.oConfigProgram.get_config_value('DB', 'filepath')
        self.oTextFiled = QLineEdit(sFileNameDB)
        oHLayoutFiledPath.addWidget(self.oTextFiled)
        oHLayoutFiledPath.addWidget(self.oButtonOpenFile)
        oHLayoutButtons.addWidget(self.oButtonApply)
        oHLayoutButtons.addWidget(self.oButtonOk)
        oHLayoutButtons.addWidget(self.oButtonCancel)
        oVLayout.addLayout(oHLayoutFiledPath)
        oVLayout.addLayout(oHLayoutButtons)
        self.setLayout(oVLayout)

    def connect_actions(self):
        self.oButtonOpenFile.clicked.connect(self.onClickOpenFile)
        self.oButtonApply.clicked.connect(self.onClickApply)
        self.oButtonOk.clicked.connect(self.onClickOk)
        self.oButtonCancel.clicked.connect(self.onCancel)

    def onClickOpenFile(self):
        dParameter = {'name': 'Selecting directory',
                      'filter': 'DB file (*.db)'}
        oFileDialog = OpenFileDialog(self, dParameter)
        lFileName = oFileDialog.exec()
        sFileName = ''
        if lFileName:
            sFileName = str(lFileName[0])

        self.oTextFiled.setText(sFileName)

    def onClickApply(self):
        sFileName = self.oTextFiled.text()
        self.oConfigProgram.set_config_value('DB', 'filepath', sFileName)

    def onClickOk(self):
        self.onClickApply()
        self.close()

    def onCancel(self):
        self.close()


if __name__ == '__main__':
    pass
