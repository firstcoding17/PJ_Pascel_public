import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 500) # 메인 윈도우 위치 및 크기 설정
        self.setWindowTitle("Main Window")

        button = QPushButton('Open Dialog', self)
        button.move(50, 50)
        button.clicked.connect(self.show_dialog)

    def show_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Window")
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
