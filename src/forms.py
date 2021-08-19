from imports import *

class AddTodoForm(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, widget, user):
        super().__init__(parent=Parent)
        self.user = user
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
        self.lineEdit.setObjectName("line")
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
        data = [f'{date_and_time}', f'{self.lineEdit.text()}', "Incomplete ❌"]
        if len(self.lineEdit.text()) > 1 and is_item(data, f"users/{self.user}/data.txt") == False:
            branch = Tree(branches={
                    "end_time":data[0],
                    "task":data[1],
                    "status":data[2],
                })
            branch.save(branch.branches, id="all", path=f"users/{self.user}/data.txt")
            self.wid.addTopLevelItem(QTreeWidgetItem(data))
        elif len(self.lineEdit.text()) < 1:
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle("Error")
                self.msg.setWindowIcon(QtGui.QIcon('images/icon.png'))
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("Your task must be at least 1 character.")
                self.msg.exec_()
        elif is_item(data, f"users/{self.user}/data.txt") == True:
            QtWidgets.QMessageBox.critical(self, "Error!", "A todo already exists with this title.")