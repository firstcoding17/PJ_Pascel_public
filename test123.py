from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QAction, QVBoxLayout, \
    QWidget, QFileDialog, QDialog, QLineEdit, QInputDialog
from PyQt5.QtCore import Qt
import sys
import pandas as pd
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('pascel-v0.1.5alpha')
        self.setGeometry(100, 100, 1200, 800)
        self.tab_list = []
        self.data_info = []  # 딕셔너리로 데이터 정보들 저장해서 분석에 이용할 것

        # 스타일 시트 파일 읽기
        style_sheet_file = QFile('Pascel.css')
        if style_sheet_file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(style_sheet_file)
            style_sheet = stream.readAll()
            self.setStyleSheet(style_sheet)
            style_sheet_file.close()

        self.initMenuBar()

        # 위쪽 위젯 (2/3)
        # 수직 스플리터 생성
        splitter = QSplitter(Qt.Vertical)  # 수직 스플리터
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.top_widget = QWidget()  # top_widget 정의
        self.top_widget.setMinimumHeight(self.height() * 2 // 3)  # 높이를 전체 높이의 2/3로 설정
        top_label = QLabel('Data Window')
        top_label.setAlignment(Qt.AlignCenter)
        self.top_widget.setStyleSheet("background-color:#F9DB91")
        self.top_widget.layout = QVBoxLayout()
        self.top_widget.layout.addWidget(top_label)
        self.top_widget.layout.addWidget(self.tab_widget)  # self.top_widget에 tab_widget 추가
        self.top_widget.setLayout(self.top_widget.layout)  # self.top_widget에 레이아웃 설정

        # 아래쪽 위젯 (1/3)
        bottom_widget = QWidget()
        bottom_label = QLabel('output window')
        bottom_label.setAlignment(Qt.AlignCenter)
        bottom_widget.layout = QVBoxLayout()
        bottom_widget.layout.addWidget(bottom_label)
        bottom_widget.setLayout(bottom_widget.layout)

        # 스플리터에 위젯 추가
        splitter.addWidget(self.top_widget)
        splitter.addWidget(bottom_widget)

        self.setCentralWidget(splitter)

    def initMenuBar(self):
        menubar = self.menuBar()
        menubar.setGeometry(0, 0, self.width(), 30)

        file_menu = menubar.addMenu('파일(&File)')
        toolbar_file = QToolBar('&File(파일)')
        self.addToolBar(toolbar_file)

        open_action = QAction(QIcon('image/data_load.png'), '데이터 가져오기(&Data Open)', self)
        open_action.setShortcut('Ctrl+D')
        open_action.setStatusTip('데이터를 가져옵니다')
        open_action.triggered.connect(self.openFile)
        toolbar_file.addAction(open_action)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon('image/data_save.png'), '데이터 저장(&Save Data)', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('데이터를 저장합니다')
        save_action.triggered.connect(self.saveData)
        file_menu.addAction(save_action)
        toolbar_file.addAction(save_action)

        new_data_action = QAction(QIcon('image/new_data.png'), '데이터 파일 만들기(&New Data)', self)
        new_data_action.setShortcut('Ctrl+N')
        new_data_action.setStatusTip('새 데이터 만들기')
        new_data_action.triggered.connect(self.new_file)
        file_menu.addAction(new_data_action)
        toolbar_file.addAction(new_data_action)

        plot_menu = menubar.addMenu('그래프 그리기(&Plot)')
        toolbar_plot = QToolBar('&Plot(그래프그리기)')
        self.addToolBar(toolbar_plot)

        plot_1d_action = QAction(QIcon('image/plot1d.png'), '데이터 1개로 그래프 그리기(1d Plot)', self)
        plot_1d_action.setShortcut('Ctrl+1')
        plot_1d_action.setStatusTip('데이터 1개 기반 그래프 그리기')
        # triggered
        plot_menu.addAction(plot_1d_action)

        plot_2d_action = QAction(QIcon('image/plot2d.png'), '데이터 2개로 그래프 그리기(1d Plot)', self)
        plot_2d_action.setShortcut('Ctrl+2')
        plot_2d_action.setStatusTip('데이터 2개 기반 그래프 그리기')
        # triggered
        plot_menu.addAction(plot_2d_action)
        toolbar_plot.addAction(plot_2d_action)

        plot_3d_action = QAction(QIcon('image/plot3d.png'), '데이터 3개로 그래프 그리기(1d Plot)', self)
        plot_3d_action.setShortcut('Ctrl+3')
        plot_3d_action.setStatusTip('데이터 3개 기반 그래프 그리기')
        # triggered
        plot_menu.addAction(plot_3d_action)
        toolbar_plot.addAction(plot_3d_action)

        plot_mul_action = QAction(QIcon('image/mul_plot.png'), '데이터 n개로 그래프 그리기(Mul Plot)', self)
        plot_mul_action.setShortcut('Ctrl+M')
        plot_mul_action.setStatusTip('데이터 n개 기반 그래프 그리기')
        # triggered
        plot_menu.addAction(plot_mul_action)
        toolbar_plot.addAction(plot_mul_action)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Data File", "",
                                                  "Data Files (*.csv *.json *.sas *.xlsx *.txt);;All Files (*)",
                                                  options=options)

        if fileName:
            # 파일 형식에 따라 데이터 불러오기
            if fileName.endswith('.csv'):
                data = pd.read_csv(fileName)
            elif fileName.endswith('.json'):
                data = pd.read_json(fileName)
            elif fileName.endswith('.sas'):
                data = pd.read_sas(fileName)
            elif fileName.endswith('.xlsx'):
                data = pd.read_excel(fileName)
            else:
                # 기타 형식의 파일 (예: 텍스트 파일)을 읽는 방법 구현 필요
                pass

            # 데이터를 테이블 위젯에 표시
            self.show_data_in_table(data)

    def show_data_in_table(self, data):
        if data is not None:
            table = self.tab_widget.currentWidget().findChild(QTableWidget)
            if table:
                table.setRowCount(data.shape[0])
                table.setColumnCount(data.shape[1])

                for row in range(data.shape[0]):
                    for col in range(data.shape[1]):
                        item = QTableWidgetItem(str(data.iat[row, col]))
                        table.setItem(row, col, item)
        else:
            # 데이터를 불러오지 못한 경우 에러 메시지 또는 처리 방법을 추가할 수 있습니다.
            pass

    def new_file(self):
        # Create a new tab widget
        tab = QWidget()
        tab.setStyleSheet("background-color: #FFC0CB")  # Set background color
        table = QTableWidget()
        table.setRowCount(5)  # Set initial row count
        table.setColumnCount(5)  # Set initial column count

        table.resizeRowToContents(0)
        table.resizeColumnToContents(0)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tab.layout = QVBoxLayout()
        tab.layout.addWidget(table)
        tab.setLayout(tab.layout)

        # Add the tab to the existing QTabWidget (self.top_widget)
        self.tab_widget.addTab(tab, "New Tab" + str(self.tab_widget.count()))

        # Add context menu for the table
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_context_menu)

    def close_tab(self, index):
        if index >= 0:
            self.tab_widget.removeTab(index)

    def saveData(self):
        current_tab = self.tab_widget.currentWidget()
        table = current_tab.findChild(QTableWidget)
        if not table:
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Save Data as CSV", "", "CSV Files (*.csv);;All Files (*)")
        if filename:
            data = []
            for row in range(table.rowCount()):
                data_row = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item is not None:
                        data_row.append(item.text())
                    else:
                        data_row.append('')
                data.append(data_row)
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, header=False)

    def show_context_menu(self, pos):
        table = self.tab_widget.currentWidget().findChild(QTableWidget)
        if not table:
            return

        menu = QMenu(self)
        add_row_action = QAction('Add Row', self)
        add_col_action = QAction('Add Column', self)
        save_csv_action = QAction('Save as CSV', self)

        add_row_action.triggered.connect(lambda: self.add_row(table))
        add_col_action.triggered.connect(lambda: self.add_column(table))
        save_csv_action.triggered.connect(lambda: self.save_table_as_csv(table))

        menu.addAction(add_row_action)
        menu.addAction(add_col_action)
        menu.addAction(save_csv_action)

        menu.exec_(table.mapToGlobal(pos))

    def add_row(self, table):
        table.insertRow(table.rowCount())

    def add_column(self, table):
        table.insertColumn(table.columnCount())

    def save_table_as_csv(self, table):
        filename, _ = QFileDialog.getSaveFileName(self, "Save as CSV", "", "CSV Files (*.csv);;All Files (*)")
        if filename:
            data = []
            for row in range(table.rowCount()):
                data_row = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item is not None:
                        data_row.append(item.text())
                    else:
                        data_row.append('')
                data.append(data_row)
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, header=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())