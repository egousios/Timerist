from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit

class SingleLineTextInput(QLineEdit):
    def __init__(self, parent=None, text_input_font=None, height=None):
        super().__init__(parent=parent)
        self.Height = height
        self.setStyleSheet("""
        QLineEdit {
            background: #fff;
            color: #252424;
            border: 2px solid #233cad;
            border-radius: 5px;
            font-family: 15pt OpenSans-SemiBold;
        }
        QLineEdit:hover {
            background: #fff;
            color: #252424;
            border: 2px solid #4187a6;
            border-radius: 5px;
            font-family: 15pt OpenSans-SemiBold;
        }
        """)
        self.setFont(text_input_font)
        if self.Height != None:
            self.setFixedHeight(self.Height)