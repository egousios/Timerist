from imports import *
from utils import *

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
            self.alarm_gif = QtGui.QMovie("assets/alarm.gif")
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