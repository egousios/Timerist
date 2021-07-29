"""
app.py
====================================
A module that combines all other source files, and runs the application.
"""

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtPrintSupport, QtWebEngineWidgets, Qsci
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import QCloseEvent, QCursor, QDesktopServices, QFont, QIcon, QMovie, QFontDatabase, QPainter, QPixmap, QTextImageFormat, QTextListFormat, QTextTableFormat, QTextCursor
from PyQt5.QtWidgets import QApplication, QCommandLinkButton, QFontDialog, QColorDialog, QFormLayout, QLabel, QListWidgetItem, QSpacerItem, QTextEdit, QTimeEdit, QTreeWidgetItem, QVBoxLayout, QHBoxLayout
from backend.query import Tree
from backend.query import slice_per
from backend.query import read_contents_from_query
from backend.query import edit_item_from_query
from backend.query import change_item_from_query
from backend.query import delete_item_from_query
from backend.query import edit_item
from backend.query import return_contents_from_query
from backend.time import days_in_between, StopWatch, get_current_time
from datetime import datetime
import os
import sys
import qdarkgraystyle
import qtwidgets
from qtwidgets import AnimatedToggle

class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)

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


class EditTodoTabs(QtWidgets.QWidget):
    def __init__(self, parent, timeText, taskToComplete, soundAlarm, music, newText, prev_date, prev_status, tree, Sound=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()
        self.timeText = timeText
        self.task = taskToComplete
        self.soundAlarm = soundAlarm
        self.music = music
        self.newText = newText
        self.prev_date = prev_date
        self.tree = tree
        if 'm' in self.prev_date:
            self.prev_time = self.prev_date[11:-2]+self.prev_date[20]+self.prev_date[21]
        else:
            self.prev_time = self.prev_date[11:-2]
        self.prev_status = prev_status


        self.tab1 = QtWidgets.QWidget()

        self.font = QtGui.QFont()
        self.font.setPointSize(15)

        self.labelTime = QtWidgets.QLabel(self.tab1)
        self.labelTime.setGeometry(QtCore.QRect(30, 10, 411, 51))
        if len(self.task) < 14:
            self.labelTime.setFont(self.font)
        else:
            self.nfont = QtGui.QFont()
            self.nfont.setPointSize(13)
            self.labelTime.setFont(self.nfont)
        self.labelTime.setText(f"Time Left To Complete: {self.task}")
        

        self.font2 = QtGui.QFont()
        if 'days' in self.timeText or 'day' in self.timeText:
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
            self.checkBox1.setGeometry(QtCore.QRect(420, 75, 411, 90))
            self.checkBox1.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
            self.checkBox1.setChecked(True)
            self.checkBox1.stateChanged.connect(self.AlarmNoise)
        else:
            self.labelTime2.setStyleSheet("color: rgb(255, 42, 0);")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.showTime()


        if self.soundAlarm == True:
            self.gif_label = QtWidgets.QLabel(self.tab1)
            if self.timeText == "Time is Up!":
                self.labelTime3.setGeometry(QtCore.QRect(350, 75, 411, 90))
                self.gif_label.setGeometry(QtCore.QRect(255, 60, 150, 250))
            elif self.timeText == "Task Closed ✅":
                self.gif_label.setGeometry(QtCore.QRect(180, 60, 150, 250))
            else:
                self.gif_label.setGeometry(QtCore.QRect(360, 60, 150, 250))

            self.gif_label.setMinimumSize(QtCore.QSize(150, 100))
            self.gif_label.setMaximumSize(QtCore.QSize(150, 100))
            self.gif_label_rect = self.gif_label.geometry()
            self.alarm_gif_size = QtCore.QSize(min(self.gif_label_rect.width(), self.gif_label_rect.height()), min(self.gif_label_rect.width(), self.gif_label_rect.height()))
            self.alarm_gif = QtGui.QMovie("../alarm.gif")
            self.alarm_gif.setScaledSize(self.alarm_gif_size)
            self.gif_label.setMovie(self.alarm_gif)
            self.alarm_gif.start()

        self.layout.addWidget(self.tab1)
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


    def cancel(self):
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
            branch.save(branch.branches, id="all", path=f"../users/{USER}/data.txt")
            self.wid.addTopLevelItem(QTreeWidgetItem(data))


class EditWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, text, database=None):
        super().__init__(parent=Parent)
        self.resize(400, 400)
        self.setWindowTitle(f"{title}")
        self.title = title
        self.database = database
        self.Opened = False
        self.layout = QHBoxLayout()
        self.layout2 = QVBoxLayout()
        self.widget = QtWidgets.QWidget(self)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 400, 350))
        self.textEdit.setObjectName("textEdit")
        self.font = QFont("Times", 12)
        self.textEdit.setFont(self.font)
        self.textEdit.setText(text)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.tool_btn_size = QtCore.QSize(35, 35)
        self.pushButtonCreate = QtWidgets.QToolButton(self.widget)
        self.pushButtonCreate.setIcon(QtGui.QIcon("images/add.png"))
        self.pushButtonCreate.setToolTip("Create")
        self.pushButtonCreate.setIconSize(self.tool_btn_size)
        self.pushButtonCreate.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.pushButtonCreate.clicked.connect(self.createNote)
        self.pushButtonOpen = QtWidgets.QToolButton(self.widget)
        self.pushButtonOpen.setIcon(QtGui.QIcon("images/open.png"))
        self.pushButtonOpen.setToolTip("Open")
        self.pushButtonOpen.setIconSize(self.tool_btn_size)
        self.pushButtonOpen.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.pushButtonOpen.clicked.connect(self.openNote)


        self.pushButton = QtWidgets.QToolButton(self.widget)
        self.pushButton.setIcon(QtGui.QIcon("images/save.png"))
        self.pushButton.setToolTip("Save")
        self.pushButton.setIconSize(self.tool_btn_size)
        self.pushButton.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.pushButton.clicked.connect(self.save)

        self.pushButton2 = QtWidgets.QToolButton(self.widget)
        self.pushButton2.setIcon(QtGui.QIcon("images/color.png"))
        self.pushButton2.setToolTip("Color")
        self.pushButton2.setIconSize(self.tool_btn_size)
        self.pushButton2.setGeometry(QtCore.QRect(250, 360, 110, 30))
        self.pushButton2.clicked.connect(self.color_change)

        self.pushButton3 = QtWidgets.QCheckBox("Bold", self.widget)
        self.pushButton3.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
        self.pushButton3.clicked.connect(lambda x: self.bold(True if x else False, self.pushButton3))


        self.pushButton4 = QtWidgets.QCheckBox("Italic", self.widget)
        self.pushButton4.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
        self.pushButton4.clicked.connect(lambda x: self.italic(True if x else False, self.pushButton4))

        self.pushButton5 = QtWidgets.QCheckBox("Underline", self.widget)
        self.pushButton5.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
        self.pushButton5.clicked.connect(lambda x: self.underline(True if x else False, self.pushButton5))

        self.pushButton6 = QtWidgets.QToolButton(self.widget)
        self.pushButton6.setIcon(QtGui.QIcon("images/font.png"))
        self.pushButton6.setToolTip("Font")
        self.pushButton6.setIconSize(self.tool_btn_size)
        self.pushButton6.clicked.connect(self.FontChange)

        self.pushButton7 = QtWidgets.QToolButton(self.widget)
        self.pushButton7.setIcon(QtGui.QIcon("images/left.png"))
        self.pushButton7.setToolTip("Align Left")
        self.pushButton7.setIconSize(self.tool_btn_size)
        self.pushButton7.clicked.connect(self.align_left)

        self.pushButton8 = QtWidgets.QToolButton(self.widget)
        self.pushButton8.setIcon(QtGui.QIcon("images/center.png"))
        self.pushButton8.setToolTip("Align Center")
        self.pushButton8.setIconSize(self.tool_btn_size)
        self.pushButton8.clicked.connect(self.align_center)

        self.pushButton9 = QtWidgets.QToolButton(self.widget)
        self.pushButton9.setIcon(QtGui.QIcon("images/right.png"))
        self.pushButton9.setToolTip("Align Right")
        self.pushButton9.setIconSize(self.tool_btn_size)
        self.pushButton9.clicked.connect(self.align_right)

        self.pushButton10 = QtWidgets.QToolButton(self.widget)
        self.pushButton10.setIcon(QtGui.QIcon("images/justify.png"))
        self.pushButton10.setToolTip("Align Justify")
        self.pushButton10.setIconSize(self.tool_btn_size)
        self.pushButton10.clicked.connect(self.align_justify)

        self.pushButton11 = QtWidgets.QToolButton(self.widget)
        self.pushButton11.setIcon(QtGui.QIcon("images/highlight.png"))
        self.pushButton11.setToolTip("Highlight")
        self.pushButton11.setIconSize(self.tool_btn_size)
        self.pushButton11.clicked.connect(self.highlight)

        self.pushButton12 = QtWidgets.QComboBox(self.widget)
        self.pushButton12.setToolTip('Font Size')
        self.pushButton12.setGeometry(QtCore.QRect(1245, 560, 51, 30))
        FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
        self.pushButton12.addItems([str(s) for s in FONT_SIZES])
        self.pushButton12.currentIndexChanged[str].connect(lambda s: self.textEdit.setFontPointSize(float(s)))

        
        self.pushButton13 = QtWidgets.QToolButton(self.widget)
        self.pushButton13.setIcon(QtGui.QIcon("images/number_list.png"))
        self.pushButton13.setToolTip("Numbered List")
        self.pushButton13.setIconSize(self.tool_btn_size)
        self.pushButton13.clicked.connect(self.numbered_list)

        self.pushButton14 = QtWidgets.QToolButton(self.widget)
        self.pushButton14.setIcon(QtGui.QIcon("images/list.png"))
        self.pushButton14.setToolTip("Unordered List")
        self.pushButton14.setIconSize(self.tool_btn_size)
        self.pushButton14.clicked.connect(self.unordered_list)

        self.pushButton15 = QtWidgets.QToolButton(self.widget)
        self.pushButton15.setIcon(QtGui.QIcon("images/table.png"))
        self.pushButton15.setToolTip("Insert Table")
        self.pushButton15.setIconSize(self.tool_btn_size)
        self.pushButton15.clicked.connect(self.table)

        self.pushButton16 = QtWidgets.QToolButton(self.widget)
        self.pushButton16.setIcon(QtGui.QIcon("images/photo-icon.png"))
        self.pushButton16.setToolTip("Insert Image")
        self.pushButton16.setIconSize(self.tool_btn_size)
        self.pushButton16.clicked.connect(self.image)

        self.standard_font = QtGui.QFont()
        self.standard_font.setPointSize(15)

        self.pushButton18Label = QtWidgets.QLabel("Line Wrap")
        self.pushButton18Label.setFont(self.standard_font)


        self.pushButton18 = AnimatedToggle(checked_color="#FFB000", pulse_checked_color="#44FFB000")
        self.pushButton18.setMinimumSize(80, 10)
        self.pushButton18.stateChanged.connect(self.change_line_wrap)

        self.pushButton20 = QtWidgets.QToolButton(self.widget)
        self.pushButton20.setIcon(QtGui.QIcon("images/settings.png"))
        self.pushButton20.setToolTip("Settings")
        self.pushButton20.setIconSize(self.tool_btn_size)
        self.pushButton20.clicked.connect(self.settings)
        
        self.setCentralWidget(self.widget)
        self.layout.addWidget(self.pushButtonCreate, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButtonOpen, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton3, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton4, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton5, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton6, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton12, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton2, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton11, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton7, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton8, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton9, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton10, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton13, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton14, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton15, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton16, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton18Label, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton18, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.pushButton20, alignment=Qt.AlignHCenter)
        self.layout2.addLayout(self.layout)
        self.layout2.addWidget(self.textEdit)
        self.widget.setLayout(self.layout2)
        scrollWidget = QtWidgets.QScrollArea()
        scrollWidget.setWidget(self.widget)
        scrollWidget.setWidgetResizable(True)
        self.setCentralWidget(scrollWidget)
        self.destroyed.connect(self.closeEvent)

    def save(self):
        try:
            file = open(f"../users/{USER}/database/{self.title}", 'w', encoding='utf-8').close()
            with open(f"../users/{USER}/database/{self.title}", "w", encoding='utf-8') as f:
                f.write(self.textEdit.toHtml())
                f.close()
            QtWidgets.QMessageBox.information(Timerist, "Saved!", f"Your changes were saved successfully.")
        except:
            QtWidgets.QMessageBox.warning(Timerist, "Saving Error", "Please open an existing note to save your changes.")


    def color_change(self):
        dialog = QColorDialog().getColor()
        if dialog.isValid():
            cursor = self.textEdit.textCursor()
            if cursor.hasSelection():
                fmt = QtGui.QTextCharFormat()
                m = []
                for e in dialog.getRgb():
                    m.append(e)
                color = QtGui.QColor(m[0], m[1], m[2], m[3])
                fmt.setForeground(color)
                cursor.mergeCharFormat(fmt)
            else:
                fmt = QtGui.QTextCharFormat()
                m = []
                for e in dialog.getRgb():
                    m.append(e)
                color = QtGui.QColor(m[0], m[1], m[2], m[3])
                fmt.setForeground(color)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)


    

    def bold(self, should, widget):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            fmt = QtGui.QTextCharFormat()
            if should == True:
                fmt.setFontWeight(self.font.Bold)
                cursor.mergeCharFormat(fmt)
            else:
                fmt.setFontWeight(self.font.Normal)
                cursor.mergeCharFormat(fmt)
                widget.setChecked(False)
        else:
            fmt = QtGui.QTextCharFormat()
            if should == True:
                fmt.setFontWeight(self.font.Bold)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)
            else:
                fmt.setFontWeight(self.font.Normal)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)
                widget.setChecked(False)

    def italic(self, should, widget):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            fmt = QtGui.QTextCharFormat()
            if should == True:
                fmt.setFontItalic(True)
                cursor.mergeCharFormat(fmt)
            else:
                fmt.setFontItalic(False)
                cursor.mergeCharFormat(fmt)
                widget.setChecked(False)
        else:
            fmt = QtGui.QTextCharFormat()
            if should == True:
                fmt.setFontItalic(True)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)
            else:
                fmt.setFontItalic(False)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)
                widget.setChecked(False)

    
    def underline(self, should, widget):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            fmt = QtGui.QTextCharFormat()
            if should == True:
                fmt.setFontUnderline(True)
                cursor.mergeCharFormat(fmt)
            else:
                fmt.setFontUnderline(False)
                cursor.mergeCharFormat(fmt)
                widget.setChecked(False)
        else:
            fmt = QtGui.QTextCharFormat()
            if should == True:
                fmt.setFontUnderline(True)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)
            else:
                fmt.setFontUnderline(False)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)
                widget.setChecked(False)

    def align_left(self):
        try:
            cursor = self.textEdit.textCursor()
            if cursor.hasSelection():
                fmt = cursor.blockFormat()
                fmt.setAlignment(Qt.AlignLeft)
                cursor.mergeBlockFormat(fmt)
            else:
                fmt = cursor.blockFormat()
                fmt.setAlignment(Qt.AlignLeft)
                cursor.mergeBlockFormat(fmt)
                self.textEdit.setTextCursor(cursor)
        except Exception as E:
            print(E)

    def align_center(self):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            fmt = cursor.blockFormat()
            fmt.setAlignment(Qt.AlignCenter)
            cursor.mergeBlockFormat(fmt)
        else:
            fmt = cursor.blockFormat()
            fmt.setAlignment(Qt.AlignCenter)
            cursor.mergeBlockFormat(fmt)
            self.textEdit.setTextCursor(cursor)

    def align_right(self):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            fmt = cursor.blockFormat()
            fmt.setAlignment(Qt.AlignRight)
            cursor.mergeBlockFormat(fmt)
        else:
            fmt = cursor.blockFormat()
            fmt.setAlignment(Qt.AlignRight)
            cursor.mergeBlockFormat(fmt)
            self.textEdit.setTextCursor(cursor)

    def align_justify(self):
        cursor = self.textEdit.textCursor()
        if cursor.hasSelection():
            fmt = cursor.blockFormat()
            fmt.setAlignment(Qt.AlignJustify)
            cursor.mergeBlockFormat(fmt)
        else:
            fmt = cursor.blockFormat()
            fmt.setAlignment(Qt.AlignJustify)
            cursor.mergeBlockFormat(fmt)
            self.textEdit.setTextCursor(cursor)

    def highlight(self):
        dialog = QColorDialog().getColor()
        if dialog.isValid():
            cursor = self.textEdit.textCursor()
            if cursor.hasSelection():
                fmt = QtGui.QTextCharFormat()
                m = []
                for e in dialog.getRgb():
                    m.append(e)
                color = QtGui.QColor(m[0], m[1], m[2], m[3])
                fmt.setBackground(color)
                cursor.mergeCharFormat(fmt)
            else:
                fmt = QtGui.QTextCharFormat()
                m = []
                for e in dialog.getRgb():
                    m.append(e)
                color = QtGui.QColor(m[0], m[1], m[2], m[3])
                fmt.setBackground(color)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)

    def numbered_list(self):
        document = self.textEdit.document()
        cursor = self.textEdit.textCursor()
        listFormat = QTextListFormat()
        listFormat.setStyle(QTextListFormat.ListDecimal)
        listFormat.setNumberPrefix("(")
        listFormat.setNumberSuffix(")")
        listFormat.setIndent(2)
        listFormat.setForeground(QtGui.QColor(0, 0, 0))
        cursor.insertList(listFormat)

    def unordered_list(self):
        self.unordered_list_win_config = QtWidgets.QDialog(self)
        self.unordered_list_win_config.resize(200, 200)
        self.unordered_list_win_config.setWindowIcon(QtGui.QIcon("images/list.png"))
        self.unordered_list_win_config.setWindowTitle("Insert Unordered List")
        formGroupBox = QtWidgets.QGroupBox("Bullet Type")

        layout = QtWidgets.QFormLayout()

        self.filled_circle_btn = QtWidgets.QRadioButton()

        self.empty_circle_btn = QtWidgets.QRadioButton()

        self.filled_square_btn = QtWidgets.QRadioButton()

        label_font = QtGui.QFont()
        label_font.setPointSize(20)
        
        filled_circle_label = QtWidgets.QLabel("Filled Circle: ")
        filled_circle_label.setFont(label_font)
        empty_circle_label = QtWidgets.QLabel("Empty Circle: ")
        empty_circle_label.setFont(label_font)
        filled_square_label = QtWidgets.QLabel("Filled Square: ")
        filled_square_label.setFont(label_font)

        layout.addRow(filled_circle_label, self.filled_circle_btn)
        layout.addRow(empty_circle_label, self.empty_circle_btn)
        layout.addRow(filled_square_label, self.filled_square_btn)

        formGroupBox.setLayout(layout)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.getInfo_unordered_config)
        buttonBox.rejected.connect(self.reject_unordered_config)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(formGroupBox)
        mainLayout.addWidget(buttonBox)

        self.unordered_list_win_config.setLayout(mainLayout)
        self.unordered_list_win_config.show()

    def getInfo_unordered_config(self):
        if self.filled_circle_btn.isChecked() == True:
            document = self.textEdit.document()
            cursor = self.textEdit.textCursor()
            listFormat = QTextListFormat()
            listFormat.setStyle(QTextListFormat.ListDisc)
            listFormat.setIndent(2)
            listFormat.setForeground(QtGui.QColor(0, 0, 0))
            cursor.insertList(listFormat)
        elif self.filled_square_btn.isChecked() == True:
            document = self.textEdit.document()
            cursor = self.textEdit.textCursor()
            listFormat = QTextListFormat()
            listFormat.setStyle(QTextListFormat.ListSquare)
            listFormat.setIndent(2)
            listFormat.setForeground(QtGui.QColor(0, 0, 0))
            cursor.insertList(listFormat)
        elif self.empty_circle_btn.isChecked() == True:
            document = self.textEdit.document()
            cursor = self.textEdit.textCursor()
            listFormat = QTextListFormat()
            listFormat.setStyle(QTextListFormat.ListCircle)
            listFormat.setIndent(2)
            listFormat.setForeground(QtGui.QColor(0, 0, 0))
            cursor.insertList(listFormat)

    def reject_unordered_config(self):
        self.unordered_list_win_config.destroy()

    
    def table(self):
        self.table_config_win = QtWidgets.QDialog(self)
        self.table_config_win.resize(200, 200)
        self.table_config_win.setWindowIcon(QtGui.QIcon("images/table.png"))
        self.table_config_win.setWindowTitle("Insert Table")
        formGroupBox = QtWidgets.QGroupBox("Configuration")

        layout = QtWidgets.QFormLayout()

        self.table_rows = QtWidgets.QSpinBox()

        self.table_cols = QtWidgets.QSpinBox()
      

        label_font = QtGui.QFont()
        label_font.setPointSize(20)
        
        rows_label = QtWidgets.QLabel("Rows: ")
        rows_label.setFont(label_font)

        cols_label = QtWidgets.QLabel("Columns: ")
        cols_label.setFont(label_font)

        layout.addRow(rows_label, self.table_rows)
        layout.addRow(cols_label, self.table_cols)

        formGroupBox.setLayout(layout)

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.getInfo_table_config)
        buttonBox.rejected.connect(self.reject_table_config)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(formGroupBox)
        mainLayout.addWidget(buttonBox)

        self.table_config_win.setLayout(mainLayout)
        self.table_config_win.show()


    def getInfo_table_config(self):
        document = self.textEdit.document()
        cursor = self.textEdit.textCursor()
        tableFormat = QTextTableFormat()
        tableFormat.setBorderCollapse(True)
        tableFormat.setCellSpacing(20)
        tableFormat.setCellPadding(40)
        tableFormat.setBorderBrush(QtGui.QColor(0, 0, 0))
        cursor.insertTable(self.table_rows.value(), self.table_cols.value(), tableFormat)

    def reject_table_config(self):
        self.table_config_win.destroy()

    def image(self):
        try:
            file = QtWidgets.QFileDialog.getOpenFileName(self, "Insert Image", ".", "PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)")
            document = self.textEdit.document()
            cursor = QTextCursor(document)
            cursor.insertImage(file[0])
        except:
            pass


    def change_line_wrap(self):
        if self.pushButton18.isChecked():
            self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        else:
            self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

    def settings(self):
        self.settings_win = QtWidgets.QDialog(self)
        self.settings_win.resize(500, 400)
        self.settings_win.setWindowIcon(QtGui.QIcon("images/settings.png"))
        self.settings_win.setWindowTitle("Editor Settings")

        label_font = QtGui.QFont()
        label_font.setPointSize(20)

        tab_layout = QtWidgets.QVBoxLayout()

        tabs = TabWidget()

        # tabs -> apperance, preferances 

        apperance_tab = QtWidgets.QWidget()
        preferances_tab = QtWidgets.QWidget()

        tabs.addTab(apperance_tab, "Apperance")
        tabs.addTab(preferances_tab, "Preferances")

        tab_layout.addWidget(tabs)

        apperance_tab_layout = QVBoxLayout()

        apperance_form_layout = QFormLayout()
        apperance_form_widget = QtWidgets.QWidget()

        background_field_label = QtWidgets.QLabel("Background")
        background_field_label.setFont(label_font)

        theme_field_label = QtWidgets.QLabel("Color Theme")
        theme_field_label.setFont(label_font)

        background_field_options_widget = QtWidgets.QWidget()
        background_field_options_layout = QHBoxLayout()

        theme_field_options_widget = AnimatedToggle(checked_color="#3498DB", pulse_checked_color="#44FFB000")
        #theme_field_options_widget.stateChanged.connect(self.settings_change_theme)

        background_field_option1 = QtWidgets.QPushButton("Color")
        background_field_option2 = QtWidgets.QPushButton("Image")


        background_field_options_layout.addWidget(background_field_option1)
        background_field_options_layout.addWidget(background_field_option2)
        
        background_field_options_widget.setLayout(background_field_options_layout)

        apperance_form_layout.addRow(background_field_label, background_field_options_widget)
        apperance_form_layout.addRow(theme_field_label, theme_field_options_widget)

        apperance_buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        apperance_buttonBox.accepted.connect(self.apperanceOk)
        apperance_buttonBox.rejected.connect(self.apperanceNo)

        apperance_form_widget.setLayout(apperance_form_layout)

        apperance_tab_layout.addWidget(apperance_form_widget)
        apperance_tab_layout.addWidget(apperance_buttonBox)

        apperance_tab.setLayout(apperance_tab_layout)

        self.settings_win.setLayout(tab_layout)
        self.settings_win.show()

    def apperanceOk(self):
        pass

    def apperanceNo(self):
        pass

    def closeEvent(self, e):
        msg_save = QtWidgets.QMessageBox.question(self, "Save Changes", "Would you like to save your changes?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if msg_save == QtWidgets.QMessageBox.Yes:
            try:
                file = open(f"../users/{USER}/database/{self.title}", 'w', encoding='utf-8').close()
                with open(f"../users/{USER}/database/{self.title}", "w", encoding='utf-8') as f:
                    f.write(self.textEdit.toHtml())
                    f.close()
                QtWidgets.QMessageBox.information(self, "Saved!", f"Your changes were saved successfully.")
            except:
                QtWidgets.QMessageBox.warning(self, "Saving Error", "Please open an existing note to save your changes.")
        else:
            pass

    def createNote(self):
        if self.database != None:
            create = CreateWindow(self, self.textEdit.toHtml(), database=self.database)
            create.show()
        else:
            create = CreateWindow(self, self.textEdit.toHtml())
            create.show()
        

    def openNote(self):
        self.openWin = OpenWindow(self, self.textEdit, winTitle=self)
        self.openWin.show()

    def isOpened(self):
        return self.Opened


    def FontChange(self):
        self.Fontdlg = QFontDialog()
        font, ok = self.Fontdlg.getFont()
        if ok:
            cursor = self.textEdit.textCursor()
            if cursor.hasSelection():
                fmt = QtGui.QTextCharFormat()
                fmt.setFont(font)
                cursor.mergeCharFormat(fmt)
            else:
                fmt = QtGui.QTextCharFormat()
                fmt.setFont(font)
                cursor.mergeCharFormat(fmt)
                self.textEdit.setTextCursor(cursor)



        




class CreateWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, text=None, database=None):
        super().__init__(parent=Parent)
        self.setFixedSize(320, 150)
        self.setWindowTitle("New Note")
        self.text = text
        self.database = database
        self.centralwidget = QtWidgets.QWidget(self)
        self.lineEdit = QtWidgets.QLineEdit("Note Title", self.centralwidget)
        self.lineEdit.setGeometry(20, 20, 280, 60)
        self.lineEdit.setObjectName("saveNoteTitle")
        self.font = QFont("Times", 12)
        self.lineEdit.setFont(self.font)
        self.pushButton = QtWidgets.QPushButton("Create", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 90, 110, 30))
        self.pushButton.clicked.connect(self.save)
        self.setCentralWidget(self.centralwidget)

    def save(self):
        selected = f"../database/{self.lineEdit.text()}.html"
        if os.path.isfile(selected):
            QtWidgets.QMessageBox.critical(self, "Error!", "A note already exists with this title.")
        else:
            with open(selected, "a", encoding='utf-8') as f:
                f.write(" ")
                f.close()
            if self.database != None:
                self.database.addItem(QListWidgetItem(f'{self.lineEdit.text()}.html'))

class HTMLEditor(Qsci.QsciScintilla):
    def __init__(self, parent=None, text=''):
        super().__init__(parent)
        self.lexer = Qsci.QsciLexerHTML(self)
        self.setLexer(self.lexer)
        self.lexer.setFont(QFont("Consolas", 15))
        self.setText(text)


class EmbedHtmlWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, html, filename):
        super().__init__(parent=Parent)
        self.setWindowTitle(title)
        self.widget = QtWidgets.QWidget()
        self.layout = QHBoxLayout()
        self.tool_btn_size = QtCore.QSize(35, 35)


        ## reading the html data
        with open(filename, 'r', encoding='utf-8') as f:
            textdata = f.read()
            f.close()


        self.htmlPreview = HTMLEditor(self.widget, text=textdata)
        self.htmlPreview.setReadOnly(True)

        self.webbrowser = QtWebEngineWidgets.QWebEngineView(self.widget)
        self.webbrowser.setUrl(QtCore.QUrl.fromLocalFile(os.path.abspath(filename)))

        self.setCentralWidget(self.widget)
        self.layout.addWidget(self.htmlPreview, 50)
        self.layout.addWidget(self.webbrowser, 50)

        self.widget.setLayout(self.layout)
        scrollWidget = QtWidgets.QScrollArea()
        scrollWidget.setWidget(self.widget)
        scrollWidget.setWidgetResizable(True)
        self.setCentralWidget(scrollWidget)


class ReadWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, text):
        super().__init__(parent=Parent)
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
        QtWidgets.QMessageBox.information(self, "Coming Soon...", "The functionality of printing out your notes is coming out in the future!")

    def HtmlDialog(self):
        dialog = EmbedHtmlWindow(self, "Embed Html", self.textEdit, filename=f"../users/{USER}/database/{self.title}")
        dialog.show()

class OpenWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, textTo, winTitle=None):
        super().__init__(parent=Parent)
        self.setFixedSize(500, 500)
        self.setWindowTitle("Open A Note")
        self.to = textTo
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 20, 211, 51))
        self.winTitle = winTitle
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setText("Notes")
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setGeometry(QtCore.QRect(100, 100, 320, 200))
        for root, dirs, files in os.walk(f"../users/{self.user.email}/database"):
            for filename in files:
                QtWidgets.QListWidgetItem(filename, self.listWidget)
        self.pushButton = QtWidgets.QPushButton("Open", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 320, 100, 30))
        self.pushButton.clicked.connect(self.get)
        self.setCentralWidget(self.centralwidget)
        self.opened = False

    def get(self):
        try:
            selected = [item.text() for item in self.listWidget.selectedItems()]
            selected_str = ", ".join(selected)
            file = open(f"../users/{USER}/database/{selected_str}", "r", encoding="utf-8")
            self.filename = f"../users/{USER}/database/{selected_str}"
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
            QtWidgets.QMessageBox.warning(self, "Select a Note", "Please select a note to open.")

    def isOpened(self):
        return self.opened


class Ui_Timerist(object):
    def setupUi(self, Timerist, sound, user):
        Timerist.setObjectName("Timerist")
        Timerist.resize(650, 550)
        Timerist.setWindowIcon(QtGui.QIcon('images/icon.png'))

        self.TodoOptionsLayout = QHBoxLayout()
        self.TodoLayout = QVBoxLayout()

        self.NotesOptionsLayout = QHBoxLayout()
        self.NotesLayout = QVBoxLayout()

        self.MainWidget = QtWidgets.QWidget()

        self.opened = False
        self.tool_btn_size = QtCore.QSize(400, 400)
        self.sound = sound

        self.user = user
        User = self.user

        font = QtGui.QFont()
        font.setPointSize(20)
        self.todo_label = QtWidgets.QLabel(self.MainWidget)
        self.todo_label.setGeometry(QtCore.QRect(100, 2, 241, 51))
        self.todo_label.setFont(font)
        self.todo_label.setText("To Do List: ")

        self.notes_label = QtWidgets.QLabel(self.MainWidget)
        self.notes_label.setGeometry(QtCore.QRect(100, 2, 241, 51))
        self.notes_label.setFont(font)
        self.notes_label.setText("Notes: ")

        self.treeWidget = QtWidgets.QTreeWidget(self.MainWidget)
        self.treeWidget.setGeometry(QtCore.QRect(20, 60, 360, 300))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setHeaderLabels(["Date", "Task", "Status"])

        self.NotesDatabase = QtWidgets.QListWidget(self.MainWidget)
        self.NotesDatabase.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.NotesDatabase.setGeometry(QtCore.QRect(100, 100, 320, 200))
        for root, dirs, files in os.walk(f"../users/{self.user.email}/database"):
            for filename in files:
                QtWidgets.QListWidgetItem(filename, self.NotesDatabase)

        self.create_note = QtWidgets.QPushButton("Create", self.MainWidget)
        self.create_note.setGeometry(QtCore.QRect(320, 320, 100, 30))
        self.create_note.clicked.connect(self.CreateNote)
        self.remove_note = QtWidgets.QPushButton("Remove", self.MainWidget)
        self.remove_note.setGeometry(QtCore.QRect(100, 320, 100, 30))
        self.remove_note.clicked.connect(self.remove)
        self.edit_note = QtWidgets.QPushButton("Edit", self.MainWidget)
        self.edit_note.setGeometry(QtCore.QRect(210, 320, 100, 30))
        self.edit_note.clicked.connect(self.edit)
        self.open_note = QtWidgets.QPushButton("Open", self.MainWidget)
        self.open_note.setGeometry(QtCore.QRect(320, 320, 100, 30))
        self.open_note.clicked.connect(self.OpenNote)
        

        file = open(f"../users/{self.user.email}/data.txt", "r", encoding='utf-8')
        data = file.readlines()
        file.close()
        data = [line.replace('\n', '') for line in data]
        desired_lines = data[0::1]
        fov = slice_per(desired_lines, 3)
        for e in fov:
            self.treeWidget.addTopLevelItem(QTreeWidgetItem(e))

        self.pushButton = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 260, 83, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(115, 260, 83, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(205, 260, 83, 28))
        self.pushButton_3.setText("Update")
        self.pushButton_4 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(295, 260, 83, 28))
        self.pushButton_4.setText("View")
        self.pushButton_3.clicked.connect(self.update_todo)
        self.pushButton_4.clicked.connect(self.view_todo)
        self.color_theme_btn = AnimatedToggle(checked_color="#4c5375")
        self.color_theme_btn.setMinimumSize(80, 10)
        self.color_theme_btn.setToolTip("Dark Mode: Off")
        self.color_theme_btn.stateChanged.connect(
            lambda x: self.dark_theme() if x else self.light_theme()
        )

        self.TodoOptionsLayout.addWidget(self.todo_label, alignment=Qt.AlignTop)
        self.TodoOptionsLayout.addWidget(self.pushButton, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_2, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_3, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_4, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addStretch(5)
        self.TodoOptionsLayout.addWidget(self.color_theme_btn, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addStretch()
        self.TodoLayout.addLayout(self.TodoOptionsLayout)
        self.TodoLayout.addWidget(self.treeWidget)
        self.TodoLayout.addStretch()
        # Newest Layout for MainWidget
        self.NotesLayout.addLayout(self.TodoLayout)
        self.NotesOptionsLayout.addWidget(self.notes_label, alignment=Qt.AlignTop)
        self.NotesOptionsLayout.addWidget(self.create_note, alignment=Qt.AlignLeft)
        self.NotesOptionsLayout.addWidget(self.remove_note, alignment=Qt.AlignLeft)
        self.NotesOptionsLayout.addWidget(self.edit_note, alignment=Qt.AlignLeft)
        self.NotesOptionsLayout.addWidget(self.open_note, alignment=Qt.AlignLeft)
        self.NotesOptionsLayout.addStretch()
        self.NotesLayout.addLayout(self.NotesOptionsLayout)
        self.NotesLayout.addWidget(self.NotesDatabase)
        self.MainWidget.setLayout(self.NotesLayout)
        self.scrollWidget = QtWidgets.QScrollArea()
        self.scrollWidget.setWidget(self.MainWidget)
        self.scrollWidget.setWidgetResizable(True)
        Timerist.setCentralWidget(self.scrollWidget)


        self.menubar = QtWidgets.QMenuBar(Timerist)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.Copyright_menu = QtWidgets.QMenu("Copyright", self.menubar)
        self.view_Copyright = QtWidgets.QAction(text="View", parent=self.Copyright_menu)
        self.view_Copyright.triggered.connect(self.CopyrightShow)
        self.Copyright_menu.addAction(self.view_Copyright)
        self.menubar.addMenu(self.Copyright_menu)
        Timerist.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Timerist)
        self.statusbar.setObjectName("statusbar")
        Timerist.setStatusBar(self.statusbar)
        return User
        self.retranslateUi(Timerist)
        QtCore.QMetaObject.connectSlotsByName(Timerist)
    

    def retranslateUi(self, Timerist):
        _translate = QtCore.QCoreApplication.translate
        Timerist.setWindowTitle(_translate("Timerist", "Timerist"))
        self.pushButton.setText(_translate("Timerist", "Add"))
        self.pushButton.clicked.connect(self.add_todo)
        self.pushButton_2.setText(_translate("Timerist", "Remove"))
        self.pushButton_2.clicked.connect(self.remove_todo)

    def add_todo(self):
        add = AddTodoForm(Timerist, "Add Todo", self.treeWidget)
        add.show()

    def remove_todo(self):
        items = self.treeWidget.selectedItems()
        for item in items:
            item_text = [item.text(0), item.text(1), item.text(2)]
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
            delete_item_from_query(item_text, path='../data.txt')

    def update_todo(self):
        items = self.treeWidget.selectedItems()
        for item in items:
            item_text_prev = [item.text(0), item.text(1), item.text(2)]
            item.setText(2, "Completed ✅")
            item_text_new = [item.text(0), item.text(1), item.text(2)]
            change_item_from_query(item_text_prev, item_text_new, '../data.txt')

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
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_closed_id, taskToComplete=item_text[1], tree=self.treeWidget)
                    edit_todo_win.show()
                elif is_task_completed == False:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_time_is_up_id, self.sound, is_task_completed, taskToComplete=item_text[1], soundAlarm=True, tree=self.treeWidget)
                    edit_todo_win.show()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            else:
                if is_task_completed == True:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", task_closed_id, taskToComplete=item_text[1], tree=self.treeWidget)
                    edit_todo_win.show()
                elif is_task_completed == False:
                    edit_todo_win = EditTodoWindow(Timerist, f"Viewing Task - {task_name}", text_data, taskToComplete=item_text[1], soundAlarm=True, newText=item_text[0], sound=self.sound, isTimeShowing=True, prev_date=item_text[0], prev_status=item_text[2], tree=self.treeWidget)
                    edit_todo_win.show()

    def open(self):
        self.openWin = OpenWindow(Timerist, self.textEdit)
        self.openWin.show()

    def Save(self):
        save = CreateWindow(Timerist, self.textEdit.toHtml())
        save.show()

    def save_changes(self):
        try:
            file = open(self.openWin.filename, 'w', encoding='utf-8').close()
            with open(self.openWin.filename, "w", encoding='utf-8') as f:
                f.write(self.textEdit.toHtml())
                f.close()
            QtWidgets.QMessageBox.information(Timerist, "Saved!", f"Your changes were saved successfully.")
        except:
            QtWidgets.QMessageBox.warning(Timerist, "Saving Error", "Please open an existing note to save your changes.")

    def remove(self):
        for item in self.NotesDatabase.selectedItems():
            self.NotesDatabase.takeItem(self.NotesDatabase.row(item))
            os.remove(f"../database/{item.text()}")

    def edit(self):
        try:
            selected = [item.text() for item in self.NotesDatabase.selectedItems()]
            selected_str = ", ".join(selected)
            file = open(f"../users/{USER}/database/{selected_str}", "r", encoding='utf-8')
            data = file.read()
            file.close()
            edit_window = EditWindow(Timerist, f"{selected_str}", f"{data}", database=self.NotesDatabase)
            edit_window.show()
        except Exception as E:
            QtWidgets.QMessageBox.warning(Timerist, "Select a Note", "Please select a note so that an action can be completed.")

    def OpenNote(self):
        try:
            selected = [item.text() for item in self.NotesDatabase.selectedItems()]
            selected_str = ", ".join(selected)
            file = open(f"../users/{USER}/database/{selected_str}", "r", encoding='utf-8')
            data = file.read()
            file.close()
            read_window = ReadWindow(Timerist, f"{selected_str}", text=data)
            read_window.show()
        except Exception as E:
            QtWidgets.QMessageBox.warning(Timerist, "Select a Note", f"{E}")
        #except:
            #QtWidgets.QMessageBox.warning(Timerist, "Select a Note", "Please select a note so that an action can be completed.")

    def dark_theme(self):
        app.setStyleSheet(load_from_stylesheet("../dark-theme.qss"))
        self.color_theme_btn.setToolTip("Dark Mode: On")

    def light_theme(self):
        app.setStyleSheet("")
        self.color_theme_btn.setToolTip("Dark Mode: Off")


    def CreateNote(self):
        create = CreateWindow(Timerist, database=self.NotesDatabase)
        create.show()

    def CopyrightShow(self):
        CopyrightWin = QtWidgets.QMainWindow(Timerist)
        CopyrightWin.resize(500, 350)
        CopyrightWin.setWindowTitle("Copyright")
        CopyrightWin.setWindowIcon(QIcon("images/keys.png"))
        layout = QVBoxLayout()
        widget = QtWidgets.QWidget()
        copyright_text = QTextEdit(widget)
        copyright_text.setReadOnly(True)
        copyright_text.setCursor(Qt.PointingHandCursor)
        copyright_text.setText(open("LICENSE", "r").read())
        copyright_font_id = QFontDatabase.addApplicationFont("backend/Segoe UI.ttf")
        copyright_text_font_family = QFontDatabase.applicationFontFamilies(copyright_font_id)[0]
        copyright_text_font = QFont(copyright_text_font_family, 13)
        copyright_text.setFont(copyright_text_font)
        layout.addWidget(copyright_text)
        widget.setLayout(layout)
        CopyrightWin.setCentralWidget(widget)
        CopyrightWin.show()

app = QtWidgets.QApplication(sys.argv)
Timerist = QtWidgets.QMainWindow()
Timerist.setObjectName("Timerist")
ui = Ui_Timerist()
#USER = ui.setupUi()
