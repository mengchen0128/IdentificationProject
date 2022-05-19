import cgitb
import sys
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QSplashScreen

cgitb.enable(format("text"))

from View.QZS.QZS_View import QZSUI


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

class QZSController(QZSUI):
    def __init__(self):
        super(QZSController, self).__init__()

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

    ex = QZSController()
    ex.show()
    sys.exit(app.exec_())