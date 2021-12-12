from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit

class SearchBar(QLineEdit):
    def __init__(self, parent=None, placeholder_text='Search...'):
        super().__init__(parent=parent)
        self.placeholder_text = placeholder_text
        self.setPlaceholderText(self.placeholder_text)
        self.setStyleSheet("""
        background: #fff;
        background-image: url('images/search.png');
        background-repeat: no-repeat;
        background-position: right;
        color: #252424;
        """)
        self.search_font = QFont("Poppins", 13.5)
        self.setFont(self.search_font)