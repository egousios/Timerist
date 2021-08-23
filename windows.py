from PyQt5.QtPrintSupport import QPrintDialog
from imports import *
from windows import *
from code_editors import *
from edit_tabs import *

class EditTodoWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, text, sound=None, isCompletedTask=False, taskToComplete='', soundAlarm=False, newText='', isTimeShowing=False, prev_date='', prev_status='', tree=None):
        super().__init__(parent=Parent)
        self.title = title
        self.text = text
        self.is_completed_task = isCompletedTask
        self.task = taskToComplete
        if self.is_completed_task == False:
            self.sound = None
            self.soundAlarm = True
        self.sound = sound
        self.soundAlarm = soundAlarm
        self.newText = newText
        self.isTimeShowing = isTimeShowing
        self.prev_date = prev_date
        self.prev_status = prev_status
        self.tree = tree
        if self.sound != None:
            if self.isTimeShowing == False:
                self.sound.play()
        self.left = 0
        self.top = 0
        self.width = 520
        self.height = 240
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = EditTodoTabs(self, self.text, self.task, self.soundAlarm, self.sound, newText=self.newText, prev_date=self.prev_date, prev_status=self.prev_status, tree=self.tree)
        self.setCentralWidget(self.table_widget)
        self.destroyed.connect(self.closeEvent)
    
    def closeEvent(self, event):
        if self.sound != None:
            self.sound.stop()
            self.destroy()
        else:
            self.destroy()

class CreateWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, text=None, database=None, user=None):
        super().__init__(parent=Parent)
        self.user = user
        self.setFixedSize(320, 150)
        self.setWindowTitle("New document")
        self.text = text
        self.database = database
        self.centralwidget = QtWidgets.QWidget(self)
        self.lineEdit = QtWidgets.QLineEdit("Document Title", self.centralwidget)
        self.lineEdit.setObjectName("line")
        self.lineEdit.setGeometry(20, 20, 280, 60)
        self.font = QFont("Times", 12)
        self.lineEdit.setFont(self.font)
        self.pushButton = QtWidgets.QPushButton("Create", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 90, 110, 30))
        self.pushButton.clicked.connect(self.save)
        self.setCentralWidget(self.centralwidget)

    def save(self):
        selected = f"users/{self.user}/database/{self.lineEdit.text()}.html"
        if os.path.isfile(selected):
            QtWidgets.QMessageBox.critical(self, "Error!", "A document already exists with this title.")
        else:
            with open(selected, "a", encoding='utf-8') as f:
                f.write(" ")
                f.close()
            if self.database != None:
                self.database.addItem(QListWidgetItem(f'{self.lineEdit.text()}.html'))

class EmbedHtmlWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, html, filename):
        super().__init__(parent=Parent)
        self.setWindowTitle(title)
        self.widget = QtWidgets.QWidget()
        self.main_l = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.layout2 = QHBoxLayout()
        self.tool_btn_size = QtCore.QSize(35, 35)


        ## reading the html data
        with open(filename, 'r', encoding='utf-8') as f:
            textdata = f.read()
            f.close()


        self.htmlPreview = HTMLEditor(self.widget, text=textdata)
        self.htmlPreview.setReadOnly(True)

        self.htmlPreviewLbl = QtWidgets.QLabel("Embed HTML: ")
        self.htmlPreviewLbl.setStyleSheet("margin-left: 50px;")
        ftg = QFont()
        ftg.setPointSize(20)
        self.htmlPreviewLbl.setFont(ftg)

        self.browserLbl = QtWidgets.QLabel("Browser Preview: ")
        ftg = QFont()
        ftg.setPointSize(20)
        self.browserLbl.setFont(ftg)

        self.copyHtmlBtn = QtWidgets.QToolButton()
        self.copyHtmlBtn.setStyleSheet("margin-right: 50px;")
        self.copyHtmlBtn.setToolTip("Copy")
        self.copyHtmlBtn.setIcon(QIcon("images/copy.png"))
        self.copyHtmlBtn.setIconSize(self.tool_btn_size)
        self.copyHtmlBtn.clicked.connect(self.copyHtml)

        self.webbrowser = QtWebEngineWidgets.QWebEngineView(self.widget)
        self.webbrowser.setUrl(QtCore.QUrl.fromLocalFile(os.path.abspath(filename)))

        self.setCentralWidget(self.widget)
        self.layout2.addWidget(self.htmlPreviewLbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout2.addWidget(self.copyHtmlBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout2.addStretch(2)
        self.layout2.addWidget(self.browserLbl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout2.addSpacerItem(QSpacerItem(50, 0))
        self.layout2.addStretch(2)
        self.main_l.addLayout(self.layout2)
        self.layout.addWidget(self.htmlPreview, 50)
        self.layout.addWidget(self.webbrowser, 50)
        self.main_l.addLayout(self.layout)

        self.widget.setLayout(self.main_l)
        scrollWidget = QtWidgets.QScrollArea()
        scrollWidget.setWidget(self.widget)
        scrollWidget.setWidgetResizable(True)
        self.setCentralWidget(scrollWidget)

    def copyHtml(self):
        self.htmlPreview.selectAll()
        self.htmlPreview.copy()

    


class ReadWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, text, user):
        super().__init__(parent=Parent)
        self.user = user
        self.resize(400, 400)
        self.title = title
        self.setWindowTitle(f"{title}")
        self.centralwidget = QtWidgets.QWidget()
        self.layout = QHBoxLayout()
        self.layout2 = QVBoxLayout()
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.textEdit.setObjectName("textEdit")
        self.font = QFont("Times", 12)
        self.tool_btn_size = QtCore.QSize(50, 50)
        self.textEdit.setFont(self.font)
        self.textEdit.setText(text)

        self.pushButtonPrint = QtWidgets.QToolButton(self.centralwidget)
        self.pushButtonPrint.setIcon(QtGui.QIcon("images/print.png"))
        self.pushButtonPrint.setToolTip("Print")
        self.pushButtonPrint.setIconSize(self.tool_btn_size)
        self.pushButtonPrint.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.pushButtonPrint.clicked.connect(self.printDialog)

        self.pushButtonEmbed = QtWidgets.QToolButton(self.centralwidget)
        self.pushButtonEmbed.setIcon(QtGui.QIcon("images/embed.png"))
        self.pushButtonEmbed.setToolTip("Embed Html")
        self.pushButtonEmbed.setIconSize(self.tool_btn_size)
        self.pushButtonEmbed.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.pushButtonEmbed.clicked.connect(self.HtmlDialog)

        self.setCentralWidget(self.centralwidget)
        self.layout.addWidget(self.pushButtonPrint, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButtonEmbed, alignment=Qt.AlignHCenter)
        #self.layout.addStretch()
        self.layout2.addLayout(self.layout)
        self.layout2.addWidget(self.textEdit)
        self.centralwidget.setLayout(self.layout2)
        scrollWidget = QtWidgets.QScrollArea()
        scrollWidget.setWidget(self.centralwidget)
        scrollWidget.setWidgetResizable(True)
        self.setCentralWidget(scrollWidget)

    def printDialog(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.textEdit.document().print_(dialog.printer())

    def HtmlDialog(self):
        dialog = EmbedHtmlWindow(self, "Embed Html", self.textEdit, filename=f"users/{self.user}/database/{self.title}")
        dialog.show()

class OpenWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, textTo, user, winTitle=None):
        super().__init__(parent=Parent)
        self.user = user
        self.setFixedSize(500, 300)
        self.setWindowTitle("Open A Document")
        self.to = textTo
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 20, 211, 51))
        self.winTitle = winTitle
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setText("Documents: ")
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setGeometry(QtCore.QRect(100, 100, 320, 200))
        for root, dirs, files in os.walk(f"users/{self.user}/database"):
            for filename in files:
                QtWidgets.QListWidgetItem(filename, self.listWidget)
        self.pushButton = QtWidgets.QPushButton("Open", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 320, 100, 30))
        self.pushButton.clicked.connect(self.get)

        lay = QVBoxLayout()
        lay.addWidget(self.label, alignment=Qt.AlignCenter)
        lay.addWidget(self.listWidget, alignment=Qt.AlignCenter)
        lay.addWidget(self.pushButton, alignment=Qt.AlignCenter)
        lay.addStretch(3)
        self.centralwidget.setLayout(lay)
        self.setCentralWidget(self.centralwidget)
        self.opened = False


    def get(self):
        try:
            selected = [item.text() for item in self.listWidget.selectedItems()]
            selected_str = ", ".join(selected)
            file = open(f"users/{self.user}/database/{selected_str}", "r", encoding="utf-8")
            self.filename = f"users/{self.user}/database/{selected_str}"
            data = file.read()
            file.close()
            self.to.setText(data)
            if self.winTitle != None:
                try:
                    self.winTitle.setWindowTitle(selected_str)
                except Exception as E:
                    print(E)
            else:
                print("nope")
            self.opened = True
            self.destroy()
            return self.filename 
        except:
            QtWidgets.QMessageBox.warning(self, "Select a document", "Please select a document to open.")

    def isOpened(self):
        return self.opened
