from imports import *
from utils import *


def start_timer(end_date):
    current_date_time = QtCore.QDateTime.currentDateTime()
    fmt = current_date_time.toString("yyyy-MM-dd hh:mm:ss a")

    if datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]), int(end_date[9:11]),
                int(end_date[14:16]), int(end_date[17:19])) <= datetime(int(fmt[0:4]), int(fmt[5:7]),
                                                                        int(fmt[8:10]), int(fmt[9:11]),
                                                                        int(fmt[14:16]), int(fmt[17:19])):
        return "yes"
    else:
        return f"{days_in_between(fmt, end_date)} time left."


class EditTodoTabs(QtWidgets.QWidget):
    def __init__(self, parent, timeText, taskToComplete, soundAlarm, music, newText, prev_date, prev_status, tree,
                 Sound=None):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QVBoxLayout()
        self.timeText = timeText
        self.task = taskToComplete
        self.soundAlarm = soundAlarm
        self.music = music
        self.newText = newText
        self.prev_date = prev_date

        if 'm' in self.prev_date:
            self.prev_time = self.prev_date[11:-2] + self.prev_date[20] + self.prev_date[21]
        else:
            self.prev_time = self.prev_date[11:-2]

        self.prev_status = prev_status
        self.tree = tree

        self.tab1 = QtWidgets.QWidget()
        self.font = QtGui.QFont()
        self.font.setPointSize(15)
        self.labelTime = QtWidgets.QLabel()
        self.labelTime.setFont(self.font)
        self.labelTime.setText(f"Time Left To Complete: {self.task}")

        self.font2 = QtGui.QFont()
        self.font2.setPointSize(30)

        self.font3 = QtGui.QFont()
        self.font3.setPointSize(10)

        self.labelTime2 = QtWidgets.QLabel()
        self.labelTime2.setFont(self.font2)

        if self.timeText == "Task Closed ✅":
            self.labelTime2.setStyleSheet("color: #60945f;")
        elif self.timeText == "Time is Up!":
            self.labelTime2.setStyleSheet("color: #fc5b5b;")
            self.labelTime3 = QtWidgets.QLabel()
            self.labelTime3.setFont(self.font)
            self.labelTime3.setText('Alarm: on')
            self.checkBox1 = QtWidgets.QCheckBox()
            self.checkBox1.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px;}")
            self.checkBox1.setChecked(True)
            self.checkBox1.stateChanged.connect(self.AlarmNoise)
        else:
            self.labelTime2.setStyleSheet("color: #fc5b5b;")

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        self.showTime()

        if self.soundAlarm:
            self.gif_label = QtWidgets.QLabel()
            self.alarm_gif_size = QtCore.QSize(100, 100)
            self.alarm_gif = QtGui.QMovie("assets/alarm.gif")
            self.alarm_gif.setScaledSize(self.alarm_gif_size)
            self.gif_label.setMovie(self.alarm_gif)
            self.alarm_gif.start()

        self.tell_time_layout = QVBoxLayout()
        self.gh = QHBoxLayout()
        self.gh.addWidget(self.labelTime2)

        if hasattr(self, 'alarm_gif'):
            lbl = QLabel()
            lbl.setMovie(self.alarm_gif)
            self.gh.addWidget(lbl)

        if hasattr(self, 'labelTime3'):
            self.gh.addWidget(self.labelTime3)
            self.gh.addWidget(self.checkBox1)
            self.gh.addStretch()

        self.tell_time_layout.addWidget(self.labelTime)
        self.tell_time_layout.addLayout(self.gh)
        self.tell_time_layout.addStretch()
        self.tab1.setLayout(self.tell_time_layout)
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
