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
from PyQt5.QtCore import *



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

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # 여기에 원하는 RGB 색상을 넣어주세요
        self.setPalette(palette)

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
        self.top_widget.setStyleSheet("background-color:white")
        self.top_widget.layout = QVBoxLayout()
        self.top_widget.layout.addWidget(top_label)
        self.top_widget.layout.addWidget(self.tab_widget)  # self.top_widget에 tab_widget 추가
        self.top_widget.setLayout(self.top_widget.layout)  # self.top_widget에 레이아웃 설정






        # 스플리터에 위젯 추가
        splitter.addWidget(self.top_widget)

        self.setCentralWidget(splitter)
        self.top_DockWidget()





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
        tab.setStyleSheet("background-color: gray")  # Set background color
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

    def top_DockWidget(self):
        # 도크 위젯 생성
        dock_widget = QDockWidget('Dock Widget', self)
        dock_widget.setFeatures(
            QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetFloatable)

        # 버튼을 포함한 위젯 생성
        button_widget = QWidget()
        main_layout = QVBoxLayout()  # 수직 레이아웃

        # 수평 레이아웃
        horizontal_layout = QHBoxLayout()



        # 버튼 추가 (여러 개)
        button_margin = 5  # 적절한 여백 크기로 조절
        self.button_file = QPushButton('파일(File)', self)
        self.button_file.setShortcut("Shift+1")
        self.button_file.setContentsMargins(button_margin, 0, button_margin, 0)
        self.button_file.setStyleSheet("border: none; padding: 5px;")  # 윤곽 제거

        self.button_graph = QPushButton('그래프(Graph)', self)
        self.button_graph.setShortcut("Shift+2")
        self.button_graph.setContentsMargins(button_margin, 0, button_margin, 0)
        self.button_graph.setStyleSheet("border: none; padding: 5px;")  # 윤곽 제거

        self.button_stat = QPushButton('통계(Stat)', self)
        self.button_stat.setShortcut("Shift+3")
        self.button_stat.setContentsMargins(button_margin, 0, button_margin, 0)
        self.button_stat.setStyleSheet("border: none; padding: 5px;")  # 윤곽 제거

        self.button_ML = QPushButton('머신러닝(ML)', self)
        self.button_ML.setShortcut("Shift+4")
        self.button_ML.setContentsMargins(button_margin, 0, button_margin, 0)
        self.button_ML.setStyleSheet("border: none; padding: 5px;")  # 윤곽 제거

        self.button_DL = QPushButton('딥러닝(DL)', self)
        self.button_DL.setShortcut("Shift+5")
        self.button_DL.setContentsMargins(button_margin, 0, button_margin, 0)
        self.button_DL.setStyleSheet("border: none; padding: 5px;")  # 윤곽 제거

        self.button_settings = QPushButton('설정(Setting)', self)
        self.button_settings.setShortcut("Shift+6")
        self.button_settings.setContentsMargins(button_margin, 0, button_margin, 0)
        self.button_settings.setStyleSheet("border: none; padding: 5px;")  # 윤곽 제거

        # 수평 레이아웃
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(0)  # 간격을 0으로 설정
        horizontal_layout.addWidget(self.button_file)
        horizontal_layout.addWidget(self.button_graph)
        horizontal_layout.addWidget(self.button_stat)
        horizontal_layout.addWidget(self.button_ML)
        horizontal_layout.addWidget(self.button_DL)
        horizontal_layout.addWidget(self.button_settings)



        # QLabel을 추가하여 이미지 표시
        image_label = QLabel(self)
        pixmap = QPixmap('path_to_your_image_file')  # 실제 이미지 파일의 경로로 바꿔주세요.
        image_label.setPixmap(pixmap)

        # 위에서 만든 수평 레이아웃을 수직 레이아웃에 추가
        main_layout.addLayout(horizontal_layout)
        main_layout.addWidget(image_label)

        # 다른 위젯이나 레이아웃을 추가하고 싶다면 여기에 추가

        button_widget.setLayout(main_layout)

        # 버튼을 포함한 위젯을 도크 위젯에 추가
        dock_widget.setWidget(button_widget)

        # 도크 위젯을 QMainWindow의 위쪽에 추가
        self.addDockWidget(Qt.TopDockWidgetArea, dock_widget)

        # 추가 버튼들을 수평 레이아웃에 추가
        self.additional_buttons_layout = QHBoxLayout()
        main_layout.addLayout(self.additional_buttons_layout)

        # 버튼이 클릭되면, 선택된 버튼에 따라 추가 버튼 변경
        self.button_file.clicked.connect(lambda: self.change_additional_buttons(1))
        self.button_graph.clicked.connect(lambda: self.change_additional_buttons(2))
        self.button_stat.clicked.connect(lambda: self.change_additional_buttons(3))

        # 초기에는 button1이 선택되도록 설정
        self.change_additional_buttons(1)

    def change_additional_buttons(self, button_index):
        while self.additional_buttons_layout.count():
            item = self.additional_buttons_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                layout = item.layout()
                if layout is not None:
                    self.clear_layout(layout)

        # 버튼이 클릭되면, 선택된 버튼에 따라 추가 버튼 변경
        if button_index == 1:
            # 첫 번째 위젯과 레이블
            button_load = QPushButton(self)
            button_load.setStyleSheet(
                """
                QPushButton {
                    border: none;  # 테두리 없음
                }
                """
            )
            button_load.setFlat(True)

            # QIcon을 사용하여 이미지를 아이콘으로 변환
            load_icon = QIcon('image/data_load.png')  # 이미지 파일의 경로로 바꿔주세요.

            # 버튼에 아이콘 설정
            button_load.setIcon(load_icon)
            button_load.setIconSize(QSize(100, 100))  # 아이콘 크기 설정

            # 버튼 클릭 시 동작 연결
            button_load.clicked.connect(self.openFile)

            load_label_text = QLabel('불러오기(Data Load)', self)
            load_label_text.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # 수평 가운데 정렬 및 수직 상단 정렬

            load_layout = QVBoxLayout()
            load_layout.addWidget(button_load)
            load_layout.addWidget(load_label_text)

            load_widget = QWidget()
            load_widget.setLayout(load_layout)
            button_load.setIconSize(QSize(50, 50))

            # 두 번째 위젯과 레이블
            button_save = QPushButton(self)
            button_save.setStyleSheet(
                """
                QPushButton {
                    border: none;  # 테두리 없음
                }
                """
            )
            button_save.setFlat(True)
            # QIcon을 사용하여 이미지를 아이콘으로 변환
            save_icon = QIcon('image/data_save.png')  # 이미지 파일의 경로로 바꿔주세요.

            # 버튼에 아이콘 설정
            button_save.setIcon(save_icon)
            button_save.setIconSize(QSize(100, 100))  # 아이콘 크기 설정

            # 버튼 클릭 시 동작 연결
            button_save.clicked.connect(self.saveData)

            save_text_label = QLabel('저장하기(Data Save)', self)
            save_text_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # 수평 가운데 정렬 및 수직 상단 정렬

            save_layout = QVBoxLayout()
            save_layout.addWidget(button_save)
            save_layout.addWidget(save_text_label)

            save_widget = QWidget()
            save_widget.setLayout(save_layout)

            # 세 번째 위젯과 레이블
            button_new_data = QPushButton(self)
            button_new_data.setStyleSheet(
                """
                QPushButton {
                    border: none;  # 테두리 없음
                }
                """
            )
            button_new_data.setFlat(True)
            # QIcon을 사용하여 이미지를 아이콘으로 변환
            icon_new_data = QIcon('image/new_data.png')  # 이미지 파일의 경로로 바꿔주세요.

            # 버튼에 아이콘 설정
            button_new_data.setIcon(icon_new_data)
            button_new_data.setIconSize(QSize(100, 100))  # 아이콘 크기 설정

            # 버튼 클릭 시 동작 연결
            button_new_data.clicked.connect(self.new_file)

            new_data_text_label = QLabel('새 파일(New Data)', self)
            new_data_text_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # 수평 가운데 정렬 및 수직 상단 정렬

            new_data_layout = QVBoxLayout()
            new_data_layout.addWidget(button_new_data)
            new_data_layout.addWidget(new_data_text_label)

            new_data_widget = QWidget()
            new_data_widget.setLayout(new_data_layout)



            # 세 번째 위젯과 레이블
            new_button_4 = QPushButton(self)
            new_button_4.setStyleSheet(
                """
                QPushButton {
                    border: none;  # 테두리 없음
                }
                """
            )
            new_button_4.setFlat(True)
            # QIcon을 사용하여 이미지를 아이콘으로 변환
            icon_4 = QIcon('image/working.png')  # 이미지 파일의 경로로 바꿔주세요.

            # 버튼에 아이콘 설정
            new_button_4.setIcon(icon_4)
            new_button_4.setIconSize(QSize(100, 100))  # 아이콘 크기 설정

            # 버튼 클릭 시 동작 연결
            # button_save.clicked.connect(self.onButtonClicked)

            label_4 = QLabel('업데이트 예정.....', self)
            label_4.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # 수평 가운데 정렬 및 수직 상단 정렬

            layout_4 = QVBoxLayout()
            layout_4.addWidget(new_button_4)
            layout_4.addWidget(label_4)

            widget_4 = QWidget()
            widget_4.setLayout(layout_4)

            # 수평 레이아웃에 추가
            h_layout = QHBoxLayout()

            # 첫 번째 위젯과 레이블
            h_layout.addWidget(load_widget)

            # 두 번째 위젯과 레이블
            h_layout.addWidget(save_widget)

            # 세 번째 위젯과 레이블
            h_layout.addWidget(new_data_widget)

            h_layout.addWidget(widget_4)

            # QMainWindow에 추가
            self.additional_buttons_layout.addLayout(h_layout)



        elif button_index == 2:
            for i in range(5):
                new_button = QPushButton(f'Additional Button {button_index}-{i + 1}', self)
                self.additional_buttons_layout.addWidget(new_button)
        elif button_index == 3:
            for i in range(6):
                new_button = QPushButton(f'Additional Button {button_index}-{i + 1}', self)
                self.additional_buttons_layout.addWidget(new_button)

        # 선택된 버튼에만 윤곽 표시
        self.show_button_outline(button_index)

    def show_button_outline(self, button_index):
        # 모든 버튼의 스타일 초기화
        for btn in [self.button_file, self.button_graph, self.button_stat, self.button_ML, self.button_DL,
                    self.button_settings]:
            btn.setStyleSheet("border: none; padding: 5px;")

        # 선택된 버튼에만 윤곽 표시
        if button_index == 1:
            self.button_file.setStyleSheet("border: 2px solid #000000; padding: 3px;")
        elif button_index == 2:
            self.button_graph.setStyleSheet("border: 2px solid #000000; padding: 3px;")
        elif button_index == 3:
            self.button_stat.setStyleSheet("border: 2px solid #000000; padding: 3px;")

    # 추가로 정의한 clear_layout 메서드
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                sub_layout = item.layout()
                if sub_layout is not None:
                    self.clear_layout(sub_layout)

    def output_DockWidget(self):
        print()

    def Pro_DockWidget(self):
        print()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())