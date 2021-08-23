from imports import *
from forms import AddTodoForm

class Ui_Timerist(object):
    def setupUi(self, Timerist, sound, email, password):
        Timerist.setObjectName("Timerist")
        Timerist.resize(650, 550)
        Timerist.setWindowIcon(QtGui.QIcon('app_icon.ico'))

        self.TodoOptionsLayout = QHBoxLayout()
        self.TodoLayout = QVBoxLayout()

        self.documentsOptionsLayout = QHBoxLayout()
        self.documentsLayout = QVBoxLayout()

        self.MainWidget = QtWidgets.QWidget()

        self.opened = False
        self.tool_btn_size = QtCore.QSize(400, 400)
        self.tool_btn_size_2 = QtCore.QSize(35, 35)
        self.tool_btn_size_3 = QtCore.QSize(15, 15)
        self.sound = sound

        self.email = email
        self.password = password

        font = QtGui.QFont()
        font.setPointSize(20)
        self.todo_label = QtWidgets.QLabel(self.MainWidget)
        self.todo_label.setGeometry(QtCore.QRect(100, 2, 241, 51))
        self.todo_label.setFont(font)
        self.todo_label.setText("To Do List: ")

        self.documents_label = QtWidgets.QLabel(self.MainWidget)
        self.documents_label.setGeometry(QtCore.QRect(100, 2, 241, 51))
        self.documents_label.setFont(font)
        self.documents_label.setText("Documents: ")
        self.treeWidget = QtWidgets.QTreeWidget(self.MainWidget)
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidget.setMinimumHeight(300)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setHeaderLabels(["Date", "Task", "Status"])
        self.fillTreeWidget()


        self.refresh = QtWidgets.QPushButton("Refresh")
        self.refresh.setToolTip("Refresh Your Tasks")
        self.refresh.clicked.connect(self.Refresh)

        self.clear = QtWidgets.QPushButton("Clear")
        self.clear.setToolTip("Clear Your Tasks")
        self.clear.clicked.connect(self.Clear)

        self.documentsDatabase = QtWidgets.QListWidget(self.MainWidget)
        self.documentsDatabase.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.documentsDatabase.setMinimumHeight(300)
        for root, dirs, files in os.walk(f"users/{self.email}/database"):
            for filename in files:
                QtWidgets.QListWidgetItem(filename, self.documentsDatabase)

        self.create_document = QtWidgets.QPushButton("Create", self.MainWidget)
        self.create_document.setToolTip("Create A Document")
        self.create_document.setGeometry(QtCore.QRect(320, 320, 100, 30))
        self.create_document.clicked.connect(self.Createdocument)
        self.remove_document = QtWidgets.QPushButton("Delete", self.MainWidget)
        self.remove_document.setGeometry(QtCore.QRect(100, 320, 100, 30))
        self.remove_document.setToolTip("Delete A Document")
        self.remove_document.clicked.connect(self.remove)
        self.edit_document = QtWidgets.QPushButton("Edit", self.MainWidget)
        self.edit_document.setToolTip("Open In Editor")
        self.edit_document.setGeometry(QtCore.QRect(210, 320, 100, 30))
        self.edit_document.clicked.connect(self.edit)
        self.open_document = QtWidgets.QPushButton("Export", self.MainWidget)
        self.open_document.setToolTip("Print Or Embed")
        self.open_document.setGeometry(QtCore.QRect(320, 320, 100, 30))
        self.open_document.clicked.connect(self.Opendocument)

        self.pushButton = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 260, 83, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(115, 260, 83, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(205, 260, 83, 28))
        self.pushButton_3.setText("Update")
        self.pushButton_3.setToolTip("Update The Status")
        self.pushButton_4 = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton_4.setGeometry(QtCore.QRect(295, 260, 83, 28))
        self.pushButton_4.setText("View")
        self.pushButton_4.setToolTip("View the Timer")
        self.pushButton_3.clicked.connect(self.update_todo)
        self.pushButton_4.clicked.connect(self.view_todo)
        self.color_theme_btn = AnimatedToggle(checked_color="#4c5375")
        self.color_theme_btn.setMinimumSize(80, 10)
        self.color_theme_btn.setToolTip("Dark Mode: Off")
        self.color_theme_btn.stateChanged.connect(
            lambda x: self.dark_theme() if x else self.light_theme()
        )

        self.username = self.email.partition('@')[0]
        self.usernameLabel = QLabel(f"Hello, {self.username}")
        id = QFontDatabase.addApplicationFont("assets/Poppins-Medium.ttf")
        _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
        _font = QFont(_fontstr, 20)
        self.usernameLabel.setFont(_font)

        self.viewCopyright = QtWidgets.QToolButton(self.MainWidget)
        self.viewCopyright.setIcon(QtGui.QIcon("images/copyright.png"))
        self.viewCopyright.setToolTip("View Copyright")
        self.viewCopyright.setIconSize(self.tool_btn_size_2)
        self.viewCopyright.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.viewCopyright.clicked.connect(self.CopyrightShow)


        self.TodoOptionsLayout.addWidget(self.todo_label, alignment=Qt.AlignTop)
        self.TodoOptionsLayout.addWidget(self.pushButton, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_2, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_3, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_4, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.refresh, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.clear, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addStretch(8)
        self.TodoOptionsLayout.addWidget(self.usernameLabel, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.color_theme_btn, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.viewCopyright, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addStretch()
        self.TodoLayout.addLayout(self.TodoOptionsLayout)
        self.TodoLayout.addWidget(self.treeWidget)
        self.TodoLayout.addStretch()
        # Newest Layout for MainWidget
        self.documentsLayout.addLayout(self.TodoLayout)
        self.documentsOptionsLayout.addWidget(self.documents_label, alignment=Qt.AlignTop)
        self.documentsOptionsLayout.addWidget(self.create_document, alignment=Qt.AlignLeft)
        self.documentsOptionsLayout.addWidget(self.remove_document, alignment=Qt.AlignLeft)
        self.documentsOptionsLayout.addWidget(self.edit_document, alignment=Qt.AlignLeft)
        self.documentsOptionsLayout.addWidget(self.open_document, alignment=Qt.AlignLeft)
        self.documentsOptionsLayout.addStretch()
        self.documentsLayout.addLayout(self.documentsOptionsLayout)
        self.documentsLayout.addWidget(self.documentsDatabase)
        self.MainWidget.setLayout(self.documentsLayout)
        self.scrollWidget = QtWidgets.QScrollArea()
        self.scrollWidget.setWidget(self.MainWidget)
        self.scrollWidget.setWidgetResizable(True)
        Timerist.setCentralWidget(self.scrollWidget)



        self.retranslateUi(Timerist)
        QtCore.QMetaObject.connectSlotsByName(Timerist)


    def Clear(self):
        ask = QtWidgets.QMessageBox.question(Timerist, "Are you sure ?", "Are you sure that you want to delete all of your todos ?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if ask == QtWidgets.QMessageBox.Yes:
            file=open(f"users/{self.email}/data.txt", "w").close() # Erases all of the Data
            self.treeWidget.clear()
        else:
            pass
    
    def Refresh(self):
        self.fillTreeWidget()
        
    def fillTreeWidget(self):
        self.treeWidget.clear()
        file = open(f"users/{self.email}/data.txt", "r", encoding='utf-8')
        data = file.readlines()
        file.close()
        data = [line.replace('\n', '') for line in data]
        desired_lines = data[0::1]
        fov = slice_per(desired_lines, 3)
        for e in fov:
            if start_timer(e[0]) == 'yes' and e[2] == "Incomplete ❌": # Checks for overdue todos.
                edit_item(e, e[0], e[1], 'Overdue ⌛', f"users/{self.email}/data.txt")
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
            else:
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)


    def retranslateUi(self, Timerist):
        _translate = QtCore.QCoreApplication.translate
        Timerist.setWindowTitle(_translate("Timerist", "Timerist"))
        self.pushButton.setText(_translate("Timerist", "Add"))
        self.pushButton.setToolTip("Add A Task")
        self.pushButton.clicked.connect(self.add_todo)
        self.pushButton_2.setText(_translate("Timerist", "Remove"))
        self.pushButton_2.setToolTip("Remove A Task")
        self.pushButton_2.clicked.connect(self.remove_todo)

    def add_todo(self):
        add = AddTodoForm(Timerist, "Add Todo", self.treeWidget, user=self.email)
        add.show()

    def remove_todo(self):
        ask = QtWidgets.QMessageBox.question(Timerist, "Are you sure ?", "Are you sure that you want to delete these todo(s) ?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if ask == QtWidgets.QMessageBox.Yes:
            items = self.treeWidget.selectedItems()
            if len(items) >= 0:
                for item in items:
                    item_text = [item.text(0), item.text(1), item.text(2)]
                    self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))
                    delete_item_from_query(item_text, path=f'users/{self.email}/data.txt')
            else:
                QtWidgets.QMessageBox.warning(Timerist, "Select a document", "Please select a document so that an action can be completed.")
        else:
            pass

    def update_todo(self):
        items = self.treeWidget.selectedItems()
        for item in items:
            item_text_prev = [item.text(0), item.text(1), item.text(2)]
            if item_text_prev[2] == "Incomplete ❌":
                item.setText(2, "Completed ✅")
                item_text_new = [item.text(0), item.text(1), item.text(2)]
                change_item_from_query(item_text_prev, item_text_new, f'users/{self.email}/data.txt')
            elif item_text_prev[2] == "Overdue ⌛":
                item.setText(2, "Completed ✅")
                item_text_new = [item.text(0), item.text(1), item.text(2)]
                change_item_from_query(item_text_prev, item_text_new, f'users/{self.email}/data.txt')
            elif item_text_prev[2] == "Completed ✅":
                item.setText(2, "Incomplete ❌")
                item_text_new = [item.text(0), item.text(1), item.text(2)]
                change_item_from_query(item_text_prev, item_text_new, f'users/{self.email}/data.txt')

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
        self.openWin = OpenWindow(Timerist, self.textEdit, user=self.email)
        self.openWin.show()

    def Save(self):
        save = CreateWindow(Timerist, self.textEdit.toHtml(), user=self.email)
        save.show()

    def save_changes(self):
        try:
            file = open(self.openWin.filename, 'w', encoding='utf-8').close()
            with open(self.openWin.filename, "w", encoding='utf-8') as f:
                f.write(self.textEdit.toHtml())
                f.close()
            QtWidgets.QMessageBox.information(Timerist, "Saved!", f"Your changes were saved successfully.")
        except:
            QtWidgets.QMessageBox.warning(Timerist, "Saving Error", "Please open an existing document to save your changes.")

    def remove(self):
        items = []
        ask = QtWidgets.QMessageBox.question(Timerist, "Are you sure ?", "Are you sure that you want to delete these document(s) ?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        if ask == QtWidgets.QMessageBox.Yes:
            for item in self.documentsDatabase.selectedItems():
                items.append(item)
                if len(items) >= 1:
                    self.documentsDatabase.takeItem(self.documentsDatabase.row(item))
                    os.remove(f"users/{self.email}/database/{item.text()}")
                else:
                    QtWidgets.QMessageBox.warning(Timerist, "Select a document", "Please select a document so that an action can be completed.")
        else:
            pass

    def edit(self):
        try:
            selected = [item.text() for item in self.documentsDatabase.selectedItems()]
            for item in selected:
                file = open(f"users/{self.email}/database/{item}", "r", encoding='utf-8')
                data = file.read()
                file.close()
                edit_window = EditWindow(Timerist, f"{item}", f"{data}", database=self.documentsDatabase, user=self.email)
                edit_window.show()
        except:
            QtWidgets.QMessageBox.warning(Timerist, "Select a document", "Please select a document so that an action can be completed.")




    def Opendocument(self):
        try:
            selected = [item.text() for item in self.documentsDatabase.selectedItems()]
            for item in selected:
                file = open(f"users/{self.email}/database/{item}", "r", encoding='utf-8')
                data = file.read()
                file.close()
                read_window = ReadWindow(Timerist, f"{item}", text=data, user=self.email)
                read_window.show()
        except:
            QtWidgets.QMessageBox.warning(Timerist, "Select a document", "Please select a document so that an action can be completed.")

        # Code debugging
        '''
        selected = [item.text() for item in self.documentsDatabase.selectedItems()]
        print(selected)
        for item in selected:
            file = open(f"users/{self.email}/database/{item}", "r", encoding='utf-8')
            data = file.read()
            file.close()
            read_window = ReadWindow(Timerist, f"{item}", text=data, user=self.email)
            read_window.show()
        '''

    def dark_theme(self):
        # Loads the Dark Theme mode for the app
        app.setStyleSheet(load_from_stylesheet("assets/dark-theme.qss"))
        self.color_theme_btn.setToolTip("Dark Mode: On")

    def light_theme(self):
        # Loads the Light Theme mode for the app
        app.setStyleSheet(load_from_stylesheet("assets/light-theme.qss"))
        self.color_theme_btn.setToolTip("Dark Mode: Off")


    def Createdocument(self):
        create = CreateWindow(Timerist, database=self.documentsDatabase, user=self.email)
        create.show()

    def CopyrightShow(self):
        CopyrightWin = QtWidgets.QMainWindow(Timerist)
        CopyrightWin.resize(500, 350)
        CopyrightWin.setWindowTitle("Copyright")
        CopyrightWin.setWindowIcon(QIcon("images/copyright.png"))
        layout = QVBoxLayout()
        widget = QtWidgets.QWidget()
        copyright_text = QTextEdit(widget)
        copyright_text.setReadOnly(True)
        copyright_text.setCursor(Qt.PointingHandCursor)
        copyright_text.setText(open("assets/LICENSE", "r").read())
        copyright_font_id = QFontDatabase.addApplicationFont("assets/Segoe UI.ttf")
        copyright_text_font_family = QFontDatabase.applicationFontFamilies(copyright_font_id)[0]
        copyright_text_font = QFont(copyright_text_font_family, 13)
        copyright_text.setFont(copyright_text_font)
        layout.addWidget(copyright_text)
        widget.setLayout(layout)
        CopyrightWin.setCentralWidget(widget)
        CopyrightWin.show()

app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')
app.setStyleSheet(load_from_stylesheet('assets/light-theme.qss'))
Timerist = QtWidgets.QMainWindow()
Timerist.setObjectName("Timerist")
ui = Ui_Timerist()
