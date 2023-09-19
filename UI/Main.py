import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import pandas as pd
from menu import MenuBar
import Data_Dialog
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import pandas as pd
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFileDialog



import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem

from menu import MenuBar
from Data_Dialog import FileDialog
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Viewer')
        self.setGeometry(100, 100, 800, 600)

        self.initMenuBar()
        self.initTableWidget()

        self.show()

    def initMenuBar(self):
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

    def initTableWidget(self):
        self.tableWidget = QTableWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def openFile(self):
        file_dialog = FileDialog(self)
        if file_dialog.exec_() == QDialog.Accepted:
            filepath = file_dialog.filepath
            if filepath:
                try:
                    if filepath.endswith('.csv'):
                        df = pd.read_csv(filepath)
                    elif filepath.endswith('.xlsx'):
                        df = pd.read_excel(filepath)
                    elif filepath.endswith('.txt'):
                        df = pd.read_csv(filepath, delimiter='\t')
                    elif filepath.endswith('.sas7bdat'):
                        from sas7bdat import SAS7BDAT
                        with SAS7BDAT(filepath) as sas_file:
                            df = sas_file.to_data_frame()
                    elif filepath.endswith('.json'):
                        df = pd.read_json(filepath)
                    # 여기에 추가적인 파일 형식을 처리하는 코드를 추가할 수 있습니다.

                    self.displayDataFrame(df)  # 이 부분에서 데이터 표시 메서드를 호출합니다.
                except Exception as e:
                    print(e)

    def displayDataFrame(self, df):
        self.tableWidget.clear()

        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])

        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                self.tableWidget.setItem(row, col, item)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    # UI 스타일시트는 조금 더 정밀하게 손봐야할 듯
    '''
    app.setStyleSheet("""
        QWidget {
            background-color: "#F9DB91";
        }
        """)
        '''
    MainWindow.show()
    sys.exit(app.exec_())

