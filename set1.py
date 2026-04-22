from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 하단 버튼 초기값으로 생성
        self.bottom_buttons = [
            QPushButton('Default Button 1', self),
            QPushButton('Default Button 2', self),
            QPushButton('Default Button 3', self),
        ]

        bottom_layout = QVBoxLayout()
        for btn in self.bottom_buttons:
            bottom_layout.addWidget(btn)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_layout)

        # 처음에는 Default 버튼이 보이도록 설정
        self.set_bottom_buttons(0)

        # 상단 도크 위젯 생성
        self.top_DockWidget()

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
        button1 = QPushButton('Button 1', self)
        button2 = QPushButton('Button 2', self)
        button3 = QPushButton('Button 3', self)

        horizontal_layout.addWidget(button1)
        horizontal_layout.addWidget(button2)
        horizontal_layout.addWidget(button3)

        # QLabel을 추가하여 이미지 표시
        image_label = QLabel(self)
        pixmap = QPixmap('path_to_your_image_file')  # 실제 이미지 파일의 경로로 바꿔주세요.
        image_label.setPixmap(pixmap)

        # 위에서 만든 수평 레이아웃을 수직 레이아웃에 추가
        main_layout.addLayout(horizontal_layout)
        main_layout.addWidget(image_label)

        # 다른 위젯이나 레이아웃을 추가하고 싶다면 여기에 추가

        # 수직 레이아웃을 button_widget에 설정
        button_widget.setLayout(main_layout)

        # 버튼을 포함한 위젯을 도크 위젯에 추가
        dock_widget.setWidget(button_widget)

        # 도크 위젯을 QMainWindow의 위쪽에 추가
        self.addDockWidget(Qt.TopDockWidgetArea, dock_widget)

        # 하위 VBox 추가
        self.additional_vbox = QVBoxLayout()
        button4 = QPushButton('Additional Button 1', self)
        button5 = QPushButton('Additional Button 2', self)
        self.additional_vbox.addWidget(button4)
        self.additional_vbox.addWidget(button5)

        # 초기에는 button1이 선택되도록 설정
        self.set_additional_buttons(1)

        # 버튼이 클릭되면, 선택된 버튼에 따라 추가 버튼 변경
        button1.clicked.connect(lambda: self.set_additional_buttons(1))
        button2.clicked.connect(lambda: self.set_additional_buttons(2))
        button3.clicked.connect(lambda: self.set_additional_buttons(3))

    def set_bottom_buttons(self, index):
        # 선택된 버튼의 index에 해당하는 하단 버튼들로 변경
        button_layout = QVBoxLayout()
        for btn in self.bottom_buttons[index]:
            button_layout.addWidget(btn)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        self.top_dock_widget.setWidget(button_widget)

    def change_bottom_buttons(self, button_index):
        # 버튼이 클릭되면, 선택된 버튼에 따라 하단 버튼 변경
        if button_index == 1:
            self.bottom_buttons = [
                [QPushButton('Button 1-1', self), QPushButton('Button 1-2', self), QPushButton('Button 1-3', self)],
                [QPushButton('Button 1-4', self), QPushButton('Button 1-5', self)],
            ]
        elif button_index == 2:
            self.bottom_buttons = [
                [QPushButton('Button 2-1', self), QPushButton('Button 2-2', self)],
                [QPushButton('Button 2-3', self), QPushButton('Button 2-4', self), QPushButton('Button 2-5', self)],
            ]
        elif button_index == 3:
            self.bottom_buttons = [
                [QPushButton('Button 3-1', self), QPushButton('Button 3-2', self)],
                [QPushButton('Button 3-3', self), QPushButton('Button 3-4', self), QPushButton('Button 3-5', self)],
            ]
        elif button_index == 4:
            self.bottom_buttons = [
                [QPushButton('Button 4-1', self), QPushButton('Button 4-2', self), QPushButton('Button 4-3', self)],
            ]

        self.set_bottom_buttons(0)

    def set_additional_buttons(self, button_index):
        # 버튼이 클릭되면, 선택된 버튼에 따라 추가 버튼 변경
        if button_index == 1:
            self.additional_vbox.itemAt(0).widget().setText('Additional Button 1-1')
            self.additional_vbox.itemAt(1).widget().setText('Additional Button 1-2')
        elif button_index == 2:
            self.additional_vbox.itemAt(0).widget().setText('Additional Button 2-1')
            self.additional_vbox.itemAt(1).widget().setText('Additional Button 2-2')
        elif button_index == 3:
            self.additional_vbox.itemAt(0).widget().setText('Additional Button 3-1')
            self.additional_vbox.itemAt(1).widget().setText('Additional Button 3-2')

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
