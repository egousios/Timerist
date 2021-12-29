from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QColorDialog, QFrame, QHBoxLayout, QPushButton, QWidget, QLabel, QVBoxLayout
import sys
sys.path.insert(0, "../")
from utils import hex_to_rgb

class PreviewColor(QFrame):
    def __init__(self, parent=None, color=None):
        super().__init__(parent)
        # Give the frame a border so that we can see it.
        self.setFrameStyle(1)
        if color != None:
            self.setStyleSheet(f"background-color: {color};")

    def resizeEvent(self, event):
        # Create a square base size of 10x10 and scale it to the new size
        # maintaining aspect ratio.
        new_size = QSize(10, 10)
        new_size.scale(event.size(), Qt.KeepAspectRatio)
        self.resize(new_size)

class ColorValueShower(QWidget):
    def __init__(self, parent=None, widget_font=None, current_value=None):
        super().__init__(parent=parent)
        self.widget_layout = QHBoxLayout()
        self.current_value = current_value
        self.current_value_lbl = QLabel()
        self.current_value_lbl.setText(self.current_value)
        if widget_font != None:
            self.current_value_lbl.setFont(widget_font)
        self.preview_color = PreviewColor(color=self.current_value)
        self.change_color_btn = QPushButton()
        self.change_color_btn.setText("Select...")
        self.change_color_btn.setFont(widget_font)
        self.change_color_btn.clicked.connect(self.change_color)
        self.widget_layout.addWidget(self.current_value_lbl)
        self.widget_layout.addWidget(self.preview_color)
        self.widget_layout.addWidget(self.change_color_btn)
        self.setLayout(self.widget_layout)

    def set_color(self, color):
        self.current_value = color
        self.current_value_lbl.setText(self.current_value)
        self.preview_color.setStyleSheet(f"background-color: {self.current_value}")

    def change_color(self):
        dlg = QColorDialog()
        color = dlg.getColor()
        if color.isValid():
            self.current_value = color.name()
            self.current_value_lbl.setText(self.current_value)
            self.preview_color.setStyleSheet(f"background-color: {self.current_value};")

