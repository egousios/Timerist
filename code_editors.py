from imports import *

class HTMLEditor(Qsci.QsciScintilla):
    def __init__(self, parent=None, text=''):
        super().__init__(parent)
        self.lexer = Qsci.QsciLexerHTML(self)
        self.setLexer(self.lexer)
        self.lexer.setFont(QFont("Consolas", 15))
        self.setText(text)