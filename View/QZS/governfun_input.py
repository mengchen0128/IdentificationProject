import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox

from View.QZS.Governfun_code_editor import QCodeEditor
BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class governfun_input(QWidget):

    def __init__(self, para,*args, **kwargs):
        super(governfun_input, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.editor = QCodeEditor()  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)
        self.para=para
        self.resize(400, 300)
        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addLayout(self.create_button())

        layout.addWidget(self.editor)


        self.setLayout(layout)

    def create_button(self):

        button_layout=QHBoxLayout()

        open_file_button=QPushButton("打开")

        open_file_button.setIcon(QtGui.QIcon(os.path.join('images', 'open_file.png')))
        open_file_button.setIconSize(QtCore.QSize(24,24))
        open_file_button.setMaximumWidth(64)


        save_file_button=QPushButton("保存")
        save_file_button.setIcon(QtGui.QIcon(os.path.join('images', 'open_file.png')))
        save_file_button.setIconSize(QtCore.QSize(24,24))
        save_file_button.setMaximumWidth(64)


        saveas_file_button=QPushButton("另存为")
        saveas_file_button.setIcon(QtGui.QIcon(os.path.join('images', 'open_file.png')))
        saveas_file_button.setIconSize(QtCore.QSize(24,24))
        saveas_file_button.setMaximumWidth(64)



        open_file_button.clicked.connect(lambda:self.file_open(self.para))

        save_file_button.clicked.connect(lambda :self.file_save(self.para))

        saveas_file_button.clicked.connect(lambda :self.file_saveas(self.para))




        button_layout.addWidget(open_file_button)
        button_layout.addWidget(save_file_button)
        button_layout.addWidget(saveas_file_button)
        button_layout.addStretch()



        return button_layout



    def file_open(self,para):

        if para==0:
            path = os.path.join(BSER_DIR, 'govern_fun/GoverningFunction.py')
        elif para==1:
            path = os.path.join(BSER_DIR, 'govern_fun/GoverningGradient_mu.py')
        else :
            path = os.path.join(BSER_DIR, 'govern_fun/GoverningGradient_x.py')


        try:
            with open(path, 'rU') as f:
                    text = f.read()

        except Exception as e:
                self.dialog_critical(str(e))

        else:
            self.path = path
            self.editor.setPlainText(text)

    def file_save(self,para):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas(para)

        self._save_to_path(self.path)

    def file_saveas(self,para):
        if para == 0:
            path = os.path.join(BSER_DIR, 'govern_fun/GoverningFunction.py')
        elif para == 1:
            path = os.path.join(BSER_DIR, 'govern_fun/GoverningGradient_mu.py')
        else:
            path = os.path.join(BSER_DIR, 'govern_fun/GoverningGradient_x.py')

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
