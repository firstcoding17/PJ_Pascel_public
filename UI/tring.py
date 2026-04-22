from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMenu, QAction, QVBoxLayout, \
    QWidget, QFileDialog, QDialog, QLineEdit
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
from PyQt5.QtGui import *
import file_or_plot1d



'''

1. 모듈화
2. 디자인 이쁘게
3. 추가 기능
4. 디자인 패턴
5. 예외 처리

'''
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('pascel-v0.1.5alpha')
        self.setGeometry(100, 100, 1200, 800)
        self.tab_list = []
        self.data_info = []  # 딕셔너리로 데이터 정보들 저장해서 분석에 이용할 것
        self.data = None

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
        self.tab_widget.setMovable(True)  # 탭을 이동할 수 있도록 설정
        self.tab_widget.tabBarDoubleClicked.connect(self.rename_tab)
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


        open_action = QAction(QIcon('image/data_load.png'),'데이터 가져오기(&Data Open)', self)
        open_action.setShortcut('Ctrl+D')
        open_action.setStatusTip('데이터를 가져옵니다')
        open_action.triggered.connect(self.openFile)
        toolbar_file.addAction(open_action)
        file_menu.addAction(open_action)

        Save_action = QAction(QIcon('image/data_save.png'),'데이터 저장(&Save Data)',self)
        Save_action.setShortcut('Ctrl+S')
        Save_action.setStatusTip('데이터를 저장합니다')
        #triggered.connect
        file_menu.addAction(Save_action)
        toolbar_file.addAction(Save_action)

        New_Data_action = QAction(QIcon('image/new_data.png'),'데이터 파일 만들기(&New Data)',self)
        New_Data_action.setShortcut('Ctrl+N')
        New_Data_action.setStatusTip('새 데이터 만들기')
        New_Data_action.triggered.connect(self.new_file)
        file_menu.addAction(New_Data_action)
        toolbar_file.addAction(New_Data_action)

        plot_menu = menubar.addMenu('그래프 그리기(&Plot)')
        toolbar_Plot = QToolBar('&Plot(그래프그리기)')
        self.addToolBar(toolbar_Plot)


        Plot_1d_action = QAction(QIcon('image/plot1d.png'),'데이터 1개로 그래프 그리기(1d Plot)',self)
        Plot_1d_action.setShortcut('Ctrl+1')
        Plot_1d_action.setStatusTip('데이터 1개 기반 그래프 그리기')
        #triggered
        plot_menu.addAction(Plot_1d_action)

        Plot_2d_action = QAction(QIcon('image/plot2d.png'),'데이터 2개로 그래프 그리기(1d Plot)',self)
        Plot_2d_action.setShortcut('Ctrl+2')
        Plot_2d_action.setStatusTip('데이터 2개 기반 그래프 그리기')
        #triggered
        plot_menu.addAction(Plot_2d_action)
        toolbar_Plot.addAction(Plot_2d_action)

        Plot_3d_action = QAction(QIcon('image/plot3d.png'),'데이터 3개로 그래프 그리기(1d Plot)',self)
        Plot_3d_action.setShortcut('Ctrl+3')
        Plot_3d_action.setStatusTip('데이터 3개 기반 그래프 그리기')
        #triggered
        plot_menu.addAction(Plot_3d_action)
        toolbar_Plot.addAction(Plot_3d_action)

        Plot_mul_action = QAction(QIcon('image/mul_plot.png'),'데이터 n개로 그래프 그리기(Mul Plot)',self)
        Plot_mul_action.setShortcut('Ctrl+M')
        Plot_mul_action.setStatusTip('데이터 n개 기반 그래프 그리기')
        #triggered
        plot_menu.addAction(Plot_mul_action)
        toolbar_Plot.addAction(Plot_mul_action)

        # stats 메뉴추가
        stat_menu = menubar.addMenu('통계(Stat)')
        toolbar_stat = QToolBar('&Stat(통계)')
        self.addToolBar(toolbar_stat)


        univariate_action = QAction(QIcon('image/value.png'),'Univariate', self)
        univariate_action.setShortcut('Ctrl+U')
        #univariate_action.triggered.connect(self.univeraite)
        stat_menu.addAction(univariate_action)
        toolbar_stat.addAction(univariate_action)

        C_D_action = QAction(QIcon('image/random.png'),'Random variables and distributions', self)
        C_D_action.setShortcut('Ctrl+R')
        #C_D_action.triggered.connect(self.C_D)
        stat_menu.addAction(C_D_action)
        toolbar_stat.addAction(C_D_action)

        # Estimation and Testing
        Estimation_Testing_action = QAction(QIcon('image/normalization.png'),'Estimation and Testing', self)
        Estimation_Testing_action.setShortcut('Ctrl+E')
        #Estimation_Testing_action.triggered.connect(self.E_T)
        stat_menu.addAction(Estimation_Testing_action)
        toolbar_stat.addAction(Estimation_Testing_action)

        # reggression and corr
        regression_and_corr = QAction(QIcon('image/regression.png'),'regression and corr', self)
        regression_and_corr.setShortcut('Ctrl+R')
        #regression_and_corr.triggered.connect(self.R_C)
        stat_menu.addAction(regression_and_corr)
        toolbar_stat.addAction(regression_and_corr)

        ML_menu = menubar.addMenu('머신러닝(ML)')
        toolbar_ML = QToolBar('&ML(머신러닝)')
        self.addToolBar(toolbar_ML)

    def initTableWidget(self):
        self.tableWidget = QTableWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 우클릭 이벤트 연결
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.show_context_menu)

        # 컬럼 헤더 더블클릭 이벤트 연결
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.change_column_name)

    def openFile(self):
        file_dialog = file_or_plot1d.FileDialog(self)
        if file_dialog.exec_() == QDialog.Accepted:
            filepath = file_dialog.filepath
            if filepath:
                try:
                    if filepath.endswith('.csv'):
                        self.data = pd.read_csv(filepath)
                    elif filepath.endswith('.xlsx'):
                        self.data = pd.read_excel(filepath)
                    elif filepath.endswith('.json'):
                        self.data = pd.read_json(filepath)

                    tab = self.createTabWithDataFrame(self.data, filepath)
                    self.tab_widget.addTab(tab, "New Tab" + str(self.tab_widget.count()))

                    tab_info = {
                        'name': "New Tab" + str(self.tab_widget.count()),
                        'filepath': filepath
                    }
                    self.tab_list.append(tab_info)

                    data_info = {
                        'filepath': filepath,
                        'data': self.data
                    }
                    self.data_info.append(data_info)

                except Exception as e:
                    print(e)

    def createTabWithDataFrame(self, df, filepath):
        tab = QWidget()
        tab.setStyleSheet("background-color: #FFFFFF")  # Set background color
        table = QTableWidget()

        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                table.setItem(row, col, item)

        tab.layout = QVBoxLayout()
        tab.layout.addWidget(table)
        tab.setLayout(tab.layout)

        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.show_context_menu)

        return tab






    def new_file(self):
        # Create a new tab widget
        tab = QWidget()
        tab.setStyleSheet("background-color: #FFC0CB")  # Set background color
        table = QTableWidget()

        table.resizeRowToContents(0)
        table.resizeColumnToContents(0)

        table.setRowCount(5)  # Set initial row count
        table.setColumnCount(5)  # Set initial column count




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
            tab_name = self.tab_widget.tabText(index)
            tab_info = None

            for i, t_info in enumerate(self.tab_list):
                if t_info['name'] == tab_name:
                    tab_info = t_info
                    self.tab_list.pop(i)
                    break

            if tab_info:
                for i, d_info in enumerate(self.data_info):
                    if d_info['filepath'] == tab_info['filepath']:
                        self.data_info.pop(i)
                        break

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

    def rename_tab(self, index):
        # 탭 이름 변경 다이얼로그 표시
        current_tab = self.tab_widget.widget(index)
        current_name = self.tab_widget.tabText(index)
        new_name, ok = QInputDialog.getText(self, 'Rename Tab', 'New Name:', text=current_name)
        if ok:
            self.tab_widget.setTabText(index, new_name)

            # tab_info에서 해당 탭의 정보 업데이트
            for tab_info in self.tab_list:
                if tab_info['name'] == current_name:
                    tab_info['name'] = new_name
                    break

            # data_info에서 해당 파일 경로와 자료형의 정보 업데이트
            for data_info in self.data_info:
                if data_info['filepath'] == tab_info['filepath']:
                    data_info['name'] = new_name
                    break




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())