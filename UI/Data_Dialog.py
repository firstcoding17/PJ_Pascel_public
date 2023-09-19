import pandas as pd
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog


class FileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Open Data File')
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        self.filepath = None

        self.file_button = QPushButton('Choose File')
        self.file_button.clicked.connect(self.openFile)
        layout.addWidget(self.file_button)

        self.open_button = QPushButton('Open')
        self.open_button.clicked.connect(self.accept)
        layout.addWidget(self.open_button)

        self.setLayout(layout)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        filepath, _ = QFileDialog.getOpenFileName(self, 'Open Data File', '',
                                                  'CSV Files (*.csv);;Excel Files (*.xlsx);;Text Files (*.txt);;SAS Files (*.sas7bdat);;JSON Files (*.json)',
                                                  options=options)

        if filepath:
            self.filepath = filepath












