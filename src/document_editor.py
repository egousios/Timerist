from imports import *

class EditWindow(QtWidgets.QMainWindow):
    def __init__(self, Parent, title, text, user=None, database=None):
        super().__init__(parent=Parent)
        self.user = user
        self.resize(500, 400)
        self.setWindowTitle(f"{title}")
        self.title = title
        self.database = database
        self.Opened = False
        self.layout = QHBoxLayout()
        self.layout2 = QVBoxLayout()
        self.widget = QtWidgets.QWidget(self)
        self.editor_settings = load_editor_settings(f"users/{self.user}/editor_settings.json")
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(20, 20, 400, 350))
        self.textEdit.setObjectName("textEdit")

        if "'background-color'" in self.editor_settings:
            color = self.editor_settings["'background-color'"]
            ev = eval(color)
            sheet = f"background-color: rgba{ev};"
            self.textEdit.setStyleSheet(sheet)
        if "'background-image'" in self.editor_settings:
            img = self.editor_settings["'background-image'"]
            sheet = f"background-image: url({img});"
            self.textEdit.setStyleSheet(sheet)
        if "'save-on-close'" in self.editor_settings:
            ev = eval(self.editor_settings["'save-on-close'"])
            if ev == 'True':
                self.toggle_close_saving(True)
            elif ev == 'False':
                self.toggle_close_saving(False)

        self.editor_bg_color_clicked = False
        self.editor_bg_image_clicked = False
        self.toggle_close_saving_clicked = False
        self.editor_save_on_close = True
        self.bg_image_filename = None
        self.bg_color = None  
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
        self.pushButtonCreate.clicked.connect(self.createdocument)
        self.pushButtonOpen = QtWidgets.QToolButton(self.widget)
        self.pushButtonOpen.setIcon(QtGui.QIcon("images/open.png"))
        self.pushButtonOpen.setToolTip("Open")
        self.pushButtonOpen.setShortcut("Ctrl+O")
        self.pushButtonOpen.setIconSize(self.tool_btn_size)
        self.pushButtonOpen.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.pushButtonOpen.clicked.connect(self.opendocument)


        self.pushButton = QtWidgets.QToolButton(self.widget)
        self.pushButton.setIcon(QtGui.QIcon("images/save.png"))
        self.pushButton.setToolTip("Save")
        self.pushButton.setShortcut("Ctrl+S")
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

    def save(self):
        try:
            file = open(f"users/{self.user}/database/{self.title}", 'w', encoding='utf-8').close()
            with open(f"users/{self.user}/database/{self.title}", "w", encoding='utf-8') as f:
                f.write(self.textEdit.toHtml())
                f.close()
            QtWidgets.QMessageBox.information(Timerist, "Saved!", f"Your changes were saved successfully.")
        except:
            QtWidgets.QMessageBox.warning(Timerist, "Saving Error", "Please open an existing document to save your changes.")


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
            QtWidgets.QMessageBox.critical(self, "Fatal!", "Could not insert selected image.")


    def change_line_wrap(self):
        if self.pushButton18.isChecked():
            self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        else:
            self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

    def closeNoSave(self, e):
        self.destroy()

    def settings(self):
        self.settings_win = QtWidgets.QDialog(self)
        self.settings_win.setWindowFlags(Qt.WindowType.Window)
        self.settings_win.resize(500, 400)
        self.settings_win.setWindowIcon(QtGui.QIcon("images/settings.png"))
        self.settings_win.setWindowTitle("Editor Settings")
        self.edit_from_json = QAction()
        self.edit_from_json.setIcon(QIcon("images/gears.png"))
        self.edit_from_json.setToolTip("Open Settings In JSON")
        self.edit_from_json.triggered.connect(self.open_json)
        tlb = QToolBar()
        tlb.addAction(self.edit_from_json)

        label_font = QtGui.QFont()
        label_font.setPointSize(20)
        detail_font = QtGui.QFont()
        detail_font.setPointSize(15)

        tab_layout = QtWidgets.QVBoxLayout()

        tabs = TabWidget()

        # tabs -> apperance, preferances 

        apperance_tab = QtWidgets.QWidget()
        preferances_tab = QtWidgets.QWidget()

        tabs.addTab(apperance_tab, "Apperance")
        tabs.addTab(preferances_tab, "Preferances")

        tab_layout.addWidget(tlb)
        tab_layout.addWidget(tabs)

        apperance_tab_layout = QVBoxLayout()

        apperance_form_layout = QFormLayout()
        apperance_form_widget = QtWidgets.QWidget()

        background_field_label = QtWidgets.QLabel("Background")
        background_field_label.setFont(label_font)

        selected_bg_label = QtWidgets.QLabel("Selected Background:")
        selected_bg_label.setFont(detail_font)

        background_field_options_widget = QtWidgets.QWidget()
        background_field_options_layout = QHBoxLayout()

        
        self.selected_bg_widget = QtWidgets.QLabel()
        if not "'background-color'" in self.editor_settings:
            self.selected_bg_widget.setText("(255,255,255)")
            if not "'background-image'" in self.editor_settings:
                self.selected_bg_widget.setText("(255,255,255)")
            else:
                self.selected_bg_widget.setText(eval(self.editor_settings["'background-image'"]))       
        else:
            self.selected_bg_widget.setText(eval(self.editor_settings["'background-color'"]))
        #theme_field_options_widget.stateChanged.connect(self.settings_change_theme)

        background_field_option1 = QtWidgets.QPushButton("Color")
        background_field_option1.clicked.connect(self.change_editor_bg_color)
        background_field_option2 = QtWidgets.QPushButton("Image")
        background_field_option2.clicked.connect(self.change_editor_bg_image)


        background_field_options_layout.addWidget(background_field_option1)
        background_field_options_layout.addWidget(background_field_option2)
        
        background_field_options_widget.setLayout(background_field_options_layout)

        apperance_form_layout.addRow(background_field_label, background_field_options_widget)
        apperance_form_layout.addRow(selected_bg_label, self.selected_bg_widget)

        apperance_buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        apperance_buttonBox.accepted.connect(self.apperanceOk)
        apperance_buttonBox.rejected.connect(self.apperanceNo)

        apperance_form_widget.setLayout(apperance_form_layout)

        apperance_tab_layout.addWidget(apperance_form_widget)
        apperance_tab_layout.addWidget(apperance_buttonBox)

        apperance_tab.setLayout(apperance_tab_layout)

        ###############################
        preferances_tab_layout = QVBoxLayout()

        preferances_form_layout = QFormLayout()
        preferances_form_widget = QtWidgets.QWidget()

        
        show_save_on_close_label = QtWidgets.QLabel("Show Save Dialog On Close: ")
        show_save_on_close_label.setFont(detail_font)

        self.show_save_on_close_toggle = AnimatedToggle(checked_color="#36d1d1")
        self.show_save_on_close_toggle.stateChanged.connect(lambda x: self.toggle_close_saving(True) if x else self.toggle_close_saving(False))
        if not "'save-on-close'" in self.editor_settings:
            self.show_save_on_close_toggle.setChecked(True)
        elif "'save-on-close'" in self.editor_settings:
            if eval(self.editor_settings["'save-on-close'"]) == 'True':
                self.show_save_on_close_toggle.setChecked(True)
            elif eval(self.editor_settings["'save-on-close'"]) == 'False':
                self.show_save_on_close_toggle.setChecked(False)


        preferances_form_layout.addRow(show_save_on_close_label, self.show_save_on_close_toggle)

        preferances_form_widget.setLayout(preferances_form_layout)

        preferances_buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        preferances_buttonBox.accepted.connect(self.preferancesOk)
        preferances_buttonBox.rejected.connect(self.preferancesNo)

        preferances_tab_layout.addWidget(preferances_form_widget)
        preferances_tab_layout.addWidget(preferances_buttonBox)

        preferances_tab.setLayout(preferances_tab_layout)

        self.settings_win.setLayout(tab_layout)
        self.settings_win.show()

    def jsonOk(self):
        data = self.JSONtext.text()
        file=open(f"users/{self.user}/editor_settings.json", "w").close()
        with open(f"users/{self.user}/editor_settings.json", "w") as f:
            f.write(data)
            f.close()

    def jsonNo(self):
        self.win.destroy()

    def open_json(self):
        self.win = QtWidgets.QMainWindow(Timerist)
        self.win.resize(500, 350)
        self.win.setWindowTitle("Editor Settings (JSON)")
        self.win.setWindowIcon(QIcon("images/settings.png"))
        layout = QVBoxLayout()
        widget = QtWidgets.QWidget()
        data = open(f"users/{self.user}/editor_settings.json", "r").read()
        self.JSONtext = SimpleJSONEditor(widget)
        self.JSONtext.setText(data)
        save = QPushButton("Save")
        save.setShortcut("Ctrl+S")
        save.clicked.connect(self.jsonOk)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.jsonNo)
        hl = QHBoxLayout()
        hl.addWidget(save, 50)
        hl.addWidget(cancel, 50)
        wid = QWidget()
        wid.setLayout(hl)
        layout.addWidget(self.JSONtext)
        layout.addWidget(wid)
        widget.setLayout(layout)
        self.win.setCentralWidget(widget)
        self.win.show()

    def toggle_close_saving(self, x):
        self.toggle_close_saving_clicked = True
        if x == True:
            self.editor_save_on_close = True
            self.destroyed.connect(self.closeEvent)
        else:
            self.editor_save_on_close = False
            self.destroyed.connect(self.closeEvent)

    def change_editor_bg_color(self):
        self.editor_bg_color_clicked = True
        # get color from dialog
        dialog = QColorDialog().getColor()
        if dialog.isValid():
            self.bg_color = dialog.getRgb()
            self.textEdit.setStyleSheet(f"background-color: rgba{self.bg_color};")
            self.selected_bg_widget.setText(str(self.bg_color))


    def change_editor_bg_image(self):
        self.editor_bg_image_clicked = True
        # get image from file dialog
        try:
            file = QtWidgets.QFileDialog.getOpenFileName(self, "Insert Image", ".", "PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)")
            self.bg_image_filename = file[0]
            self.textEdit.setStyleSheet(f"background-image: url({self.bg_image_filename});")
            self.selected_bg_widget.setText(str(self.bg_image_filename))
        except:
            QtWidgets.QMessageBox.critical(self, "Fatal!", "Could not set selected image as background.") 

    def preferancesOk(self):
        if self.toggle_close_saving_clicked == True:
            previous_data = load_editor_settings(f"users/{self.user}/editor_settings.json")
            previous_data["'save-on-close'"] = f"'{self.editor_save_on_close}'"
            save_editor_settings(f"users/{self.user}/editor_settings.json", previous_data)

    def preferancesNo(self):
        self.settings_win.destroy()

    def apperanceOk(self):
        if self.editor_bg_color_clicked == True:
            previous_data = load_editor_settings(f"users/{self.user}/editor_settings.json")
            previous_data["'background-color'"] = f"'{self.bg_color}'"
            save_editor_settings(f"users/{self.user}/editor_settings.json", previous_data)
        elif self.editor_bg_image_clicked == True:
            previous_data = load_editor_settings(f"users/{self.user}/editor_settings.json")
            previous_data["'background-image'"] = f"'{self.bg_image_filename}'"
            save_editor_settings(f"users/{self.user}/editor_settings.json", previous_data)

    def apperanceNo(self):
        self.settings_win.destroy()

    def closeEvent(self, e):
        if self.toggle_close_saving_clicked == True:
            if self.editor_save_on_close == True:
                msg_save = QtWidgets.QMessageBox.question(self, "Save Changes", "Would you like to save your changes?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
                if msg_save == QtWidgets.QMessageBox.Yes:
                    try:
                        file = open(f"users/{self.user}/database/{self.title}", 'w', encoding='utf-8').close()
                        with open(f"users/{self.user}/database/{self.title}", "w", encoding='utf-8') as f:
                            f.write(self.textEdit.toHtml())
                            f.close()
                        QtWidgets.QMessageBox.information(self, "Saved!", f"Your changes were saved successfully.")
                    except:
                        QtWidgets.QMessageBox.warning(self, "Saving Error", "Please open an existing document to save your changes.")
                else:
                    pass
            elif self.editor_save_on_close == False:
                pass
        else:
            if "'save-on-close'" in self.editor_settings:
                if eval(self.editor_settings["'save-on-close'"]) == 'True':
                    msg_save = QtWidgets.QMessageBox.question(self, "Save Changes", "Would you like to save your changes?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
                    if msg_save == QtWidgets.QMessageBox.Yes:
                        try:
                            file = open(f"users/{self.user}/database/{self.title}", 'w', encoding='utf-8').close()
                            with open(f"users/{self.user}/database/{self.title}", "w", encoding='utf-8') as f:
                                f.write(self.textEdit.toHtml())
                                f.close()
                            QtWidgets.QMessageBox.information(self, "Saved!", f"Your changes were saved successfully.")
                        except:
                            QtWidgets.QMessageBox.warning(self, "Saving Error", "Please open an existing document to save your changes.")
                    else:
                        pass
                else:
                    pass

    def createdocument(self):
        if self.database != None:
            create = CreateWindow(self, self.textEdit.toHtml(), database=self.database, user=self.user)
            create.show()
        else:
            create = CreateWindow(self, self.textEdit.toHtml(), user=self.user)
            create.show()
        

    def opendocument(self):
        self.openWin = OpenWindow(self, self.textEdit, winTitle=self, user=self.user)
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