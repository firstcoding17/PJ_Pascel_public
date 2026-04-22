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
from PyQt5.QtCore import Qt, QEvent
import Pascel_v0_1_5alpha as main



class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):


        gradient = QLinearGradient(0,0,self.width(),0)
        gradient.setColorAt(0, QColor(52, 152, 219))  # 시작 색상
        gradient.setColorAt(1, QColor(26, 188, 158))  # 종료 색상

        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setBrush(self.backgroundRole(), gradient)
        self.setPalette(pal)

        # 버튼 생성
        button_start = QPushButton('시작!(Start!)', self)
        button_start.setStyleSheet("background-color: transparent; border: none;")
        button_guide = QPushButton('가이드라인(Guideline)', self)
        button_guide.setStyleSheet("background-color: transparent; border: none;")
        button_setting = QPushButton('설정(Settings)', self)
        button_setting.setStyleSheet("background-color: transparent; border: none;")
        button_exit = QPushButton('종료(exit)', self)
        button_exit.setStyleSheet("background-color: transparent; border: none;")
        login_button = QPushButton('로그인', self)
        login_button.setStyleSheet("background-color: transparent; border: none;")
        signup_button = QPushButton('회원가입', self)
        signup_button.setStyleSheet("background-color: transparent; border: none;")

        font = button_start.font()
        font.setPointSize(14)  # 텍스트 크기 조절
        button_start.setFont(font)
        button_guide.setFont(font)
        button_setting.setFont(font)
        button_exit.setFont(font)
        login_button.setFont(font)
        signup_button.setFont(font)


        # 버튼 레이아웃 생성
        button_layout = QVBoxLayout()
        button_layout.addWidget(button_start)
        button_layout.addWidget(button_guide)
        button_layout.addWidget(button_setting)
        button_layout.addWidget(button_exit)

        # 로그인과 회원가입 버튼을 가로로 배치하는 레이아웃 생성
        login_signup_layout = QHBoxLayout()
        login_signup_layout.addWidget(login_button)
        login_signup_layout.addWidget(signup_button)

        # 전체 레이아웃 생성
        main_layout = QVBoxLayout()
        main_layout.setSpacing(25)
        main_layout.addStretch(1)  # 상단 공백
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)  # 중단 공백
        main_layout.addLayout(login_signup_layout)
        main_layout.addStretch(1)  # 하단 공백

        # 위젯에 전체 레이아웃 설정
        self.setLayout(main_layout)

        # 윈도우 설정
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Pascel start window')

        # 이벤트 필터 설정
        self.installEventFilter(self)

        self.show()

        self.installEventFilter(self)

        #버튼 연결
        button_start.clicked.connect(self.openMainWindow)
        button_exit.clicked.connect(self.close)

        self.main_window = None

    def openMainWindow(self):
        self.main_window = main.MyWindow()
        self.main_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
