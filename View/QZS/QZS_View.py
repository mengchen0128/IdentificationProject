import os
import sys

import numpy
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTabWidget, QWidget, QDockWidget, QTextEdit, QTableWidget, QPushButton, QStatusBar, \
    QMainWindow, QTableWidgetItem, QAction, QToolBar, QSplitter, QMenu, QMessageBox
from win32process import SuspendThread, ResumeThread

from View.QZS.Data_input_dialog import InputDialog
from View.QZS.about_qzs import AboutDialog
from View.QZS.Extra_parameters_dialog import ExtraParaDialog
from View.QZS.findfiles import find_file
from View.QZS.generaltab import GeneralTab
from View.QZS.govern_input import ClassWizard
from View.QZS.identification.Object_Identification_Main import Worker_object

from View.QZS.identification.Thread_Identification_Main import Thread_Identification_Main
from View.QZS.log import LogViewer
from View.QZS.Nonlinear_detection_dialog import detection_dialog
from View.QZS.plot import plot_para
from View.QZS.utils.Threads import Thread

# Status_Mapping = {
#     0: "初始化中",
#     1: "正在执行",
#     2: "停止中",
#     3: "已终止",
#
# }
# RUNNING=1
# STOPING=2
# STOP=3

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

class QZSUI(QMainWindow):

    def __init__(self):

        super().__init__()
        self.array=[]
        self.setupUi()
        # self.switch=STOP
    def setupUi(self):

        
        self.setObjectName("qzs_identification")
        self.resize(1200, 800)
        self.setWindowTitle("准零刚度辨识")
        self.create_menu()
        self.create_toolbar()

        self.setCentralWidget(self.create_dockcenter())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.create_dockleft())
        self.addDockWidget(Qt.RightDockWidgetArea, self.create_dockright())
        self.addDockWidget(Qt.BottomDockWidgetArea, self.create_dockbottom())
        self.setup_logging()
        self._logger.info("日志信息")
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("准零刚度辨识系统")


    def create_menu(self):
        # 菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        edit_menu = menubar.addMenu("编辑")
        help_menu = menubar.addMenu("帮助")


        about_action = QAction("About QZS SOFTWARE",self)
        about_action.setStatusTip("Find out more about QZS")  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        file_toolbar = QToolBar("Govern_Fun")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        open_file_action = QAction(QIcon(os.path.join('images', 'img.png')), "Open Govern_Fun...", self)
        open_file_action.setStatusTip("Open Govern_Fun")
        open_file_action.triggered.connect(self.file_open)
        file_toolbar.addAction(open_file_action)


    def file_open(self):

        dialog=find_file()
        dialog.signal_finish.connect(self.tab_add_govern)
        dialog.exec_()

    def tab_add_govern(self,url,filename):

        self.tabWidget.addTab(GeneralTab(url), filename)


    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def create_dockleft(self):
        self.verticalLayoutWidget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        btn_start=QPushButton("输入参数及实验数据")
        layout.addWidget(btn_start)
        btn_start.clicked.connect(self.input_model)


        btn_govern=QPushButton("输入控制方程")
        layout.addWidget(btn_govern)
        btn_govern.clicked.connect(self.output_data)

        btn_extra_para = QPushButton("输入额外的参数")
        layout.addWidget(btn_extra_para)
        btn_extra_para.clicked.connect(self.input_extra_para)


        self.btn_start_iden=btn_start_iden= QPushButton("开始辨识")
        layout.addWidget(btn_start_iden)
        btn_start_iden.clicked.connect(self.start_identification_another)

        self.btn_suspend_iden=btn_suspend_iden= QPushButton("暂停辨识")
        btn_suspend_iden.setEnabled(False)
        layout.addWidget(btn_suspend_iden)
        btn_suspend_iden.clicked.connect(self.suspend_identification_another)

        self.btn_resume_iden=btn_resume_iden= QPushButton("继续辨识")
        btn_resume_iden.setEnabled(False)
        layout.addWidget(btn_resume_iden)
        btn_resume_iden.clicked.connect(self.resume_identification_another)


        self.btn_stop_iden=btn_stop_iden = QPushButton("终止辨识")
        btn_stop_iden.setEnabled(False)
        layout.addWidget(btn_stop_iden)
        btn_stop_iden.clicked.connect(self.stop_identification_another)


        self.btn_plot_iden=btn_plot_iden = QPushButton("关闭作图")
        btn_plot_iden.setEnabled(False)
        layout.addWidget(btn_plot_iden)
        btn_plot_iden.clicked.connect(self.plot_identification_another)

        layout.addStretch()


        self.dockleft = QDockWidget("数据输入", self)
        self.dockleft.setMinimumWidth(200)
        self.dockleft.setWidget(self.verticalLayoutWidget)

        return self.dockleft

    def create_dockcenter(self):
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_current_tab)

        self.tab_nonlinear_detection = detection_dialog()

        self.tabWidget.addTab(self.tab_nonlinear_detection, "非线性检测")
        return  self.tabWidget

    def create_dockbottom(self):

        splitter = QSplitter()



        # Qt.Vertical 垂直   Qt.Horizontal 水平
        splitter.setOrientation(Qt.Horizontal)


        self.dockBottom = QDockWidget("输出信息", self)

        self.textedit=QTextEdit()
        self.textedit.setText("欢迎使用准零刚度辨识系统，如需帮助请点击上方帮助按钮！")

        self.log=LogViewer()


        splitter.addWidget(self.textedit)
        splitter.addWidget(self.log)
        splitter.setSizes([200, 100])
        #splitter.setStretchFactor(1, 0.3)

        self.dockBottom.setWidget(splitter)



        return self.dockBottom

    def create_dockright(self):
        self.table = QTableWidget()

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SingleSelection)


        self.table.setColumnWidth(4, 200)
        self.table.setRowHeight(0, 40)

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.table_right_menu)



        self.dockRight = QDockWidget("变量", self)
        self.dockRight.setWidget(self.table)




        return self.dockRight

    def table_right_menu(self, pos):

        selected_item_list = self.table.selectedItems()
        if len(selected_item_list) == 0:
            return
        menu = QMenu()
        item_watch = menu.addAction("查看")
        action = menu.exec_(self.table.mapToGlobal(pos))
        if action == item_watch:
            row_index=selected_item_list[0].row()
            table_show=QTableWidget()

    def input_model(self):
        dialog = InputDialog()
        dialog.signal_finish.connect(self.deal_input_data)
        dialog.input_data.connect(self.deal_table_data)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()


    def output_data(self):
        wizard = ClassWizard()
        wizard.setWindowModality(Qt.ApplicationModal)
        wizard.exec_()

    def input_extra_para(self):
        dialog=ExtraParaDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

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



    def start_identification(self):
        if len(self.array)==0:
            QMessageBox.warning(self, "警告", "辨识前请输入实验数据！")
        else:
            self.acquire_mu_and_extra_para()
            self.update_status_message("执行中")
            thread=Thread(self.mu,self.array,self.extra_para,self)
            thread.success.connect(self.init_task_success_callback)
            thread.error.connect(self.init_task_error_callback)
            thread.start()

    def start_identification_another(self):
        if len(self.array)==0:
            QMessageBox.warning(self, "警告", "辨识前请输入实验数据！")
        else:


            self.acquire_mu_and_extra_para()
            self.update_status_message("执行中")
            self._thread=Thread_Identification_Main(self.mu,self.array,self.extra_para,self)
            self._thread.valueChanged.connect(self.init_tasking_success_callback)
            self._thread.finished.connect(self.init_task_success_callback)
            self._thread.transfer.connect(self.plt_para)
            self.btn_suspend_iden.setEnabled(True)
            self.btn_start_iden.setEnabled(False)
            self.btn_stop_iden.setEnabled(True)

            self._thread.start()
    def plt_para(self,iter,mu):
        plot_parameters=plot_para(iter,mu)
        plot_parameters.plot()
    def plot_identification_another(self):
        pass

    def  suspend_identification_another(self):
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = SuspendThread(self._thread.handle)
        print('挂起线程', self._thread.handle, ret)
        self.btn_suspend_iden.setEnabled(False)
        self.btn_resume_iden.setEnabled(True)
    def resume_identification_another(self):
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = ResumeThread(self._thread.handle)
        print('恢复线程', self._thread.handle, ret)
        self.btn_suspend_iden.setEnabled(True)
        self.btn_resume_iden.setEnabled(False)

    def stop_identification_another(self):
        # if self.switch!=RUNNING:
        #     QMessageBox.warning(self,"错误", "请先执行！")
        #     return
        # self.switch=STOP
        # if self._thread.isRunning():
        #     # self._thread.requestInterruption()
        #     #self._thread.quit()
        #     #self._thread.wait()
        #
        #     # 强制
        #     self._thread.terminate()
        # self._thread.deleteLater()
        reply = QMessageBox.question(self, "QMessageBox.question()",
                                     "此操作极易造成系统崩溃，确定要继续吗？",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            self.btn_start_iden.setEnabled(False)
            self.btn_suspend_iden.setEnabled(False)
            self.btn_resume_iden.setEnabled(False)
            import ctypes
            ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
                self._thread.handle, 0)
            print('终止线程', self._thread.handle, ret)
            self.btn_stop_iden.setEnabled(False)

        elif reply == QMessageBox.No:
            pass
        else:
            pass

    def closeEvent(self, event):
        if self._thread.isRunning():
            self._thread.quit()
            # 强制
            # self._thread.terminate()
        del self._thread
        super(QZSUI, self).closeEvent(event)


    def start_identification_object(self):
        # if self.switch!=STOP:
        #     QMessageBox.warning(self,"错误","正在执行中")
        #     return

        if len(self.array)==0:
            QMessageBox.warning(self, "警告", "辨识前请输入实验数据！")
        else:
            # self.switch = RUNNING
            self.acquire_mu_and_extra_para()
            self.update_status_message("执行中")


            self._thread = QThread(self)
            self._worker = Worker_object(self.mu,self.array,self.extra_para)
            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run_object)
            self._thread.finished.connect(self.init_task_success_callback)
            self._worker.valueChanged.connect(self.init_tasking_success_callback)
            self._worker.finished.connect(self.stop_identification_another)


            self._thread.start()


    def init_tasking_success_callback(self,list):
        self.textedit.append(str(list)+"\n")
        self._logger.info("辨识中！")

    def init_task_success_callback(self):

        self._logger.info("辨识结束！请在array中查看结果！")
        self.status.showMessage("辨识结束，请在array数组中查看结果！")
        self.btn_start_iden.setEnabled(True)
        self.btn_suspend_iden.setEnabled(False)
        self.btn_resume_iden.setEnabled(False)
        self.btn_stop_iden.setEnabled(False)
        self.btn_plot_iden.setEnabled(True)
    def init_task_error_callback(self, str):
        self.textedit.setText(str)
        self._logger.error("Uncaught exception occurred",
                           "请检查参数设置后重试！")
    def deal_input_data(self,str):
        self.textedit.setText(str)

    def deal_table_data(self,array_temp):
        #array=numpy.array(list,dtype=object)
        self.array=array=array_temp
        self.table.setColumnCount(3)
        size=np.shape(array)
        self.table.setRowCount(size[1])

        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):

                if col==0:
                    cell = QTableWidgetItem(str(array[0, row][0][0,0]))
                    self.table.setItem(row,col,cell)
                else:
                    cell = QTableWidgetItem(str(np.shape(array[0, row][col])))
                    self.table.setItem(row, col, cell)

    def close_current_tab(self, i):
        if self.tabWidget.count() < 2:
            QMessageBox.warning(self, "警告", "此为最后一页，不能关闭！")
            return

        self.tabWidget.removeTab(i)

    def setup_logging(self):

        from logbook.compat import redirect_logging
        from logbook import INFO, Logger

        redirect_logging()
        self.log.handler.level = INFO
        self.log.handler.push_application()

        self._logger = Logger()

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            self._logger.error("Uncaught exception occurred",
                               exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = handle_exception
    def update_status_message(self,message):
        self.status.showMessage(message)
        self.status.repaint()
