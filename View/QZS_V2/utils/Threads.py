
from PyQt5.QtCore import QThread, pyqtSignal

from View.QZS.identification.Identification_Main import identification_main


class Thread(QThread):

    success = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, mu,predata,extrs_para,*args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.mu=mu
        self.predata=predata
        self.extrs_para=extrs_para



    def run(self) :
        try:

                result=identification_main(self.mu,self.predata,self.extrs_para)
                self.success.emit(result)

        except Exception as e:
            self.error.emit("发生了错误，请检查参数设置！")
