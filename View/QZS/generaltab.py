from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout


class GeneralTab(QWidget):
    def __init__(self, url,parent=None):
        super(GeneralTab, self).__init__(parent)

        self.textEdit = QTextEdit(self)

        self.textEdit.setText(open(url, 'rb').read().decode())
        mainLayout = QVBoxLayout()

        hlayout=QHBoxLayout()

        self.button_save=QPushButton("保存")
        self.button_cancel=QPushButton("取消")

        hlayout.addWidget(self.button_save)
        hlayout.addWidget(self.button_cancel)
        hlayout.addStretch()
        mainLayout.addWidget(self.textEdit)
        mainLayout.addLayout(hlayout)

        self.setLayout(mainLayout)

    def setText(self, text):
        self.textEdit.setPlainText(text)