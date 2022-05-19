import cgitb
import os
import sys

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QSplashScreen
from qt_material import apply_stylesheet, QtStyleTools

from View.QZS_V2.QZS_View_V2 import QZSUI_V2

cgitb.enable(format("text"))



class GifSplashScreen(QSplashScreen):

    def __init__(self, *args, **kwargs):
        super(GifSplashScreen, self).__init__(*args, **kwargs)
        self.movie = QMovie('images/splash.gif')
        self.movie.frameChanged.connect(self.onFrameChanged)
        self.movie.start()

    def onFrameChanged(self, _):
        self.setPixmap(self.movie.currentPixmap())

    def finish(self, widget):
        self.movie.stop()
        super(GifSplashScreen, self).finish(widget)

class QZSController(QZSUI_V2):
    def __init__(self):
        super(QZSController, self).__init__()
        #self.apply_stylesheet(self, 'light_blue.xml', invert_secondary=True)

        # for i in range(2):
        #     sleep(1)
        #     splash_dialog.showMessage('加载进度: %d' % i, Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
        #     QApplication.instance().processEvents()
        #
        # splash_dialog.showMessage('初始化完成', Qt.AlignHCenter | Qt.AlignBottom, Qt.white)
        # splash_dialog.finish(self)




if __name__ == '__main__':
    app = QApplication(sys.argv)


    # splash_dialog = GifSplashScreen()
    # splash_dialog.show()
    # apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)


    ex = QZSController()

    # stylesheet = app.styleSheet()
    # with open('QSS/custom.css') as file:
    #     app.setStyleSheet(stylesheet + file.read().format(**os.environ))
    # ex.pushButton.setProperty('class', 'big_button')
    ex.show()
    sys.exit(app.exec_())