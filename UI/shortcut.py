from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

class Shortcut(QShortcut):
    def __init__(self, parent):
        super().__init__(QKeySequence("Ctrl+Q"), parent)
        self.activated.connect(parent.close)