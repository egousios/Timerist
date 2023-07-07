from imports import *


class AddTodoForm(QtWidgets.QDialog):
    def __init__(self, Parent, title, widget, user):
        super().__init__(parent=Parent)
        self.user = user
        self.wid = widget
        self.setFixedSize(485, 550)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("app_icon.ico"))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        font = QtGui.QFont()
        font.setPointSize(15)

        self.label = QtWidgets.QLabel()
        self.label.setFont(font)
        self.label.setText("Date To Complete:")

        self.datetime = QtWidgets.QCalendarWidget(self)
        kl = get_current_time()
        yr = kl[0:4]
        mm = kl[5:7]
        dd = kl[8:10]
        self.datetime.setMinimumDate(QtCore.QDate(int(yr), int(mm), int(dd)))

        self.timeToCompleteLbl = QtWidgets.QLabel()
        self.timeToCompleteLbl.setFont(font)
        self.timeToCompleteLbl.setText("Time To Complete:")

        self.timeEdit = QtWidgets.QTimeEdit(self)

        self.label2 = QtWidgets.QLabel()
        self.label2.setFont(font)
        self.label2.setText("Task:")

        self.lineEdit = QtWidgets.QLineEdit(self)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText("Ok")
        self.pushButton.clicked.connect(self.add)

        self.pushButton2 = QtWidgets.QPushButton(self)
        self.pushButton2.setText("Cancel")
        self.pushButton2.clicked.connect(self.cancel)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.datetime)
        layout.addWidget(self.timeToCompleteLbl)
        layout.addWidget(self.timeEdit)
        layout.addWidget(self.label2)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton)
        layout.addWidget(self.pushButton2)
        layout.addStretch()
        self.setLayout(layout)

    def cancel(self):
        self.destroy()

    def add(self):
        date = self.datetime.selectedDate().toString("yyyy-MM-dd")
        time = self.timeEdit.time().toString("hh:mm:ss a")
        date_and_time = f"{date} {time}"
        data = [f'{date_and_time}', f'{self.lineEdit.text()}', "Incomplete ❌"]

        if len(self.lineEdit.text()) >= 1 and is_item(data, get_route_to_data(self.user, "availible_tasks")) == False:
            branch = Tree(branches={
                "end_time": data[0],
                "task": data[1],
                "status": data[2],
            })
            branch.save(branch.branches, id="all", path=get_route_to_data(self.user, "availible_tasks"))
            self.wid.addTopLevelItem(QTreeWidgetItem(data))
        elif len(self.lineEdit.text()) < 1:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setWindowIcon(QtGui.QIcon('app_icon.ico'))
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("Your task must be at least 1 character.")
            self.msg.exec_()
        elif is_item(data, get_route_to_data(self.user, "availible_tasks")) == True:
            QtWidgets.QMessageBox.critical(self, "Error!", "A todo already exists with this title.")


class EditTodoForm(QtWidgets.QDialog):
    def __init__(self, Parent, title, widget, user, item_to_edit, prev_data):
        super().__init__(parent=Parent)
        self.user = user
        self.wid = widget
        self.item_to_edit = item_to_edit
        self.prev_data = prev_data
        self.setFixedSize(485, 550)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("app_icon.ico"))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        font = QtGui.QFont()
        font.setPointSize(15)

        self.label = QtWidgets.QLabel()
        self.label.setFont(font)
        self.label.setText("Date To Complete:")

        self.datetime = QtWidgets.QCalendarWidget(self)
        y = int(self.item_to_edit.text(0)[0:4])
        m = int(self.item_to_edit.text(0)[5:7])
        d = int(self.item_to_edit.text(0)[8:10])
        self.datetime.setSelectedDate(QDate(y, m, d))

        self.timeToCompleteLbl = QtWidgets.QLabel()
        self.timeToCompleteLbl.setFont(font)
        self.timeToCompleteLbl.setText("Time To Complete:")

        self.timeEdit = QtWidgets.QTimeEdit(self)
        hr = int(self.item_to_edit.text(0)[9:11])
        mm = int(self.item_to_edit.text(0)[14:16])
        sec = int(self.item_to_edit.text(0)[17:19])
        self.timeEdit.setTime(QTime(hr, mm, sec))

        self.label2 = QtWidgets.QLabel()
        self.label2.setFont(font)
        self.label2.setText("Task:")

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setText(self.item_to_edit.text(1))

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setText("Save Changes")
        self.pushButton.clicked.connect(self.edit)

        self.pushButton2 = QtWidgets.QPushButton(self)
        self.pushButton2.setText("Cancel Changes")
        self.pushButton2.clicked.connect(self.cancel)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.datetime)
        layout.addWidget(self.timeToCompleteLbl)
        layout.addWidget(self.timeEdit)
        layout.addWidget(self.label2)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton)
        layout.addWidget(self.pushButton2)
        layout.addStretch()
        self.setLayout(layout)

    def cancel(self):
        self.destroy()

    def edit(self):
        date = self.datetime.selectedDate().toString("yyyy-MM-dd")
        time = self.timeEdit.time().toString("hh:mm:ss a")
        date_and_time = f"{date} {time}"
        data = [f'{date_and_time}', f'{self.lineEdit.text()}', "Incomplete ❌"]

        if len(self.lineEdit.text()) > 1:
            self.item_to_edit.setText(0, data[0])
            self.item_to_edit.setText(1, data[1])
            self.item_to_edit.setText(2, data[2])
            change_item_from_query(self.prev_data, data, get_route_to_data(self.user, "availible_tasks"))
            self.destroy()
        elif len(self.lineEdit.text()) < 1:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Error")
            self.msg.setWindowIcon(QtGui.QIcon('app_icon.ico'))
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("Your new must be at least 1 character.")
            self.msg.exec_()

