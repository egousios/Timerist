"""
app.py
====================================
A module that combines all other source files, and runs the application.
"""

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import QCloseEvent, QFont, QIcon, QMovie, QFontDatabase
from PyQt5.QtWidgets import QFontDialog, QColorDialog, QTimeEdit, QTreeWidgetItem, QVBoxLayout
from Resource.query import Tree
from Resource.query import slice_per
from Resource.query import read_contents_from_query
from Resource.query import edit_item_from_query
from Resource.query import change_item_from_query
from Resource.query import delete_item_from_query
from Resource.time import days_in_between, StopWatch, get_current_time
from datetime import datetime
import os
import qdarkstyle

def load_from_stylesheet(file):
    '''
    A function that reads a qss stylesheet line-by-line
    and returns the data as a string for PyQt5 to read
    and parse the stylesheet.
    '''
    with open(file, "r") as f:
        data = f.read()
        f.close()
    return str(data)

def start_timer(end_date):
    current_date_time = QtCore.QDateTime.currentDateTime()
    fmt = current_date_time.toString("yyyy-MM-dd hh:mm:ss a")
    if datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]), int(end_date[9:11]), int(end_date[14:16]), int(end_date[17:19])) <= datetime(int(fmt[0:4]), int(fmt[5:7]), int(fmt[8:10]), int(fmt[9:11]), int(fmt[14:16]), int(fmt[17:19])):
        return "yes"
    else:
        return f"{days_in_between(fmt, end_date)} time left."

        
class EditTodoWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, text, sound=None, isCompletedTask=False, taskToComplete='', soundAlarm=False, newText=''):
        super().__init__(parent=Parent)
        self.title = title
        self.text = text
        self.is_completed_task = isCompletedTask
        self.task = taskToComplete
        if self.is_completed_task == False:
            self.sound = None
            self.soundAlarm = True
        self.sound = sound
        if self.sound != None:
            self.sound.play()
        self.soundAlarm = soundAlarm
        self.newText = newText
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 580
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = EditTodoTabs(self, self.text, self.task, self.soundAlarm, self.sound, newText=self.newText)
        self.setCentralWidget(self.table_widget)
        self.destroyed.connect(self.closeEvent)
    
    def closeEvent(self, event):
        if self.sound != None:
            self.sound.stop()
            self.destroy()
        else:
            self.destroy()


class EditTodoTabs(QtWidgets.QWidget):
    def __init__(self, parent, timeText, taskToComplete, soundAlarm, music, newText):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.timeText = timeText
        self.task = taskToComplete
        self.soundAlarm = soundAlarm
        self.music = music
        self.newText = newText
        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        self.tab3 = QtWidgets.QWidget()
        self.tabs.resize(500, 500)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"View")
        self.tabs.addTab(self.tab2,"Edit")
        self.tabs.addTab(self.tab3,"Schedule")
        self.tab1.layout = QtWidgets.QVBoxLayout(self)
        '''
        Editing Window -> Tab 2
        Date -> changeable
        Task -> changeable
        Status -> changeable
        '''
        self.font = QtGui.QFont()
        self.font.setPointSize(15)
        self.label = QtWidgets.QLabel(self.tab2)
        self.label.setGeometry(QtCore.QRect(30, 10, 411, 51))
        self.label.setFont(self.font)
        self.label.setText("New Date To Complete:")

        self.labelTime = QtWidgets.QLabel(self.tab1)
        self.labelTime.setGeometry(QtCore.QRect(30, 10, 411, 51))
        self.labelTime.setFont(self.font)
        self.labelTime.setText(f"Time Left To Complete: {self.task}")
        

        self.font2 = QtGui.QFont()
        if 'days' in self.timeText:
            self.font2.setPointSize(20)
        else:
            self.font2.setPointSize(30)

        self.font3 = QtGui.QFont()
        self.font3.setPointSize(10)

        self.labelTime2 = QtWidgets.QLabel(self.tab1)
        self.labelTime2.setGeometry(QtCore.QRect(30, 70, 411, 90))
        self.labelTime2.setFont(self.font2)
        if self.timeText == "Task Closed ✅":
            self.labelTime2.setStyleSheet("color: rgb(120, 255, 0);")
        elif self.timeText == "Time is Up!":
            self.labelTime2.setStyleSheet("color: rgb(240, 35, 35);")
            self.labelTime3 = QtWidgets.QLabel(self.tab1)
            self.labelTime3.setFont(self.font3)
            self.labelTime3.setText('Alarm: on')
            self.checkBox1 = QtWidgets.QCheckBox(self.tab1)
            self.checkBox1.setGeometry(QtCore.QRect(410, 75, 411, 90))
            self.checkBox1.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
            self.checkBox1.setChecked(True)
            self.checkBox1.stateChanged.connect(self.AlarmNoise)
        else:
            self.labelTime2.setStyleSheet("color: rgb(255, 42, 0);")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.showTime()

        self.datetime = QtWidgets.QCalendarWidget(self.tab2)
        self.datetime.setGeometry(QtCore.QRect(30, 70, 411, 170))
        kl = get_current_time()
        yr = kl[0:4]
        mm = kl[5:7]
        dd = kl[8:10]
        self.datetime.setMinimumDate(QtCore.QDate(int(yr), int(mm), int(dd)))
        self.label2 = QtWidgets.QLabel(self.tab2)
        self.label2.setGeometry(QtCore.QRect(30, 250, 411, 51))
        self.label2.setFont(self.font)
        self.label2.setText("New Task:")
        self.lineEdit = QtWidgets.QLineEdit(self.tab2)
        self.lineEdit.setGeometry(QtCore.QRect(30, 300, 411, 31))
        
        self.label3 = QtWidgets.QLabel(self.tab2)
        self.label3.setGeometry(QtCore.QRect(30, 350, 411, 51))
        self.label3.setFont(self.font)
        self.label3.setText("New Status:")

        if self.soundAlarm == True:
            self.gif_label = QtWidgets.QLabel(self.tab1)
            if self.timeText == "Time is Up!":
                self.labelTime3.setGeometry(QtCore.QRect(340, 75, 411, 90))
                self.gif_label.setGeometry(QtCore.QRect(240, 60, 150, 250))
            elif self.timeText == "Task Closed ✅":
                self.gif_label.setGeometry(QtCore.QRect(180, 60, 150, 250))
            else:
                self.gif_label.setGeometry(QtCore.QRect(360, 60, 150, 250))

            self.gif_label.setMinimumSize(QtCore.QSize(150, 100))
            self.gif_label.setMaximumSize(QtCore.QSize(150, 100))
            self.gif_label_rect = self.gif_label.geometry()
            self.alarm_gif_size = QtCore.QSize(min(self.gif_label_rect.width(), self.gif_label_rect.height()), min(self.gif_label_rect.width(), self.gif_label_rect.height()))
            self.alarm_gif = QtGui.QMovie("alarm.gif")
            self.alarm_gif.setScaledSize(self.alarm_gif_size)
            self.gif_label.setMovie(self.alarm_gif)
            self.alarm_gif.start()

        self.completion = QtWidgets.QCheckBox(self.tab2)
        self.completion.setGeometry(QtCore.QRect(30, 400, 200, 51))
        self.completion.setStyleSheet("QCheckBox::indicator { width: 40px; height: 40px;}")
        #self.completion.stateChanged.connect(self.checked) // sets the completion as bool

        self.pushButton = QtWidgets.QPushButton(self.tab2)
        self.pushButton.setGeometry(QtCore.QRect(30, 470, 105, 30))
        self.pushButton.setText("Save Changes")
        #self.pushButton.clicked.connect(self.add)
        self.pushButton2 = QtWidgets.QPushButton(self.tab2)
        self.pushButton2.setGeometry(QtCore.QRect(150, 470, 105, 30))
        self.pushButton2.setText("Cancel Changes")
        #self.pushButton2.clicked.connect(self.cancel)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def AlarmNoise(self):
        if self.checkBox1.isChecked():
            self.music.play()
            self.alarm_gif.setPaused(True)
            self.alarm_gif.start()
            self.labelTime3.setText('Alarm: on')
        else:
            self.music.stop()
            self.alarm_gif.setPaused(True)
            self.labelTime3.setText('Alarm: off')

    def showTime(self):
        self.labelTime2.setText(f"{self.timeText}")
        if self.newText != '':
            self.timeText = start_timer(self.newText)
        if self.timeText == 'yes':
            self.timeText = 'Time is Up!'
            self.parent.destroy()
            


class AddTodoForm(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, widget):
        super().__init__(parent=Parent)
        self.wid = widget
        self.setFixedSize(485, 550)
        self.setWindowTitle(title)
        self.centralwidget = QtWidgets.QWidget(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 411, 51))
        self.label.setFont(font)
        self.label.setText("Date To Complete:")
        self.dateLabel = QtWidgets.QLabel(self.centralwidget)
        self.dateLabel.setGeometry(QtCore.QRect(230, 20, 411, 51))
        self.datetime = QtWidgets.QCalendarWidget(self)
        self.datetime.setGeometry(QtCore.QRect(30, 90, 411, 170))
        self.datetime.clicked.connect(self.dateTell)
        kl = get_current_time()
        yr = kl[0:4]
        mm = kl[5:7]
        dd = kl[8:10]
        self.datetime.setMinimumDate(QtCore.QDate(int(yr), int(mm), int(dd)))

        self.timeToCompleteLbl = QtWidgets.QLabel(self.centralwidget)
        self.timeToCompleteLbl.setGeometry(QtCore.QRect(30, 270, 411, 51))
        self.timeToCompleteLbl.setFont(font)
        self.timeToCompleteLbl.setText("Time To Complete:")
        self.timeLabel = QtWidgets.QLabel(self.centralwidget)
        self.timeLabel.setGeometry(QtCore.QRect(230, 270, 411, 51))
        self.timeEdit = QtWidgets.QTimeEdit(self)
        self.timeEdit.setGeometry(QtCore.QRect(30, 320, 411, 31))
        self.timeEdit.timeChanged.connect(self.timeTell)


        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(30, 370, 411, 51))
        self.label2.setFont(font)
        self.label2.setText("Task:")
        self.taskLabel = QtWidgets.QLabel(self.centralwidget)
        self.taskLabel.setGeometry(QtCore.QRect(85, 410, 411, 51))
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(30, 420, 411, 31))
        self.lineEdit.returnPressed.connect(self.taskUpdate)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(30, 480, 90, 30))
        self.pushButton.setText("Ok")
        self.pushButton.clicked.connect(self.add)
        self.pushButton2 = QtWidgets.QPushButton(self)
        self.pushButton2.setGeometry(QtCore.QRect(150, 480, 90, 30))
        self.pushButton2.setText("Cancel")
        self.pushButton2.clicked.connect(self.cancel)
        self.setCentralWidget(self.centralwidget)

    def timeTell(self):
        time = self.timeEdit.time().toString("hh:mm:ss a")
        font = QtGui.QFont()
        font.setPointSize(15)
        self.timeLabel.setFont(font)
        self.timeLabel.setText(f"{time}")

    def cancel(self):
        self.destroy()

    def dateTell(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        time_label = self.datetime.selectedDate().toString("yyyy-MM-dd")
        self.dateLabel.setFont(font)
        self.dateLabel.setText(f"{time_label}")

    def taskUpdate(self):
        font = QtGui.QFont()
        font.setPointSize(15)
        task = self.lineEdit.text()
        self.taskLabel.setFont(font)
        self.taskLabel.setText(f"{task}")

    def add(self):
        date = self.datetime.selectedDate().toString("yyyy-MM-dd")
        time = self.timeEdit.time().toString("hh:mm:ss a")
        date_and_time = f"{date} {time}"
        if len(self.lineEdit.text()) < 1:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setWindowIcon(QtGui.QIcon('images/icon.png'))
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("Your task must be at least 1 character.")
            self.msg.exec_()
        else:
            data = [f'{date_and_time}', f'{self.lineEdit.text()}', "Incomplete ❌"]
            branch = Tree(branches={
                "end_time":data[0],
                "task":data[1],
                "status":data[2],
            })
            branch.save(branch.branches, id="all", path="data.txt")
            self.wid.addTopLevelItem(QTreeWidgetItem(data))

class ColorThemeWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title):
        super().__init__(parent=Parent)
        self.setFixedSize(460, 100)
        self.setWindowTitle(title)
        self.centralwidget = QtWidgets.QWidget(self)
        self.pushButton = QtWidgets.QPushButton("Dark", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 20, 110, 50))
        self.pushButton.clicked.connect(self.dark)
        self.pushButton = QtWidgets.QPushButton("Light", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(250, 20, 110, 50))
        self.pushButton.clicked.connect(self.light)
        self.setCentralWidget(self.centralwidget)

    def dark(self):
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        app.setStyleSheet(dark_stylesheet)

    def light(self):
        app.setStyleSheet(load_from_stylesheet('light-theme.qss'))




class EditWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, text):
        super().__init__(parent=Parent)
        self.setFixedSize(400, 400)
        self.setWindowTitle(f"{title}")
        self.title = title
        self.centralwidget = QtWidgets.QWidget(self)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 400, 350))
        self.textEdit.setObjectName("textEdit")
        self.font = QFont("Times", 12)
        self.textEdit.setFont(self.font)
        self.textEdit.setText(text)
        self.pushButton = QtWidgets.QPushButton("Save", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.pushButton.clicked.connect(self.save)
        self.setCentralWidget(self.centralwidget)

    def save(self):
        file = open(f'database/{self.title}', 'w', encoding='utf-8').close()
        with open(f"database/{self.title}", "w", encoding='utf-8') as f:
            f.write(self.textEdit.toPlainText())
            f.close()


class SaveWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, text):
        super().__init__(parent=Parent)
        self.setFixedSize(320, 150)
        self.setWindowTitle("Save Note As")
        self.text = text
        self.centralwidget = QtWidgets.QWidget(self)
        self.lineEdit = QtWidgets.QLineEdit("Note Title", self.centralwidget)
        self.lineEdit.setGeometry(20, 20, 280, 60)
        self.lineEdit.setObjectName("saveNoteTitle")
        self.font = QFont("Times", 12)
        self.lineEdit.setFont(self.font)
        self.pushButton = QtWidgets.QPushButton("Save", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 90, 110, 30))
        self.pushButton.clicked.connect(self.save)
        self.setCentralWidget(self.centralwidget)

    def save(self):
        with open(f"database/{self.lineEdit.text()}", "w") as f:
            f.write(self.text)


class ReadWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, text):
        super().__init__(parent=Parent)
        self.setFixedSize(400, 400)
        self.setWindowTitle(f"{title}")
        self.centralwidget = QtWidgets.QWidget(self)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.textEdit.setObjectName("textEdit")
        self.font = QFont("Times", 12)
        self.textEdit.setFont(self.font)
        self.textEdit.setText(text)
        self.setCentralWidget(self.centralwidget)

class OpenWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, textTo):
        super().__init__(parent=Parent)
        self.setFixedSize(500, 500)
        self.setWindowTitle("Select A Note")
        self.to = textTo
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 20, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setText("Notes")
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setGeometry(QtCore.QRect(100, 100, 320, 200))
        for root, dirs, files in os.walk("database"):
            for filename in files:
                QtWidgets.QListWidgetItem(filename, self.listWidget)
        self.pushButton = QtWidgets.QPushButton("Open", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 320, 100, 30))
        self.pushButton.clicked.connect(self.get)
        self.setCentralWidget(self.centralwidget)

    def get(self):
        try:
            selected = [item.text() for item in self.listWidget.selectedItems()]
            selected_str = ", ".join(selected)
            file = open(f"database/{selected_str}", "r")
            data = file.read()
            file.close()
            self.to.setText(data)
            self.destroy()
        except:
            QtWidgets.QMessageBox.about(self, "Select a Note", "Please select a note to open.")


class NotesWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent):
        super().__init__(parent=Parent)
        self.setFixedSize(500, 500)
        self.setWindowTitle("Notes")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 20, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setText("Notes")
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setGeometry(QtCore.QRect(100, 100, 320, 200))
        for root, dirs, files in os.walk("database"):
            for filename in files:
                QtWidgets.QListWidgetItem(filename, self.listWidget)
        self.pushButton = QtWidgets.QPushButton("Remove", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 320, 100, 30))
        self.pushButton.clicked.connect(self.remove)
        self.pushButton2 = QtWidgets.QPushButton("Edit", self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(210, 320, 100, 30))
        self.pushButton2.clicked.connect(self.edit)
        self.pushButton3 = QtWidgets.QPushButton("Open", self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(320, 320, 100, 30))
        self.pushButton3.clicked.connect(self.open)
        self.setCentralWidget(self.centralwidget)

    def open(self):
        try:
            selected = [item.text() for item in self.listWidget.selectedItems()]
            selected_str = ", ".join(selected)
            file = open(f"database/{selected_str}", "r")
            data = file.read()
            file.close()
            read_window = ReadWindow(self, f"{selected_str}", text=data)
            read_window.show()
        except:
            QtWidgets.QMessageBox.about(self, "Select a Note", "Please select a note so that an action can be completed.")


    def edit(self):
        try:
            selected = [item.text() for item in self.listWidget.selectedItems()]
            selected_str = ", ".join(selected)
            file = open(f"database/{selected_str}", "r")
            data = file.read()
            file.close()
            edit_window = EditWindow(self, f"{selected_str}", f"{data}")
            edit_window.show()
        except:
            QtWidgets.QMessageBox.about(self, "Select a Note", "Please select a note so that an action can be completed.")

    def remove(self):
        for item in self.listWidget.selectedItems():
            self.listWidget.takeItem(self.listWidget.row(item))
            os.remove(f"database/{item.text()}")


class Ui_Timerist(object):
    def setupUi(self, Timerist, sound):
        Timerist.setObjectName("Timerist")
        Timerist.setFixedSize(920, 600)
        Timerist.setWindowIcon(QtGui.QIcon('images/icon.png'))
        Timerist.destroyed.connect(self.closeEvent)
        self.sound = sound
        self.centralwidget = QtWidgets.QWidget(Timerist)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(570, 2, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(100, 2, 241, 51))
        self.label2.setFont(font)
        self.label2.setText("To Do List")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(410, 60, 491, 281))
        self.textEdit.setObjectName("textEdit")
        self.font = QFont("Times", 12)
        self.textEdit.setFont(self.font)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(20, 60, 360, 192))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setHeaderLabels(["Date", "Task", "Status"])
        file = open("data.txt", "r", encoding='utf-8')
        data = file.readlines()
        file.close()
        data = [line.replace('\n', '') for line in data]
        desired_lines = data[0::1]
        fov = slice_per(desired_lines, 3)
        for e in fov:
            self.treeWidget.addTopLevelItem(QTreeWidgetItem(e))
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(410, 350, 81, 20)) ###### 40
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(470, 350, 81, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(530, 350, 81, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(750, 350, 61, 22))
        self.toolButton.setObjectName("toolButton")
        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setGeometry(QtCore.QRect(610, 350, 61, 22))
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setGeometry(QtCore.QRect(680, 350, 61, 22))
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_4 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_4.setGeometry(QtCore.QRect(820, 350, 61, 22))
        self.toolButton_4.setObjectName("toolButton_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 260, 83, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(115, 260, 83, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(205, 260, 83, 28))
        self.pushButton_3.setText("Update")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(295, 260, 83, 28))
        self.pushButton_4.setText("View")
        self.pushButton_3.clicked.connect(self.update_todo)
        self.pushButton_4.clicked.connect(self.view_todo)
        Timerist.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Timerist)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuNotes = QtWidgets.QMenu(self.menubar)
        self.menuNotes.setObjectName("menuNotes")
        Timerist.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Timerist)
        self.statusbar.setObjectName("statusbar")
        Timerist.setStatusBar(self.statusbar)
        self.actionColor_Theme = QtWidgets.QAction(Timerist)
        self.actionColor_Theme.setObjectName("actionColor_Theme")
        self.actionView = QtWidgets.QAction(Timerist)
        self.actionView.setObjectName("actionView")
        self.menuSettings.addAction(self.actionColor_Theme)
        self.menuNotes.addAction(self.actionView)
        self.actionColor_Theme.triggered.connect(self.color_theme)
        self.actionView.triggered.connect(self.view)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuNotes.menuAction())
        self.retranslateUi(Timerist)
        QtCore.QMetaObject.connectSlotsByName(Timerist)
    

    def retranslateUi(self, Timerist):
        _translate = QtCore.QCoreApplication.translate
        Timerist.setWindowTitle(_translate("Timerist", "Timerist"))
        self.label.setText(_translate("Timerist", "Notes"))
        self.checkBox.setText(_translate("Timerist", "Bold"))
        self.checkBox.clicked.connect(lambda x: self.textEdit.setFontWeight(self.font.Bold if x else self.font.Normal))
        self.checkBox_2.setText(_translate("Timerist", "Italic"))
        self.checkBox_2.clicked.connect(self.italic)
        self.checkBox_3.setText(_translate("Timerist", "Underline"))
        self.checkBox_3.clicked.connect(self.underline)
        self.toolButton.setText(_translate("Timerist", "Font..."))
        self.toolButton.clicked.connect(self.FontChange)
        self.toolButton_2.setText(_translate("Timerist", "Create"))
        self.toolButton_2.clicked.connect(self.Save)
        self.toolButton_3.setText(_translate("Timerist", "Open"))
        self.toolButton_3.clicked.connect(self.open)
        self.toolButton_4.setText(_translate("Timerist", "Color..."))
        self.toolButton_4.clicked.connect(self.color_change)
        self.pushButton.setText(_translate("Timerist", "Add"))
        self.pushButton.clicked.connect(self.add_todo)
        self.pushButton_2.setText(_translate("Timerist", "Remove"))
        self.pushButton_2.clicked.connect(self.remove_todo)
        self.menuSettings.setTitle(_translate("Timerist", "Settings"))
        self.menuNotes.setTitle(_translate("Timerist", "Notes"))
        self.actionColor_Theme.setText(_translate("Timerist", "Color Theme"))
        self.actionView.setText(_translate("Timerist", "View"))
        
    def italic(self):
        self.textEdit.setFontItalic(True)
        
    def underline(self):
        self.textEdit.setFontUnderline(True)

    def color_theme(self):
        cWindow = ColorThemeWindow(Timerist, "Color Theme")
        cWindow.show()

    def add_todo(self):
        add = AddTodoForm(Timerist, "Add Todo", self.treeWidget)
        add.show()

    def remove_todo(self):
        items = self.treeWidget.selectedItems()
        for item in items:
            item_text = [item.text(0), item.text(1), item.text(2)]
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
            delete_item_from_query(item_text, path='data.txt')

    def update_todo(self):
        items = self.treeWidget.selectedItems()
        for item in items:
            item_text_prev = [item.text(0), item.text(1), item.text(2)]
            item.setText(2, "Completed ✅")
            item_text_new = [item.text(0), item.text(1), item.text(2)]
            change_item_from_query(item_text_prev, item_text_new, 'data.txt')

    def view_todo(self):
        items = self.treeWidget.selectedItems()
        for item in items:
            item_text = [item.text(0), item.text(1), item.text(2)]
            task_name = item_text[1]
            text_data = start_timer(item_text[0])
            completion_of_task = item_text[2]
            is_task_completed = False
            task_closed_id = "Task Closed ✅"
            task_time_is_up_id = "Time is Up!"
            if completion_of_task == "Completed ✅":
                is_task_completed = True
            else:
                is_task_completed = False
            if text_data == "yes":
                if is_task_completed == True:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_closed_id, taskToComplete=item_text[1])
                    edit_todo_win.show()
                elif is_task_completed == False:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_time_is_up_id, self.sound, is_task_completed, taskToComplete=item_text[1], soundAlarm=True)
                    edit_todo_win.show()
            else:
                if is_task_completed == True:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_closed_id, taskToComplete=item_text[1])
                    edit_todo_win.show()
                elif is_task_completed == False:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", text_data, taskToComplete=item_text[1], soundAlarm=True, newText=item_text[0])
                    edit_todo_win.show()

    def color_change(self):
        dialog = QColorDialog().getColor().getRgb()
        self.textEdit.setStyleSheet(f"color:rgba{dialog}")

    def FontChange(self):
        self.Fontdlg = QFontDialog()
        font, ok = self.Fontdlg.getFont()
        if ok:
            self.textEdit.setFont(font)

    def open(self):
        open = OpenWindow(Timerist, self.textEdit)
        open.show()
        

    def Save(self):
        save = SaveWindow(Timerist, self.textEdit.toPlainText())
        save.show()

    def view(self):
        notes_window = NotesWindow(Timerist)
        notes_window.show()

    def closeEvent(self):
        Timerist.destroySubWindows()

# Create the necessary instances of our classes in order to run the GUI.    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setPalette(QtWidgets.QApplication.style().standardPalette())
    app.setStyleSheet(load_from_stylesheet('light-theme.qss'))
    sound_file = 'alarm.wav'
    sound = QtMultimedia.QSoundEffect()
    sound.setSource(QtCore.QUrl.fromLocalFile(sound_file))
    sound.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
    sound.setVolume(50)
    Timerist = QtWidgets.QMainWindow()
    ui = Ui_Timerist()
    ui.setupUi(Timerist, sound)
    Timerist.show()
    sys.exit(app.exec_())
