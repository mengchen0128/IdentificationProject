from PyQt5.QtWidgets import QWizard, QLabel, QVBoxLayout, QWizardPage, QGroupBox, QGridLayout

from View.QZS.governfun_input import governfun_input


class ClassWizard(QWizard):
    def __init__(self, parent=None):
        super(ClassWizard, self).__init__(parent)

        self.addPage(IntroPage())
        self.addPage(ClassInfoPage())
        self.addPage(CodeStylePage())
        self.addPage(OutputFilesPage())
        self.addPage(ConclusionPage())

        self.setWindowTitle("控制方程输入")
        self.resize(600,500)



    def accept(self):





        super(ClassWizard, self).accept()

class IntroPage(QWizardPage):
    def __init__(self, parent=None):
        super(IntroPage, self).__init__(parent)

        self.setTitle("Introduction")


        label = QLabel("请按步骤输入控制方程,需要对python语法有一定了解！")
        label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class ClassInfoPage(QWizardPage):
    def __init__(self, parent=None):
        super(ClassInfoPage, self).__init__(parent)

        self.setTitle("GoverningFunction")
        self.setSubTitle("Specify basic information about the class for "
                "which you want to generate skeleton source code files.")

        groupBox = QGroupBox("C&onstructor")
        groupBoxLayout = QVBoxLayout()

        #text_govern=notepad()
        governing_function_textedit = governfun_input(0)


        groupBoxLayout.addWidget(governing_function_textedit)

        groupBox.setLayout(groupBoxLayout)

        layout = QGridLayout()
        layout.addWidget(groupBox, 0, 0)



        self.setLayout(layout)




class CodeStylePage(QWizardPage):
    def __init__(self, parent=None):
        super(CodeStylePage, self).__init__(parent)

        self.setTitle("GoverningGradient_mu")
        self.setSubTitle("Choose the formatting of the generated code.")

        groupBox = QGroupBox("C&onstructor")
        groupBoxLayout = QVBoxLayout()

        text_govern_mu = governfun_input(1)
        governing_gradient_mu_textedit = text_govern_mu


        groupBoxLayout.addWidget(governing_gradient_mu_textedit)

        groupBox.setLayout(groupBoxLayout)

        layout = QGridLayout()
        layout.addWidget(groupBox, 0, 0)


        self.setLayout(layout)




class OutputFilesPage(QWizardPage):
    def __init__(self, parent=None):
        super(OutputFilesPage, self).__init__(parent)

        self.setTitle("GoverningGradient_x")
        self.setSubTitle("Specify where you want the wizard to put the "
                "generated skeleton code.")

        groupBox = QGroupBox("C&onstructor")
        groupBoxLayout = QVBoxLayout()

        text_govern_x = governfun_input(2)
        governing_gradient_x_textedit = text_govern_x

        groupBoxLayout.addWidget(governing_gradient_x_textedit)

        groupBox.setLayout(groupBoxLayout)

        layout = QGridLayout()
        layout.addWidget(groupBox, 0, 0)


        self.setLayout(layout)



class ConclusionPage(QWizardPage):
    def __init__(self, parent=None):
        super(ConclusionPage, self).__init__(parent)

        self.setTitle("输入完成")

        self.label = QLabel()
        self.label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def initializePage(self):
        finishText = self.wizard().buttonText(QWizard.FinishButton)
        finishText.replace('&', '')
        self.label.setText("Click %s to generate." % finishText)