import os
import sys

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QTabWidget, QWidget, QDockWidget, QTextEdit, QTableWidget, QPushButton, QStatusBar, \
    QMainWindow, QTableWidgetItem, QAction, QToolBar, QSplitter, QMenu, QMessageBox, QApplication, QSizePolicy, \
    QVBoxLayout, QLabel, QListWidgetItem, QHBoxLayout, QListWidget
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
from View.QZS_V2.dock_left_dialog import dockleft
from View.QZS_V2.harmonic_table_widget import harmonic_table_widget
from View.QZS_V2.identification_algorithm.Thread_FourierSeriesExpansion import FourierSeriesExpansion_Thread
from View.QZS_V2.identification_algorithm.Thread_Identification import Thread_Identification

BSER_DIR=os.path.dirname(os.path.realpath(__file__))

RUNNING=1
STOP=2
SUSPENDING=3
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

class QZSUI_V3(QMainWindow,QtStyleTools):

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
        """设置字体字号"""
        font = self.font()
        font.setPointSize(13)
        font.setFamily("SimHei")

        self.window().setFont(font)

        QApplication.instance().setFont(font)

    def setupUi(self):
        """初始化"""
        self.setObjectName("qzs_identification")
        self.resize(1200, 800)
        self.setWindowTitle("准零刚度系统结构参数标定软件")

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
        """创建系统菜单"""
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        edit_menu = menubar.addMenu("编辑")
        self.a_menu = menubar.addMenu("视图")
        b_menu = menubar.addMenu("导航")
        c_menu = menubar.addMenu("重构")
        d_menu = menubar.addMenu("工具")
        e_menu = menubar.addMenu("窗口")
        self.help_menu = menubar.addMenu("帮助")

    def create_menu_action(self):
        """创建系统菜单栏动作"""
        about_action = QAction(QIcon(os.path.join('images', 'question.png')),"About QZS SOFTWARE",self)
        about_action.setStatusTip("Find out more about QZS")
        about_action.triggered.connect(self.about)
        self.help_menu.addAction(about_action)

    def create_toolbar(self):
        """创建系统工具栏"""
        self.toolbar = QToolBar()

        input_para_action = QAction(QIcon(os.path.join('images', 'input_para.png')), "导入参数...", self)
        input_para_action.setStatusTip("输入参数")
        input_para_action.triggered.connect(self.input_model)
        self.toolbar.addAction(input_para_action)

        govern_check_action = QAction(QIcon(os.path.join('images', 'govern_fun.png')), "打开控制方程...", self)
        govern_check_action.setStatusTip("控制方程")
        govern_check_action.triggered.connect(self.govern_file_open)
        self.toolbar.addAction(govern_check_action)

        save_result_action = QAction(QIcon(os.path.join('images', 'save_result.png')), "保存辨识结果...", self)
        save_result_action.setStatusTip("保存结果")
        save_result_action.triggered.connect(self.save_identification)
        self.toolbar.addAction(save_result_action)

        key_import_action = QAction(QIcon(os.path.join('images', 'key_import.png')), "一键导入之前设置...", self)
        key_import_action.setStatusTip("一键导入")
        key_import_action.triggered.connect(self.a_key_to_import)
        self.toolbar.addAction(key_import_action)


        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(left_spacer)


        start_iden_action=QAction(QIcon(os.path.join('images', 'play.png')), "Start...", self)
        start_iden_action.setStatusTip("开始辨识")
        start_iden_action.triggered.connect(self.start_identification)
        self.toolbar.addAction(start_iden_action)

        suspend_iden_action=QAction(QIcon(os.path.join('images', 'pause.png')), "Suspend...", self)
        suspend_iden_action.setStatusTip("暂停")
        suspend_iden_action.triggered.connect(self.suspend_identification)
        self.toolbar.addAction(suspend_iden_action)

        resume_iden_action = QAction(QIcon(os.path.join('images', 'resume.png')), "Resume...", self)
        resume_iden_action.setStatusTip("继续")
        resume_iden_action.triggered.connect(self.resume_identification)
        self.toolbar.addAction(resume_iden_action)

        stop_iden_action = QAction(QIcon(os.path.join('images', 'stop.png')), "Stop...", self)
        stop_iden_action.setStatusTip("终止")
        stop_iden_action.triggered.connect(self.stop_identification)
        self.toolbar.addAction(stop_iden_action)


        self.addToolBar(self.toolbar)
    def govern_file_open(self):
        """打开控制方程"""
        dialog=Select_govern_V2()
        dialog.signal_finish.connect(self.tab_add_govern)
        dialog.exec_()

    def tab_add_govern(self,url,filename):
        """在TAB显示控制方程"""
        self.tabWidget.addTab(GeneralTab(url), filename)

    def about(self):
        """打开帮助文档"""
        dlg = AboutDialog_V2()
        dlg.exec_()

    def create_dockleft(self):
        """创建左边的功能区"""
        self.dockleft_dialog=dockleft()
        self.dockleft_dialog.listWidget.currentRowChanged.connect(
            self.run_action)
        self.dockleft = QDockWidget("功能区", self)
        self.dockleft.setMinimumWidth(150)
        #self.dockleft.setMaximumWidth(200)
        self.dockleft.setWidget(self.dockleft_dialog)

        return self.dockleft

    def create_dockcenter(self):
        """中间的TAB"""

        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_current_tab)




        return  self.tabWidget

    def create_dockbottom(self):
        """底部文本框"""

        splitter = QSplitter()



        # Qt.Vertical 垂直   Qt.Horizontal 水平
        splitter.setOrientation(Qt.Horizontal)


        self.dockBottom = QDockWidget("输出信息", self)

        self.textedit=QTextEdit()

        self.textedit.setText("欢迎使用准零刚度辨识系统，如需帮助请点击上方帮助按钮！")

        #self.log=LogViewer()


        splitter.addWidget(self.textedit)
        #splitter.addWidget(self.log)
        splitter.setSizes([200, 100])
        #splitter.setStretchFactor(1, 0.3)


        self.dockBottom.setWidget(splitter)


        return self.dockBottom

    def create_dockright(self):
        """右侧表格"""
        self.table = QTableWidget(0,4)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setHorizontalHeaderLabels(("激励频率","时间" ,"响应","激励"))

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.table_right_menu)



        self.dockRight = QDockWidget("变量", self)
        self.dockRight.setWidget(self.table)




        return self.dockRight

    def table_right_menu(self, pos):
        """表格右键的事件"""
        selected_item_list = self.table.selectedItems()
        if len(selected_item_list) == 0:
            return
        menu = QMenu()
        item_watch = menu.addAction("查看")
        action = menu.exec_(self.table.mapToGlobal(pos))
        if action == item_watch:
            row_index=selected_item_list[0].row()
            table_show=QTableWidget()

    def add_fre_res_dialog(self):
        """频响分析"""
        self.fre_res_dialog=Frequency_response_dialog()
        self.tabWidget.addTab(self.fre_res_dialog, "频响分析")



    def output_data(self):
        pass


    def acquire_mu_and_extra_para(self):
        """开始执行前获取mu和额外的参数"""
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
        """开始执行"""
        if len(self.list)==0:
            QMessageBox.warning(self, "警告", "辨识请先进行参数设置及数据输入！")
        else:

            if self.switch != STOP:
                QMessageBox.warning(self, "错误", "正在执行中")
                return

            self.switch = RUNNING
            self.loading=MetroCircleProgress(self)
            self.status.addPermanentWidget(self.loading)

            #self.update_status_message("执行中")

            self.add_residual_dialog()

            self._thread=Thread_Identification(self.mu,self.list,self.extra_para,self)

            self._thread.valueChanged.connect(self.init_tasking_success_callback)

            self._thread.finished.connect(self.init_task_success_callback)

            self._thread.transfer.connect(self.plt_para)

            self._thread.start()



    def input_model(self):
        """输入参数信息"""
        wizard = ClassWizard_V2()
        wizard.components['para_page'].para_log.signal_finish.connect(self.deal_input_data)
        wizard.components['file_page'].experiment_dialog.input_data.connect(self.deal_table_data)
        wizard.setWindowModality(Qt.ApplicationModal)
        wizard.exec_()

    def deal_table_data(self,array_temp):
        """创建表格内容"""
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
        """谐波系数表格"""

        self.acquire_mu_and_extra_para()

        self.update_status_message("计算谐波系数中")

        self.list = FourierSeriesExpansion_Thread(int(self.extra_para[-1]), self.array)

        create_harmonic_table=harmonic_table_widget(self.list)

        self.tabWidget.addTab(create_harmonic_table,"谐波系数")



        self.update_status_message("谐波系数计算完成")


    def plt_para(self,iter,mu):
        """绘制辨识后的参数"""


        plot_parameters=plot_para(iter,mu)
        plot_parameters.plot()


    def save_identification(self):
        """保存辨识结果"""

        save_result= result_save_dialog()
        save_result.setWindowModality(Qt.ApplicationModal)
        save_result.exec_()

    def suspend_identification(self):
        """挂起线程"""
        if self.switch!=RUNNING  :
            QMessageBox.warning(self,"错误","请先运行或者已经挂起")
            return

        self.switch=SUSPENDING

        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = SuspendThread(self._thread.handle)
        print('挂起线程', self._thread.handle, ret)

    def resume_identification(self):
        """恢复辨识进程"""

        if self.switch!=SUSPENDING:
            QMessageBox.warning(self,"错误","请先挂起")
            return
        self.switch=RUNNING
        if self._thread.handle == -1:
            return print('handle is wrong')
        ret = ResumeThread(self._thread.handle)
        print('恢复线程', self._thread.handle, ret)


    def stop_identification(self):
        """停止辨识，一般不要进行此操作，容易卡死"""

        if self.switch!=RUNNING and self.switch!=SUSPENDING:
            QMessageBox.warning(self,"错误","请先运行")
            return

        reply = QMessageBox.question(self, "QMessageBox.question()",
                                     "此操作极易造成系统崩溃，确定要继续吗？",
                                     QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            import ctypes
            ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
                self._thread.handle, 0)
            print('终止线程', self._thread.handle, ret)
            self.btn_stop_iden.setEnabled(False)

        elif reply == QMessageBox.No:
            pass
        else:
            pass

    # def closeEvent(self, event):
    #     if self._thread.isRunning():
    #         self._thread.quit()
    #         # 强制
    #         # self._thread.terminate()
    #     del self._thread
    #     super(QZSUI_V2, self).closeEvent(event)



    def init_tasking_success_callback(self,list):
        """辨识执行时进行的动作：文本框实时显示辨识结果,显示残差..."""
        self.textedit.append(str(list)+"\n")
        self.textedit.moveCursor(QTextCursor.End)
        self.iter.append(list[0])
        self.gamma_list.append(list[1])
        self.increment_list.append(list[2])



        self.residual_tab.gamma_plot.plot(self.iter,self.gamma_list, clear=True,pen=pg.mkPen(color='k', width=2))

        self.residual_tab.increment_plot.plot(self.iter,self.increment_list, clear=True,pen=pg.mkPen(color='k', width=2))

        pg.QtGui.QApplication.processEvents()








        #self._logger.info("辨识中！")

    def init_task_success_callback(self):
        """辨识结束后的任务"""
        #self._logger.info("辨识结束！请在array中查看结果！")
        self.status.showMessage("辨识结束，请在array数组中查看结果！")
        self.switch = STOP
        self.status.removeWidget(self.loading)

    def init_task_error_callback(self, str):
        """辨识失败后的任务"""
        self.textedit.setText(str)
        # self._logger.error("Uncaught exception occurred",
        #                    "请检查参数设置后重试！")
    def deal_input_data(self,str):
        self.textedit.setText(str)




    def close_current_tab(self, i):
        """关闭选项卡"""
        if self.tabWidget.count() < 2:
            QMessageBox.warning(self, "警告", "此为最后一页，不能关闭！")
            return

        self.tabWidget.removeTab(i)

    def setup_logging(self):
        """设置日志"""
        from logbook.compat import redirect_logging
        from logbook import INFO

        redirect_logging()
        self.log.handler.level = INFO
        self.log.handler.push_application()

        # self._logger = Logger()
        # self._logger.info("日志信息")
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            # self._logger.error("Uncaught exception occurred",
            #                    exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = handle_exception
    def update_status_message(self,message):
        """更新状态栏信息"""
        self.status.showMessage(message)
        self.status.repaint()

    def add_residual_dialog(self):
        """添加残差窗口"""
        self.residual_tab=residual_dialog()
        self.tabWidget.addTab(self.residual_tab, "残差监控")

    def add_amplitude_dialog(self):

        self.amplitude_tab = Amplitude_harmonic_dialog(self.list)
        self.tabWidget.addTab(self.amplitude_tab , "谐波幅值")

    def add_nonlinear_dialog(self):
        self.tab_nonlinear_detection = detection_dialog_V2()
        self.tabWidget.addTab(self.tab_nonlinear_detection, "非线性检测")
    def run_action(self,index):

        if index==0:
            self.add_nonlinear_dialog()
        elif index==1:
            self.add_fre_res_dialog()
        elif index==2:
            self.add_residual_dialog()
        else :
            self.add_amplitude_dialog()


    def a_key_to_import(self):


        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)


    # splash_dialog = GifSplashScreen()
    # splash_dialog.show()
    # apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)

    ex = QZSUI_V3()
    ex.show()
    sys.exit(app.exec_())