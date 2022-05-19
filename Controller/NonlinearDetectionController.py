import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from View.Detection.NonlinearDetection_View import ChildDialogUi1
import cgitb
cgitb.enable(format("text"))

class DetectionController(QMainWindow,ChildDialogUi1):
    def __init__(self):
        super(DetectionController, self).__init__()
        self.setupUi(self)
        self.tree.clicked.connect(self.Tree_Clicked)



    def Tree_Clicked(self, currentindex):
        #print(currentindex.data())  # 和下面两句相等

        print(self.sender().currentItem().text(0))  # 获取点击的key的值
 # 获取点击的value的值




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DetectionController()
    ex.show()
    sys.exit(app.exec_())