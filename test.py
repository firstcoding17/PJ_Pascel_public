import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QPushButton

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('탭 관리 예제')
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget(self)
        self.tab_list = []  # 탭을 저장할 리스트

        new_tab_button = QPushButton("새 탭", self)
        new_tab_button.move(100,100)
        new_tab_button.clicked.connect(self.addNewTab)

        close_tab_button = QPushButton("선택한 탭 닫기", self)
        close_tab_button.clicked.connect(self.closeSelectedTab)

        self.setCentralWidget(self.tab_widget)

    def addNewTab(self):
        new_tab = QWidget()
        tab_text = '새로운 탭 {}'.format(len(self.tab_list) + 1)
        self.tab_widget.addTab(new_tab, tab_text)
        self.tab_list.append(new_tab)  # 탭을 리스트에 추가

    def closeSelectedTab(self):
        # 현재 선택된 탭을 닫음
        selected_tab = self.tab_widget.currentWidget()
        if selected_tab in self.tab_list:
            self.tab_list.remove(selected_tab)
            self.tab_widget.removeTab(self.tab_widget.currentIndex())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
