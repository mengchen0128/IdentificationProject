from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialogButtonBox, QDialog


class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("QZS IDENTIFICATION SOFTWARE")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)


        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)