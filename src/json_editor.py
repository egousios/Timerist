import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciScintilla, QsciLexerJSON


class SimpleJSONEditor(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(SimpleJSONEditor, self).__init__(parent)


        font = QFont()
        font.setFamily('Consolas')
        font.setFixedPitch(True)
        font.setPointSize(15)
        self.setFont(font)
        self.setMarginsFont(font)


        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))


        self.setMarginSensitivity(1, True)

        self.markerDefine(QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#3d3c38"),
            self.ARROW_MARKER_NUM)



        self.setBraceMatching(QsciScintilla.StrictBraceMatch)


        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))


        lexer = QsciLexerJSON()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)

        text = bytearray(str.encode("Arial"))
        
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, text)


        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)


        self.setMinimumSize(600, 450)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)