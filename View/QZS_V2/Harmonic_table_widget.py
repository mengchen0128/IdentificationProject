import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAction, QMenu, QHeaderView


class harmonic_table_widget(QTableWidget):
    def __init__(self, list,parent=None):
        super(harmonic_table_widget, self).__init__(parent)
        self.list=list
        self.table()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showData)
    def table(self):

        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["激励频率", "响应谐波系数", "激励谐波系数"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        size=len(self.list)
        self.setRowCount(size)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                if col==0:
                    cell = QTableWidgetItem(str(round(self.list[row].omega,1)))
                    self.setItem(row,col,cell)
                elif col==1:
                    cell = QTableWidgetItem(str(np.shape(self.list[row].X)))
                    self.setItem(row, col, cell)

                else :
                    cell = QTableWidgetItem(str(np.shape(self.list[row].F)))
                    self.setItem(row, col, cell)


    def showData(self,pos):
        selected_item_list = self.selectedItems()
        menu = QMenu()
        item_show = menu.addAction("查看")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == item_show:
            row_index = selected_item_list[0].row()
            col_index = selected_item_list[0].column()
            if col_index == 0:
                print (round(self.list[row_index].omega,1))

            elif col_index == 1:
                 print(self.list[row_index].X)
            else:
                 print(self.list[row_index].F)







