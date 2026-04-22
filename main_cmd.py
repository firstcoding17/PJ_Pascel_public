import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 이미지 레이블 생성
        image_label_start = QLabel(self)
        pixmap_start = QPixmap('start_icon.png')  # 시작 아이콘 이미지 파일 경로로 변경
        image_label_start.setPixmap(pixmap_start)

        image_label_guide = QLabel(self)
        pixmap_guide = QPixmap('guide_icon.png')  # 가이드 아이콘 이미지 파일 경로로 변경
        image_label_guide.setPixmap(pixmap_guide)

        image_label_setting = QLabel(self)
        pixmap_setting = QPixmap('setting_icon.png')  # 설정 아이콘 이미지 파일 경로로 변경
        image_label_setting.setPixmap(pixmap_setting)

        image_label_exit = QLabel(self)
        pixmap_exit = QPixmap('exit_icon.png')  # 종료 아이콘 이미지 파일 경로로 변경
        image_label_exit.setPixmap(pixmap_exit)

        # 버튼 생성
        button_start = QPushButton('시작!(Start!)', self)
        button_guide = QPushButton('가이드라인(Guideline)', self)
        button_setting = QPushButton('설정(Settings)', self)
        button_exit = QPushButton('종료(exit)', self)
        login_button = QPushButton('로그인', self)
        signup_button = QPushButton('회원가입', self)

        # 폰트 및 밑줄 스타일 설정
        font = button_start.font()
        font.setFamily("고딕")  # 폰트 패밀리 설정
        font.setPointSize(14)  # 텍스트 크기 조절

        button_start.setFont(font)
        button_guide.setFont(font)
        button_setting.setFont(font)
        button_exit.setFont(font)
        login_button.setFont(font)
        signup_button.setFont(font)

        # 밑줄 스타일 설정
        underline_style = "text-decoration: underline;"

        button_start.setStyleSheet(underline_style)
        button_guide.setStyleSheet(underline_style)
        button_setting.setStyleSheet(underline_style)
        button_exit.setStyleSheet(underline_style)
        login_button.setStyleSheet(underline_style)
        signup_button.setStyleSheet(underline_style)

        # 버튼 및 이미지 레이아웃 생성
        layout_start = QHBoxLayout()
        layout_start.addWidget(image_label_start)
        layout_start.addWidget(button_start)

        layout_guide = QHBoxLayout()
        layout_guide.addWidget(image_label_guide)
        layout_guide.addWidget(button_guide)

        layout_setting = QHBoxLayout()
        layout_setting.addWidget(image_label_setting)
        layout_setting.addWidget(button_setting)

        layout_exit = QHBoxLayout()
        layout_exit.addWidget(image_label_exit)
        layout_exit.addWidget(button_exit)

        # 로그인과 회원가입 버튼을 가로로 배치하는 레이아웃 생성
        login_signup_layout = QHBoxLayout()
        login_signup_layout.addWidget(login_button)
        login_signup_layout.addWidget(signup_button)

        # 전체 레이아웃 생성
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_start)
        main_layout.addLayout(layout_guide)
        main_layout.addLayout(layout_setting)
        main_layout.addLayout(layout_exit)
        main_layout.addStretch(1)  # 상단 및 중단 공백
        main_layout.addLayout(login_signup_layout)
        main_layout.addStretch(1)  # 하단 공백

        # 위젯에 전체 레이아웃 설정
        self.setLayout(main_layout)

        # 윈도우 설정
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Pascel start window')

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
