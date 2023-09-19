from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        file_menu = self.addMenu('File')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.parent.openFile)
        file_menu.addAction(open_action)
