import os
import sys

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QTabWidget, QWidget, QDockWidget, QTextEdit, QTableWidget, QPushButton, QStatusBar, \
    QMainWindow, QTableWidgetItem, QAction, QToolBar, QSplitter, QMenu, QMessageBox, QApplication, QSizePolicy, \
    QVBoxLayout, QLabel
from qt_material import QtStyleTools
from win32process import SuspendThread, ResumeThread

from View.QZS.generaltab import GeneralTab
from View.QZS.plot import plot_para
from View.QZS_V2.About_qzs_V2 import AboutDialog_V2
from View.QZS_V2.Amplitude_harmonic_dialog import Amplitude_harmonic_dialog
from View.QZS_V2.ClassWizard_V2 import ClassWizard_V2
from View.QZS_V2.Frequency_response_dialog import Frequency_response_dialog
from View.QZS_V2.MetroCircleProgress import MetroCircleProgress
from View.QZS_V2.Nonlinear_detection_dialog_V2 import detection_dialog_V2
from View.QZS_V2.Residual_dialog import residual_dialog
from View.QZS_V2.Result_save_dialog import result_save_dialog
from View.QZS_V2.Select_govern_V2 import Select_govern_V2
from View.QZS_V2.identification_algorithm.Thread_FourierSeriesExpansion import FourierSeriesExpansion_Thread
from View.QZS_V2.identification_algorithm.Thread_Identification import Thread_Identification

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

RUNNING=1
STOP=2
SUSPENDING=3


class QZSUI_V2(QMainWindow,QtStyleTools):

    def __init__(self):

        super().__init__()
        self.iter=[]
        self.gamma_list=[]
        self.increment_list=[]
        self.setupUi()
        self.setAcceptDrops(True)
        self.mu=[]
        self.switch=STOP
        self.list=[]

        #self.apply_stylesheet(self, 'light_blue.xml', invert_secondary=True)


    def set_font_size(self):
        font = self.font()
        font.setPointSize(13)
        font.setFamily("SimHei")

        self.window().setFont(font)

        QApplication.instance().setFont(font)

    def setupUi(self):

        self.setObjectName("qzs_identification")
        self.resize(1200, 800)
        self.setWindowTitle("??????????????????????????????????????????")

        self.create_menu()
        self.create_menu_action()

        self.create_toolbar()

        self.setCentralWidget(self.create_dockcenter())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.create_dockleft())
        self.addDockWidget(Qt.RightDockWidgetArea, self.create_dockright())
        self.addDockWidget(Qt.BottomDockWidgetArea, self.create_dockbottom())

        #self.setup_logging()


        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready!")

        self.set_font_size()
    def create_menu(self):
        """??????????????????"""
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('??????')
        edit_menu = menubar.addMenu("??????")
        self.a_menu = menubar.addMenu("??????")
        b_menu = menubar.addMenu("??????")
        c_menu = menubar.addMenu("??????")
        d_menu = menubar.addMenu("??????")
        e_menu = menubar.addMenu("??????")
        self.help_menu = menubar.addMenu("??????")

    def create_menu_action(self):
        """???????????????????????????"""
        about_action = QAction("About QZS SOFTWARE",self)
        about_action.setStatusTip("Find out more about QZS")
        about_action.triggered.connect(self.about)
        self.help_menu.addAction(about_action)

    def create_toolbar(self):
        """?????????????????????"""
        self.toolbar = QToolBar()

        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(left_spacer)


        start_iden_action=QAction(QIcon(os.path.join('images', 'play.png')), "Start...", self)
        start_iden_action.setStatusTip("????????????")
        start_iden_action.triggered.connect(self.start_identification_another)
        self.toolbar.addAction(start_iden_action)

        suspend_iden_action=QAction(QIcon(os.path.join('images', 'pause.png')), "Suspend...", self)
        suspend_iden_action.setStatusTip("??????")
        suspend_iden_action.triggered.connect(self.suspend_identification_another)
        self.toolbar.addAction(suspend_iden_action)

        resume_iden_action = QAction(QIcon(os.path.join('images', 'forward.png')), "Resume...", self)
        resume_iden_action.setStatusTip("??????")
        resume_iden_action.triggered.connect(self.resume_identification_another)
        self.toolbar.addAction(resume_iden_action)

        stop_iden_action = QAction(QIcon(os.path.join('images', 'stop.png')), "Stop...", self)
        stop_iden_action.setStatusTip("??????")
        stop_iden_action.triggered.connect(self.stop_identification_another)
        self.toolbar.addAction(stop_iden_action)

        open_govern_action = QAction(QIcon(os.path.join('images', 'g.png')), "Open Govern_Fun...", self)
        open_govern_action.setStatusTip("Open Govern_Fun")
        open_govern_action.triggered.connect(self.govern_file_open)
        self.toolbar.addAction(open_govern_action)

        amplitude_harmonic_action = QAction(QIcon(os.path.join('images', 'a.png')), "Open Amplitude_harmonic_dialog...", self)
        amplitude_harmonic_action.setStatusTip("Open Amplitude_harmonic_dialog")
        amplitude_harmonic_action.triggered.connect(self.add_amplitude_dialog)
        self.toolbar.addAction(amplitude_harmonic_action)



        residual_action = QAction(QIcon(os.path.join('images', 'r.png')), "Residual...", self)
        residual_action.setStatusTip("Open Residual_Dialog")
        residual_action.triggered.connect(self.add_residual_dialog)
        self.toolbar.addAction(residual_action)

        frequency_a_action = QAction(QIcon(os.path.join('images', 'f.png')), "Open Fre_Res_Dialog...", self)
        frequency_a_action.setStatusTip("Open Fre_Res_Dialog")
        frequency_a_action.triggered.connect(self.add_fre_res_dialog)
        self.toolbar.addAction(frequency_a_action)

        nonlinear_detection_action = QAction(QIcon(os.path.join('images', 'n.png')), "Open nonlinear_detection_dialog...", self)
        nonlinear_detection_action.setStatusTip("Open nonlinear_detection_dialog")
        nonlinear_detection_action.triggered.connect(self.add_nonlinear_dialog)
        self.toolbar.addAction(nonlinear_detection_action)

        self.addToolBar(self.toolbar)
    def govern_file_open(self):

        dialog=Select_govern_V2()
        dialog.signal_finish.connect(self.tab_add_govern)
        dialog.exec_()

    def tab_add_govern(self,url,filename):

        self.tabWidget.addTab(GeneralTab(url), filename)

    def about(self):
        """??????????????????"""
        dlg = AboutDialog_V2()
        dlg.exec_()

    def create_dockleft(self):
        self.verticalLayoutWidget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        btn_start=QPushButton("????????????????????????")

        layout.addWidget(btn_start)



        btn_start.clicked.connect(self.input_model)



        self.btn_save_iden=btn_save_iden = QPushButton("??????????????????")
        btn_save_iden.setEnabled(False)
        layout.addWidget(btn_save_iden)
        btn_save_iden.clicked.connect(self.save_identification_another)


        layout.addStretch()


        self.dockleft = QDockWidget("????????????", self)
        self.dockleft.setMinimumWidth(200)
        self.dockleft.setWidget(self.verticalLayoutWidget)

        return self.dockleft

    def create_dockcenter(self):


        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_current_tab)


        self.add_nonlinear_dialog()
        self.add_residual_dialog()
        self.add_fre_res_dialog()

        return  self.tabWidget

    def create_dockbottom(self):


        splitter = QSplitter()



        # Qt.Vertical ??????   Qt.Horizontal ??????
        splitter.setOrientation(Qt.Horizontal)


        self.dockBottom = QDockWidget("????????????", self)

        self.textedit=QTextEdit()

        self.textedit.setText("?????????????????????????????????????????????????????????????????????????????????")

        #self.log=LogViewer()


        splitter.addWidget(self.textedit)
        #splitter.addWidget(self.log)
        splitter.setSizes([200, 100])
        #splitter.setStretchFactor(1, 0.3)


        self.dockBottom.setWidget(splitter)


        return self.dockBottom

    def create_dockright(self):
        self.table = QTableWidget(0,4)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setHorizontalHeaderLabels(("????????????","??????" ,"??????","??????"))

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.table_right_menu)



        self.dockRight = QDockWidget("??????", self)
        self.dockRight.setWidget(self.table)




        return self.dockRight

    def table_right_menu(self, pos):

        selected_item_list = self.table.selectedItems()
        if len(selected_item_list) == 0:
            return
        menu = QMenu()
        item_watch = menu.addAction("??????")
        action = menu.exec_(self.table.mapToGlobal(pos))
        if action == item_watch:
            row_index=selected_item_list[0].row()
            table_show=QTableWidget()

    def add_fre_res_dialog(self):
        self.fre_res_dialog=Frequency_response_dialog()
        self.tabWidget.addTab(self.fre_res_dialog, "????????????")



    def output_data(self):
        pass


    def acquire_mu_and_extra_para(self):
        mu=[]
        extra_para=[]
        import json
        filepath_mu = os.path.join(BSER_DIR, "database/parameters.json")
        with open(filepath_mu, mode='r', encoding='utf-8') as f:
            data_mu = f.read()
            datalist_mu = json.loads(data_mu)

            for row_list in datalist_mu:
                for i, ele in enumerate(row_list):
                     if i == 1:
                         mu.append(float(ele))
            f.close()

        filepath_extra_para = os.path.join(BSER_DIR, "database/extra_parameters.json")
        with open(filepath_extra_para, mode='r', encoding='utf-8') as f:
            data_mu = f.read()
            datalist_para = json.loads(data_mu)
            for key in datalist_para:
                extra_para.append(float(datalist_para[key]))

            f.close()
        self.mu=mu
        self.extra_para=extra_para


    def start_identification_another(self):

        if len(self.list)==0:
            QMessageBox.warning(self, "??????", "????????????????????????????????????????????????")
        else:

            if self.switch != STOP:
                QMessageBox.warning(self, "??????", "???????????????")
                return

            self.switch = RUNNING
            self.loading=MetroCircleProgress(self)
            self.status.addPermanentWidget(self.loading)

            #self.update_status_message("?????????")

            self._thread=Thread_Identification(self.mu,self.list,self.extra_para,self)

            self._thread.valueChanged.connect(self.init_tasking_success_callback)

            self._thread.finished.connect(self.init_task_success_callback)

            self._thread.transfer.connect(self.plt_para)

            self._thread.start()



    def input_model(self):
        wizard = ClassWizard_V2()
        wizard.components['para_page'].para_log.signal_finish.connect(self.deal_input_data)
        wizard.components['file_page'].experiment_dialog.input_data.connect(self.deal_table_data)
        wizard.setWindowModality(Qt.ApplicationModal)
        wizard.exec_()

    def deal_table_data(self,array_temp):

        self.array=array_temp
        #array=numpy.array(list,dtype=object)

        size=np.shape(array_temp)

        self.table.setRowCount(size[1])

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):

                if col==0:
                    cell = QTableWidgetItem(str(array_temp[0, row][0][0,0]))
                    self.table.setItem(row,col,cell)
                else:
                    cell = QTableWidgetItem(str(np.shape(array_temp[0, row][col])))
                    self.table.setItem(row, col, cell)

        self.create_harmonic_table()

    def create_harmonic_table(self):


        self.acquire_mu_and_extra_para()

        self.update_status_message("??????????????????")

        self.list = FourierSeriesExpansion_Thread(int(self.extra_para[-1]), self.array)


    def plt_para(self,iter,mu):
        """????????????????????????"""

        self.switch = STOP
        self.status.removeWidget(self.loading)
        plot_parameters=plot_para(iter,mu)
        plot_parameters.plot()


    def save_identification_another(self):
        """??????????????????"""

        save_result= result_save_dialog()
        save_result.setWindowModality(Qt.ApplicationModal)
        save_result.exec_()

    def suspend_identification_another(self):

        if self.switch!=RUNNING  :
            QMessageBox.warning(self,"??????","??????????????????????????????")
            return

        self.switch=SUSPENDING

        """????????????????????????"""
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = SuspendThread(self._thread.handle)
        print('????????????', self._thread.handle, ret)

    def resume_identification_another(self):
        """??????????????????"""

        if self.switch!=SUSPENDING:
            QMessageBox.warning(self,"??????","????????????")
            return
        self.switch=RUNNING
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = ResumeThread(self._thread.handle)
        print('????????????', self._thread.handle, ret)


    def stop_identification_another(self):
        """?????????????????????????????????????????????????????????"""

        if self.switch!=RUNNING and self.switch!=SUSPENDING:
            QMessageBox.warning(self,"??????","????????????")
            return

        reply = QMessageBox.question(self, "QMessageBox.question()",
                                     "?????????????????????????????????????????????????????????",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            import ctypes
            ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
                self._thread.handle, 0)
            print('????????????', self._thread.handle, ret)
            self.btn_stop_iden.setEnabled(False)

        elif reply == QMessageBox.No:
            pass
        else:
            pass

    # def closeEvent(self, event):
    #     if self._thread.isRunning():
    #         self._thread.quit()
    #         # ??????
    #         # self._thread.terminate()
    #     del self._thread
    #     super(QZSUI_V2, self).closeEvent(event)



    def init_tasking_success_callback(self,list):
        """??????????????????????????????????????????????????????????????????,????????????..."""
        self.textedit.append(str(list)+"\n")
        self.textedit.moveCursor(QTextCursor.End)
        self.iter.append(list[0])
        self.gamma_list.append(list[1])
        self.increment_list.append(list[2])



        self.residual_tab.gamma_plot.plot(self.iter,self.gamma_list, clear=True,pen=pg.mkPen(color='k', width=2))
        self.residual_tab.increment_plot.plot(self.iter,self.increment_list, clear=True,pen=pg.mkPen(color='k', width=2))
        pg.QtGui.QApplication.processEvents()








        #self._logger.info("????????????")

    def init_task_success_callback(self):
        """????????????????????????"""
        #self._logger.info("?????????????????????array??????????????????")
        self.status.showMessage("?????????????????????array????????????????????????")

        self.btn_save_iden.setEnabled(True)

    def init_task_error_callback(self, str):
        """????????????????????????"""
        self.textedit.setText(str)
        # self._logger.error("Uncaught exception occurred",
        #                    "?????????????????????????????????")
    def deal_input_data(self,str):
        self.textedit.setText(str)




    def close_current_tab(self, i):
        """???????????????"""
        if self.tabWidget.count() < 2:
            QMessageBox.warning(self, "??????", "????????????????????????????????????")
            return

        self.tabWidget.removeTab(i)

    def setup_logging(self):
        """????????????"""
        from logbook.compat import redirect_logging
        from logbook import INFO

        redirect_logging()
        self.log.handler.level = INFO
        self.log.handler.push_application()

        # self._logger = Logger()
        # self._logger.info("????????????")
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            # self._logger.error("Uncaught exception occurred",
            #                    exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = handle_exception
    def update_status_message(self,message):
        """?????????????????????"""
        self.status.showMessage(message)
        self.status.repaint()

    def add_residual_dialog(self):
        """??????????????????"""
        self.residual_tab=residual_dialog()
        self.tabWidget.addTab(self.residual_tab, "??????")

    def add_amplitude_dialog(self):
        self.residual_tab = Amplitude_harmonic_dialog()
        self.tabWidget.addTab(self.residual_tab, "????????????")
    def add_nonlinear_dialog(self):
        self.tab_nonlinear_detection = detection_dialog_V2()
        self.tabWidget.addTab(self.tab_nonlinear_detection, "???????????????")
if __name__ == '__main__':
    app = QApplication(sys.argv)


    # splash_dialog = GifSplashScreen()
    # splash_dialog.show()
    # apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)

    ex = QZSUI_V2()
    ex.show()
    sys.exit(app.exec_())