#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
import os

from PyQt5.QtCore import (QDir, QFile, QFileInfo, Qt, pyqtSignal)
from PyQt5.QtWidgets import (QAbstractItemView, QComboBox,
                             QDialog, QFileDialog, QGridLayout, QHBoxLayout, QHeaderView, QLabel,
                             QPushButton, QSizePolicy, QTableWidget,
                             QTableWidgetItem)

BSER_DIR=QDir.currentPath()+"/"
class Select_govern_V2(QDialog):

    signal_finish = pyqtSignal(str,str)

    def __init__(self, parent=None):
        super(Select_govern_V2, self).__init__(parent)


        findButton = self.createButton("&Show", self.find)


        self.filesFoundLabel = QLabel()

        self.createFilesTable()

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(findButton)

        mainLayout = QGridLayout()

        mainLayout.addWidget(self.filesTable, 1, 0, 1, 3)
        mainLayout.addWidget(self.filesFoundLabel, 2, 0)
        mainLayout.addLayout(buttonsLayout, 3, 0, 1, 3)
        self.setLayout(mainLayout)

        self.setWindowTitle("显示控制函数")


    def find(self):
        self.filesTable.setRowCount(0)
        path = os.path.join(BSER_DIR, "govern_fun")
        self.currentDir = QDir(path)

        fileName = "*"
        files = self.currentDir.entryList([fileName],
                                          QDir.Files | QDir.NoSymLinks)
        self.showFiles(files)

    def showFiles(self, files):
        for fn in files:
            file = QFile(self.currentDir.absoluteFilePath(fn))
            size = QFileInfo(file).size()

            fileNameItem = QTableWidgetItem(fn)
            fileNameItem.setFlags(fileNameItem.flags() ^ Qt.ItemIsEditable)
            sizeItem = QTableWidgetItem("%d KB" % (int((size + 1023) / 1024)))
            sizeItem.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

        self.filesFoundLabel.setText("%d file(s) found (Double click on a file to open it)" % len(files))

    def createButton(self, text, member):
        button = QPushButton(text)
        button.clicked.connect(member)
        return button

    def createFilesTable(self):
        self.filesTable = QTableWidget(0, 2)
        self.filesTable.setMaximumWidth(500)
        self.filesTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size"))
        self.filesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)

        self.filesTable.cellActivated.connect(self.openFileOfItem)

    def openFileOfItem(self, row):
        item = self.filesTable.item(row, 0)
        filename=item.text()
        self.signal_finish.emit(str(self.currentDir.absoluteFilePath(item.text())),filename)

