from PyQt5.QtWidgets import (
    QScrollArea, QHBoxLayout, QVBoxLayout, QAbstractItemView, QComboBox,
    QHeaderView, QLabel, QPushButton, QTabWidget, QWidget, QMessageBox
)
from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QPixmap
from PyQt5.QtCore import QSize, Qt

from dialogs.AdvancedTodoSearchFilterDialog import AdvancedTodoSearchFilterDialog
from imports import *
from forms import *
from todo_side_menu.Components.archived_todo import ArchivedTodo
from todo_side_menu.Components.recycled_todo import RecycledTodo
sys.path.insert(0, "../")
from auth import Auth
from todo_side_menu.archive_manager import ArchiveManager
from todo_side_menu.recycle_bin import RecycleBin
from custom_components.profile_pic_picker import ProfilePicPicker, BigProfilePicPicker
from custom_components.search_bar import SearchBar
from json_settings.user_settings import load_user_settings, save_user_settings
from utils import (
    load_json_data_from_json_file, get_route_to_data, return_contents_from_query,
    is_item, delete_item_from_query
)
from theme_editor import THEMES, THEME_FILES, SAVED_THEME_DATAS_SOURCE
from hash import hash_char_for_astrix

import shutil
from datetime import datetime
import sys

QMENU_STYLESHEET = """
QMenu { 
    background-color: black; 
    color: white; 
    border: black solid 1px;
}
"""

class QTreeWidgetCustom(QtWidgets.QTreeWidget):
    def __init__(self, parent, email):
        super().__init__(parent=parent)
        self.email = email

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        contextMenu.setStyleSheet(QMENU_STYLESHEET)
        archive = contextMenu.addAction("Archive")
        recycle = contextMenu.addAction("Recycle")
        edit = contextMenu.addAction("Edit")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == archive:
            self.Archive()
        elif action == recycle:
            self.Recycle()
        elif action == edit:
            self.Edit()

    def Archive(self):
        for item in self.selectedItems():
            data = [item.text(0), item.text(1), item.text(2)]

            if is_item(data, get_route_to_data(self.email, "archived_tasks")):
                QMessageBox.critical(Timerist, "Error", "Couldn't archive todo because todo is already archived.")
            else:
                branch = Tree(branches={
                    "end_time": data[0],
                    "task": data[1],
                    "status": data[2],
                })
                branch.save(branch.branches, id="all", path=get_route_to_data(self.email, "archived_tasks"))
                self.takeTopLevelItem(self.indexOfTopLevelItem(item))
                delete_item_from_query(data, path=get_route_to_data(self.email, "availible_tasks"))
                todo_object = ArchivedTodo(self.archiveWid, data)
                todo_object.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0d0e0f;}")
                self.archiveWid.todos.append(todo_object)
                self.archiveWid.main_layout.addWidget(todo_object)

    def Recycle(self):
        for item in self.selectedItems():
            data = [item.text(0), item.text(1), item.text(2)]

            if is_item(data, get_route_to_data(self.email, "recycled_tasks")):
                QMessageBox.critical(Timerist, "Error", "Couldn't recycle todo because todo is already recycled.")
            else:
                branch = Tree(branches={
                    "end_time": data[0],
                    "task": data[1],
                    "status": data[2],
                })
                branch.save(branch.branches, id="all", path=get_route_to_data(self.email, "recycled_tasks"))
                self.takeTopLevelItem(self.indexOfTopLevelItem(item))
                delete_item_from_query(data, path=get_route_to_data(self.email, "availible_tasks"))
                todo_object = RecycledTodo(self.recycleWid, data)
                todo_object.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0d0e0f;}")
                self.recycleWid.todos.append(todo_object)
                self.recycleWid.main_layout.addWidget(todo_object)

    def Edit(self):
        items = self.selectedItems()
        for item in items:
            editDlg = EditTodoForm(
                self,
                f"Editing Todo - {item.text(1)}",
                self,
                user=self.email,
                item_to_edit=item,
                prev_data=[item.text(0), item.text(1), item.text(2)]
            )
            editDlg.show()


"""Settings Constants"""

app = QtWidgets.QApplication(sys.argv)

# Add this to the stylesheets to regulate system appearance.
THEME_REGULATOR = """
QTreeWidget QHeaderView::section {
    font-size: 12pt;
}

QMenu { 
    background: transparent;
    color: white; 
    border: black solid 1px;
}

QLineEdit {
    font-size: 11.5px;
}

QMainWindow {
    color: #fff;
}

QScrollArea {
    background: transparent;
}
"""

CURSORS = [
    "Default", "Windows", "Large Windows", "Mega Windows",
    "Medium Windows", "Semi-Medium Windows", "Mac 1",
    "Mac 2", "Mac 3", "Mac 4",
    "Mac 5", "Legacy 1", "Legacy 2",
    "Legacy 3", "Legacy 4", "Legacy 5",
    "Linux"
]

CURSOR_FILES = [
    "Default",
    "cursors/windows/regular_win.png",
    "cursors/windows/semi_mega_win.png",
    "cursors/windows/mega_win.png",
    "cursors/windows/medium_win.png",
    "cursors/windows/semi_medium_win.png",
    "cursors/mac/1_mac.png",
    "cursors/mac/2_mac.png",
    "cursors/mac/3_mac.png",
    "cursors/mac/4_mac.png",
    "cursors/mac/5_mac.png",
    "cursors/legacy/legacy1.png",
    "cursors/legacy/legacy2.png",
    "cursors/legacy/legacy3.png",
    "cursors/legacy/legacy4.png",
    "cursors/legacy/legacy5.png",
    "cursors/linux.png"
]

TASK_FONT_SIZE_RANGE = (6, 100)

FONTS = [font for font in QFontDatabase().families()]
FONTS[0] = "Default"

FONT_CHANGEABLE_WIDGETS = [
    "QPushButton",
    "QLabel",
    "QLineEdit",
    "QMessageBox",
    "QSpinBox",
    "QCalendarWidget",
    "QDialog",
    "QFrame",
    "QToolTip",
    "QTabWidget",
    "QMenu",
    "QPlainTextEdit",
    "QTextEdit"
]

TREE_WIDGET_FILTERS = ["All", "Overdue ⌛", "Incomplete ❌", "Completed ✅"]

class Ui_Timerist(object):
    def setupUi(self, Timerist, sound, email, password, cached_password, uid, email_verified, auth, idToken):
        Timerist.setObjectName("Timerist")
        Timerist.resize(650, 550)
        Timerist.setWindowIcon(QtGui.QIcon('app_icon.ico'))
        Timerist.destroyed.connect(self.closeEvent)

        self.TodoOptionsLayout = QHBoxLayout()
        self.TodoLayout = QVBoxLayout()

        self.MainWidget = QtWidgets.QWidget()

        self.opened = False
        self.tool_btn_size = QtCore.QSize(400, 400)
        self.tool_btn_size_2 = QtCore.QSize(50, 50)
        self.tool_btn_size_3 = QtCore.QSize(15, 15)
        self.sound = sound

        self.email = email
        self.password = password
        self.cached_password = cached_password
        self.user_id = uid
        self.email_verified = email_verified
        self.auth = auth
        self.idToken = idToken
        self.shouldPlayTimerOnOpen = True
        self.showConfirmationDialogBeforeEmptyBin = True
        self.user_settings_path = get_route_to_data(self.email, "user_settings")

        self.default_config = {
            "theme":"Default",
            "cursor":"Default",
            "task_font_size":14,
            "selected_font":"Default",
            "should_play_timer_on_open":True,
            "show_confirmation_dialog_before_emptying_bin":True,
        }

        try:
            self.user_settings = load_user_settings(self.user_settings_path)
        except:
            self.user_settings = {"background-image":"images/account.png", "config":self.default_config}

        try:
            self.user_config = self.user_settings["config"]
        except:
            self.user_config = self.default_config

        self.selected_theme = self.user_config["theme"]
        self.selected_cursor = self.user_config["cursor"]
        self.selected_task_font_size = self.user_config["task_font_size"]
        self.selected_font = self.user_config["selected_font"]
        self.shouldPlayTimerOnOpen = self.user_config["should_play_timer_on_open"]
        self.showConfirmationDialogBeforeEmptyBin = self.user_config["show_confirmation_dialog_before_emptying_bin"]

        self.config = {
            "theme":self.selected_theme,
            "cursor":self.selected_cursor,
            "task_font_size":self.selected_task_font_size,
            "selected_font":self.selected_font,
            "should_play_timer_on_open":self.shouldPlayTimerOnOpen,
            "show_confirmation_dialog_before_emptying_bin":self.showConfirmationDialogBeforeEmptyBin
        }

        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_font = QFont("Poppins", 15)

        ### Context Menu Tabs
        self.ArchivedTodos = ArchiveManager(
            Timerist, get_route_to_data(self.email, "availible_tasks"),
            return_contents_from_query(get_route_to_data(self.email, "archived_tasks")),
            email=self.email, maker=self, manager=self
        )
        self.RecycledTodos = RecycleBin(
            Timerist, get_route_to_data(self.email, "availible_tasks"),
            return_contents_from_query(get_route_to_data(self.email, "recycled_tasks")),
            email=self.email, maker=self, manager=self,
            showConfirmationBeforeEmpty=self.showConfirmationDialogBeforeEmptyBin
        )

        self.tree_filter_mode = "All"

        self.treeWidget = QTreeWidgetCustom(self.MainWidget, self.email)
        self.treeWidget.archiveWid = self.ArchivedTodos
        self.treeWidget.recycleWid = self.RecycledTodos
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        header = self.treeWidget.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.treeWidget.setMinimumHeight(300)
        self.treeWidget.setMinimumWidth(500)
        self.treeWidget.setObjectName("treeWidget")
        default_font = QFont("Poppins")
        default_font.setPointSize(self.selected_task_font_size)
        self.treeWidget.setFont(default_font)
        self.treeWidget.setHeaderLabels(["Due Date", "Task", "Status"])
        self.treeWidget.installEventFilter(Timerist)
        self.fillTreeWidget()

        self.treeWidgetFilterLabel = QLabel("Filter: ")
        self.treeWidgetFilterLabel.setFont(self.label_font)

        self.treeWidgetSearchBar = SearchBar(placeholder_text="Search For Tasks Here...")
        self.treeWidgetSearchBar.textChanged.connect(self.search_todo)

        self.treeWidgetFilter = QComboBox()
        self.treeWidgetFilter.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLength)

        self.treeWidgetFilter.addItems(TREE_WIDGET_FILTERS)
        self.treeWidgetFilter.setCurrentIndex(TREE_WIDGET_FILTERS.index("All"))
        self.treeWidgetFilter.setStyleSheet("""
        QComboBox{ background-color: white; color: black; }
        """)
        self.treeWidgetFilter.activated.connect(self.change_tree_filter_mode)

        self.open_advanced_todo_search_btn = QPushButton("Advanced...")
        self.open_advanced_todo_search_btn.setMaximumWidth(180)
        self.open_advanced_todo_search_btn.clicked.connect(self.open_advanced_todo_search_dialog)

        self.treeWidgetFilterLayout = QHBoxLayout()
        self.treeWidgetFilterLayout.addWidget(self.treeWidgetFilter)
        self.treeWidgetFilterLayout.addWidget(self.open_advanced_todo_search_btn)

        self.treeWidgetSection = QWidget()
        self.treeWidgetSectionLayout = QVBoxLayout()
        self.treeWidgetSectionLayout.addWidget(self.treeWidgetFilterLabel)
        self.treeWidgetSectionLayout.addWidget(self.treeWidgetSearchBar)
        self.treeWidgetSectionLayout.addLayout(self.treeWidgetFilterLayout)
        self.treeWidgetSectionLayout.addWidget(self.treeWidget)
        self.treeWidgetSection.setLayout(self.treeWidgetSectionLayout)

        """Context Menu UI"""
        self.TodoContextMenu=QTabWidget()
        self.TodoContextMenu.setStyleSheet("background-color: white;")
        self.TodoContextMenu.setMinimumHeight(300)

        self.archived_scrollbar = QScrollArea(widgetResizable=True)
        self.archived_scrollbar.setWidget(self.ArchivedTodos)

        self.recycled_scrollbar = QScrollArea(widgetResizable=True)
        self.recycled_scrollbar.setWidget(self.RecycledTodos)
        self.recycled_scrollbar.setMinimumWidth(self.recycled_scrollbar.widget().width())

        ### Tab Titles and Icons
        self.TodoContextMenu.addTab(self.archived_scrollbar, "Archived")
        self.TodoContextMenu.setTabIcon(0, QIcon("images/open.png"))
        self.TodoContextMenu.addTab(self.recycled_scrollbar, "Recycled")
        self.TodoContextMenu.setTabIcon(1, QIcon("images/recycle.png"))
        ### Context Menu Font
        self.TodoContextMenuFont = QFont()
        self.TodoContextMenuFont.setPointSize(15)
        self.TodoContextMenu.setFont(self.TodoContextMenuFont)
        self.TodoContextMenu.setIconSize(QtCore.QSize(32, 32))
        """Context Menu UI"""

        self.todo_label = QtWidgets.QLabel(self.MainWidget)
        self.todo_label.setGeometry(QtCore.QRect(100, 2, 241, 51))
        self.todo_label.setFont(font)
        self.todo_label.setText("To Do List: ")

        self.refresh = QtWidgets.QPushButton("Refresh")
        self.refresh.setToolTip("Refresh Your Tasks")
        self.refresh.clicked.connect(self.Refresh)

        self.clear = QtWidgets.QPushButton("Clear")
        self.clear.setToolTip("Clear Your Tasks")
        self.clear.clicked.connect(self.Clear)

        self.pushButton = QtWidgets.QPushButton(self.MainWidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 260, 83, 28))
       self.pushButton.setObjectName("pushButton")
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

        self.username = self.email.partition('@')[0]
        self.usernameLabel = QLabel(f"Hello, {self.username}")
        id = QFontDatabase.addApplicationFont("assets/Poppins-Medium.ttf")
        _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
        _font = QFont(_fontstr, 20)
        self.usernameLabel.setFont(_font)

        self.profile_pic = ProfilePicPicker(self.MainWidget, profile_pic=self.user_settings["background-image"], save_to=self.user_settings_path, func=save_user_settings, config=self.config)
        self.profile_pic.setFixedSize(QSize(50, 50))

        self.settingsWindow(show=False)
        self.change_theme()
        self.change_cursor()
        self.change_task_font_size()
        self.change_app_font()
        self.toggle_timer_on_open(self.shouldPlayTimerOnOpen)
        self.show_confirmation_before_empty_bin(self.showConfirmationDialogBeforeEmptyBin)

        self.settings = QtWidgets.QToolButton(self.MainWidget)
        self.settings.setIcon(QtGui.QIcon("images/settings.png"))
        self.settings.setToolTip("Settings")
        self.settings.setIconSize(self.tool_btn_size_2)
        self.settings.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.settings.clicked.connect(self.open_settings_win)

        self.viewCopyright = QtWidgets.QToolButton(self.MainWidget)
        self.viewCopyright.setIcon(QtGui.QIcon("images/copyright.png"))
        self.viewCopyright.setToolTip("View Copyright")
        self.viewCopyright.setIconSize(self.tool_btn_size_2)
        self.viewCopyright.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.viewCopyright.clicked.connect(self.CopyrightShow)

        self.logout = QtWidgets.QToolButton(self.MainWidget)
        self.logout.setIcon(QtGui.QIcon("images/logout.png"))
        self.logout.setToolTip("Logout")
        self.logout.setIconSize(self.tool_btn_size_2)
        self.logout.setGeometry(QtCore.QRect(150, 360, 110, 30))
        self.logout.clicked.connect(self.Logout)

        self.TodoOptionsLayout.addWidget(self.todo_label, alignment=Qt.AlignTop)
        self.TodoOptionsLayout.addWidget(self.pushButton, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_3, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.pushButton_4, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.refresh, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addWidget(self.clear, alignment=Qt.AlignLeft)
        self.TodoOptionsLayout.addStretch(8)
        self.TodoOptionsLayout.addWidget(self.usernameLabel, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.profile_pic, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.settings, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.viewCopyright, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addWidget(self.logout, alignment=Qt.AlignRight)
        self.TodoOptionsLayout.addStretch()

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.treeWidgetSection)
        self.main_layout.addWidget(self.TodoContextMenu)
        self.main_layout.setStretch(0, 50)
        self.main_layout.setStretch(1, 50)
        self.TodoLayout.addLayout(self.TodoOptionsLayout)
        self.TodoLayout.addLayout(self.main_layout)
        self.TodoLayout.setStretch(1, 1)
        # Newest Layout for MainWidget
        self.MainWidget.setLayout(self.TodoLayout)
        self.MainWidget.setStyleSheet("background-color: #fff")
        self.scrollWidget = QtWidgets.QScrollArea()
        self.scrollWidget.setWidget(self.MainWidget)
        self.scrollWidget.setWidgetResizable(True)
        g = QVBoxLayout()
        g.addWidget(self.scrollWidget)
        Timerist.setLayout(g)
        self.retranslateUi(Timerist)
        QtCore.QMetaObject.connectSlotsByName(Timerist)

    def get_tree(self):
        return self.treeWidget

    def Logout(self):
        background = load_user_settings(self.user_settings_path)["background-image"]
        if hasattr(self, "settings_win"):
            save_user_settings(self.user_settings_path, {"background-image":background, "config":self.config})
        save_user_settings(self.user_settings_path, {"background-image":background, "config":self.config})
        Timerist.destroy(destroyWindow=True, destroySubWindows=True)
        QApplication.instance().exit(0)
        os.system("python -u Timerist.py") # change to Timerist.exe

    def Refresh(self):
        self.fillTreeWidget(self.tree_filter_mode)

    def search_todo(self):
        # Get all root nodes
        all_items = self.treeWidget.findItems("", Qt.MatchStartsWith, column=1)
        # matching items
        match_items = self.treeWidget.findItems(self.treeWidgetSearchBar.text(), Qt.MatchStartsWith, column=1)
        # Hide all root nodes
        for item in all_items:
            item.setHidden(True)
        # Display the root node that meets the conditions
        for item in match_items:
            item.setHidden(False)

def Clear(self):
    ask = QtWidgets.QMessageBox.question(
        Timerist,
        "Are you sure ?",
        "Do you want to recycle all of your todos ?",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    )
    if ask == QtWidgets.QMessageBox.Yes:
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            if isinstance(item, QTreeWidgetItem):
                data = [item.text(0), item.text(1), item.text(2)]
                if is_item(data, get_route_to_data(self.email, "recycled_tasks")):
                    QMessageBox.critical(
                        Timerist,
                        "Error",
                        "Couldn't recycle todo because todo is already recycled."
                    )
                else:
                    branch = Tree(
                        branches={
                            "end_time": data[0],
                            "task": data[1],
                            "status": data[2],
                        }
                    )
                    branch.save(branch.branches, id="all", path=get_route_to_data(self.email, "recycled_tasks"))
                    self.treeWidget.takeTopLevelItem(i)
                    delete_item_from_query(data, path=get_route_to_data(self.email, "availible_tasks"))
                    todo_object = RecycledTodo(self.RecycledTodos, data)
                    todo_object.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0d0e0f;}")
                    self.RecycledTodos.todos.append(todo_object)
                    self.RecycledTodos.main_layout.addWidget(todo_object)

def open_advanced_todo_search_dialog(self):
    dialog = AdvancedTodoSearchFilterDialog(Timerist, fill_tree_function=self.fillTreeWidget, sort_tree_function=self.sortTreeWidget)
    dialog.show()

def closeEvent(self, evt):
    background = load_user_settings(self.user_settings_path)["background-image"]
    if hasattr(self, "settings_win"):
        save_user_settings(self.user_settings_path, {"background-image": background, "config": self.config})
    save_user_settings(self.user_settings_path, {"background-image": background, "config": self.config})
    Timerist.destroy(destroyWindow=True, destroySubWindows=True)

def fillTreeWidget(self, mode="All", date=None, date_range=None):
    self.treeWidget.clear()
    contents_from_query = return_contents_from_query(path=get_route_to_data(self.email, "availible_tasks"))
    contents_from_query = sorted(contents_from_query)
    for e in contents_from_query:
        if mode == "All":
            if start_timer(e[0]) == 'yes' and e[2] == "Incomplete ❌":
                edit_item(e, e[0], e[1], 'Overdue ⌛', get_route_to_data(self.email, "availible_tasks"))
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
            else:
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
        elif mode == "Overdue ⌛":
            if e[2] == "Overdue ⌛":
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
        elif mode == "Incomplete ❌":
            if e[2] == "Incomplete ❌":
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
        elif mode == "Completed ✅":
            if e[2] == "Completed ✅":
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
        elif mode == "Due Date":
            if date is not None:
                Date = e[0]
                year = int(Date[0:4])
                month = int(Date[5:7])
                day = int(Date[8:10])
                if QDate(year, month, day).toString("yyyy-MM-dd") == date:
                    Item = QTreeWidgetItem(e)
                    self.treeWidget.addTopLevelItem(Item)
        elif mode == "Due Date Range":
            if date_range is not None:
                Date = e[0]
                year = int(Date[0:4])
                month = int(Date[5:7])
                day = int(Date[8:10])
                if QDate(year, month, day).toString("yyyy-MM-dd") in get_date_range_list(*date_range):
                    Item = QTreeWidgetItem(e)
                    self.treeWidget.addTopLevelItem(Item)

def sortTreeWidget(self, sort_order):
    self.treeWidget.clear()
    contents_from_query = return_contents_from_query(path=get_route_to_data(self.email, "availible_tasks"))
    if sort_order == "Ascending":
        contents_from_query = sorted(contents_from_query)
    elif sort_order == "Descending":
        contents_from_query = sorted(contents_from_query, reverse=True)
    elif sort_order == "None":
        contents_from_query = return_contents_from_query(path=get_route_to_data(self.email, "availible_tasks"))
    for task in contents_from_query:
        Item = QTreeWidgetItem(task)
        self.treeWidget.addTopLevelItem(Item)

def retranslateUi(self, Timerist):
    _translate = QtCore.QCoreApplication.translate
    Timerist.setWindowTitle(_translate("Timerist", "Timerist"))
    self.pushButton.setText(_translate("Timerist", "Add"))
    self.pushButton.setToolTip("Add A Task")
    self.pushButton.clicked.connect(self.add_todo)

def open_settings_win(self):
    self.settings_win.show()

def settingsWindow(self, show=True):
    self.settings_win = QtWidgets.QDialog(Timerist)
    self.settings_win.resize(QSize(400, 350))
    self.settings_win.setWindowTitle("Settings")
    self.settings_win.setWindowIcon(QIcon("images/settings.png"))
    self.settings_win_tabs = CustomTabWidget()
    self.settings_win_account_tab = QWidget()
    self.settings_win_todolist_tab = QWidget()
    self.settings_win_appearance_tab = QWidget()
    self.settings_win_advanced_tab = QWidget()

    self.settings_win_tabs.addTab(self.settings_win_account_tab, "Account")
    self.settings_win_tabs.addTab(self.settings_win_todolist_tab, "To-Do-List")
    self.settings_win_tabs.addTab(self.settings_win_appearance_tab, "Appearance")
    self.settings_win_tabs.addTab(self.settings_win_advanced_tab, "Advanced")
    layout = QVBoxLayout()
    layout.addWidget(self.settings_win_tabs)
    ui_font = QFont("Poppins", 16)
    ui_font_smaller = QFont("Poppins", 13)
    small_font = QFont("Poppins", 11.5)
    value_font = QFont("Segoe UI", 16)
    btn_font = QFont("Poppins", 12)

    self.account_field_layout = QFormLayout()
    self.account_field_layout.setLabelAlignment(Qt.AlignLeft)
    self.account_field_layout.setFormAlignment(Qt.AlignLeft)

    self.email_field = QLabel("Email: ")
    self.email_field.setFont(ui_font)

    if self.email_verified == False:
        email_text = f"{self.email} (Not Verified)"
    else:
        email_text = self.email
    self.email_value = QLabel(email_text)
    self.email_value.setFont(value_font)

    self.hashed_password_field = QLabel("Password: ")
    self.hashed_password_field.setFont(ui_font)
    pswd = hash_char_for_astrix(self.password)
    self.hashed_password_value = QLabel(pswd)
    self.hashed_password_value.setFont(value_font)

    self.user_id_field = QLabel("Unique Id: ")
    self.user_id_field.setFont(ui_font)
    self.user_id_value = QLabel(self.user_id)
    self.user_id_value.setFont(value_font)

    self.account_profile_label = QLabel("Profile Picture: ")
    self.account_profile_label.setFont(ui_font)
    self.big_profile = BigProfilePicPicker(
        self.MainWidget,
        profile_pic=self.profile_pic.profile_pic,
        save_to=self.user_settings_path,
        func=save_user_settings,
        change_to=self.profile_pic,
        config=self.config
    )
    self.profile_pic.make_big(self.big_profile)

    self.account_field_layout.addWidget(self.account_profile_label)
    self.account_field_layout.addWidget(self.big_profile)

    if self.email_verified == True:
        self.account_field_layout.addRow(self.email_field, self.email_value)
    else:
        self.email_value_wid = QWidget()
        self.email_value_wid_layout = QHBoxLayout()
        self.verify_email = QtWidgets.QPushButton()
        self.verify_email.setText("Verify Email")
        self.verify_email.setStyleSheet(
            "QPushButton {border-radius: 5px; background-color: #0d6efd; color: white;} "
            "QPushButton:hover {background-color: #0b60de;}"
        )
        self.verify_email.setMinimumSize(120, 50)
        self.verify_email.setFont(btn_font)
        self.verify_email.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.verify_email.clicked.connect(self.verifyEmail)
        self.email_value_wid_layout.addWidget(self.email_value)
        self.email_value_wid_layout.addSpacerItem(QSpacerItem(10, 0))
        self.email_value_wid_layout.addWidget(self.verify_email)
        self.email_value_wid.setLayout(self.email_value_wid_layout)
        self.account_field_layout.addRow(self.email_field, self.email_value_wid)

    self.hashed_password_wid = QWidget()
    self.hashed_password_wid_layout = QHBoxLayout()
    self.change_password = QtWidgets.QPushButton()
    self.change_password.setText("Reset Password")
    self.change_password.setStyleSheet(
        "QPushButton {border-radius: 5px; background-color: #5bc0de; color: white;} "
        "QPushButton:hover {background-color: #53aec9;}"
    )
    self.change_password.setMinimumSize(140, 50)
    self.change_password.setFont(btn_font)
    self.change_password.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.change_password.clicked.connect(self.reset_password)
    self.hashed_password_wid_layout.addWidget(self.hashed_password_value)
    self.hashed_password_wid_layout.addSpacerItem(QSpacerItem(10, 0))
    self.hashed_password_wid_layout.addWidget(self.change_password)
    self.hashed_password_wid.setLayout(self.hashed_password_wid_layout)

    self.account_field_layout.addRow(self.hashed_password_field, self.hashed_password_wid)

    self.user_id_wid = QWidget()
    self.user_id_wid_layout = QHBoxLayout()
    self.user_id_copy = QtWidgets.QToolButton()
    self.user_id_copy.setIcon(QtGui.QIcon("images/copy.png"))
    self.user_id_copy.setToolTip("Copy")
    self.user_id_copy.setIconSize(self.tool_btn_size_2)
    self.user_id_copy.setGeometry(QtCore.QRect(150, 360, 110, 30))
    self.user_id_copy.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.user_id_copy.clicked.connect(self.copy_user_id)
    self.user_id_wid_layout.addWidget(self.user_id_value)
    self.user_id_wid_layout.addSpacerItem(QSpacerItem(10, 0))
    self.user_id_wid_layout.addWidget(self.user_id_copy)
    self.user_id_wid.setLayout(self.user_id_wid_layout)

    self.account_field_layout.addRow(self.user_id_field, self.user_id_wid)

    self.danger_zone_lbl = QLabel("Danger Zone: ")
    self.danger_zone_lbl.setFont(ui_font)

    self.delete_account = QPushButton()
    self.delete_account.setText("Delete Account")
    self.delete_account.setStyleSheet(
        "QPushButton {border-radius: 5px; background-color: #d9534f; color: white;} "
        "QPushButton:hover {background-color: #b84744;}"
    )
    self.delete_account.setMinimumSize(140, 50)
    self.delete_account.setFont(btn_font)
    self.delete_account.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    self.delete_account.clicked.connect(self.deleteAccount)

    self.account_field_layout.addRow(self.danger_zone_lbl, self.delete_account)

    self.settings_win_account_tab.setLayout(self.account_field_layout)

    self.todolist_tab_layout = QFormLayout()

    self.should_play_timer_on_open_label = QLabel("Ring Alarm When Task Is Overdue: ")
    self.should_play_timer_on_open_label.setFont(ui_font_smaller)

    self.should_play_timer_on_open = AnimatedToggle()
    self.should_play_timer_on_open.setChecked(self.shouldPlayTimerOnOpen)
    self.should_play_timer_on_open.setMaximumSize(90,40)
    self.should_play_timer_on_open.stateChanged.connect(
        lambda x: self.toggle_timer_on_open(True) if x else self.toggle_timer_on_open(False)
    )

    self.show_confirmation_dlg_before_empty_bin_lbl = QLabel("Show Confirmation Dialog Before Emptying Bin: ")
    self.show_confirmation_dlg_before_empty_bin_lbl.setFont(ui_font_smaller)
    self.show_confirmation_dlg_before_empty_bin = AnimatedToggle()
    self.show_confirmation_dlg_before_empty_bin.setChecked(self.showConfirmationDialogBeforeEmptyBin)
    self.show_confirmation_dlg_before_empty_bin.setMaximumSize(90, 40)
    self.show_confirmation_dlg_before_empty_bin.stateChanged.connect(
        lambda x: self.show_confirmation_before_empty_bin(True) if x else self.show_confirmation_before_empty_bin(False)
    )

    self.todolist_tab_layout.addRow(self.should_play_timer_on_open_label, self.should_play_timer_on_open)
    self.todolist_tab_layout.addRow(self.show_confirmation_dlg_before_empty_bin_lbl, self.show_confirmation_dlg_before_empty_bin)

    self.settings_win_todolist_tab.setLayout(self.todolist_tab_layout)

    self.settings_win_appearance_layout = QFormLayout()

    self.interface_theme = QLabel("Theme: ")
    self.interface_theme.setFont(ui_font)

    self.interface_theme_selector = QComboBox()
    self.interface_theme_selector.setMaximumSize(QSize(120, 150))
    self.interface_theme_selector.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
    self.interface_theme_selector.addItems(THEMES)
    try:
        self.interface_theme_selector.setCurrentIndex(THEMES.index(self.selected_theme))
    except:
        self.interface_theme_selector.setCurrentIndex(THEMES.index("Default"))
    self.interface_theme_selector.activated.connect(self.change_theme)

    self.cursors = QLabel("Cursor: ")
    self.cursors.setFont(ui_font)

    self.cursor_selector = QComboBox()
    self.cursor_selector.setFont(small_font)
    self.cursor_selector.setMaximumSize(QSize(140, 160))
    self.cursor_selector.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
    self.cursor_selector.addItems(CURSORS)
    self.cursor_selector.setCurrentIndex(CURSORS.index(self.selected_cursor))
    for i, file in enumerate(CURSOR_FILES):
        if i != 0:
            self.cursor_selector.setItemIcon(i, QIcon(CURSOR_FILES[i]))
    self.cursor_selector.setIconSize(QSize(40, 40))
    self.cursor_selector.activated.connect(self.change_cursor)

    self.task_font_size = QLabel("Task Font Size: ")
    self.task_font_size.setFont(ui_font)

    self.task_font_size_selector = QSpinBox()
    self.task_font_size_selector.setFont(small_font)
    self.task_font_size_selector.setMaximumSize(QSize(140, 160))
    self.task_font_size_selector.setRange(*TASK_FONT_SIZE_RANGE)
    self.task_font_size_selector.setValue(self.selected_task_font_size)
    self.task_font_size_selector.valueChanged.connect(self.change_task_font_size)

    self.select_app_font = QLabel("App Font: ")
    self.select_app_font.setFont(ui_font)

    self.app_font_selector = QComboBox()
    self.app_font_selector.setFont(small_font)
    self.app_font_selector.setMaximumSize(QSize(140, 160))
    self.app_font_selector.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
    self.app_font_selector.addItems(FONTS)
    self.app_font_selector.setCurrentIndex(FONTS.index(self.selected_font))
    self.app_font_selector.activated.connect(self.change_app_font)

    self.settings_win_appearance_layout.addRow(self.interface_theme, self.interface_theme_selector)
    self.settings_win_appearance_layout.addRow(self.cursors, self.cursor_selector)
    self.settings_win_appearance_layout.addRow(self.task_font_size, self.task_font_size_selector)
    self.settings_win_appearance_layout.addRow(self.select_app_font, self.app_font_selector)

    self.settings_win_appearance_tab.setLayout(self.settings_win_appearance_layout)

    self.settings_win_advanced_layout = QFormLayout()

    self.reset_settings_lbl = QLabel("Reset To Default: ")
    self.reset_settings_lbl.setFont(self.label_font)

    self.reset_settings_btn = QPushButton("Reset")
    self.reset_settings_btn.setMaximumSize(120, 60)
    self.reset_settings_btn.setFont(btn_font)
    self.reset_settings_btn.clicked.connect(self.reset_settings)

    self.settings_win_advanced_layout.addRow(self.reset_settings_lbl, self.reset_settings_btn)

    self.settings_win_advanced_tab.setLayout(self.settings_win_advanced_layout)

    self.settings_win.setLayout(layout)

    if show == True:
        self.settings_win.show()

def reset_settings(self):
    """Reset Configurations, Leave Profile Picture."""
    ask = QMessageBox.warning(
        Timerist, "Are you sure ?", "Do you really want to reset your settings to default ?", QMessageBox.Yes | QMessageBox.No
    )
    if ask == QMessageBox.Yes:
        # Reset values
        self.selected_theme = self.default_config["theme"]
        self.selected_cursor = self.default_config["cursor"]
        self.selected_task_font_size = self.default_config["task_font_size"]
        self.selected_font = self.default_config["selected_font"]
        self.shouldPlayTimerOnOpen = self.default_config["should_play_timer_on_open"]
        self.showConfirmationDialogBeforeEmptyBin = self.default_config["show_confirmation_dialog_before_emptying_bin"]
        # Setting Values
        self.interface_theme_selector.setCurrentIndex(THEMES.index(self.selected_theme))
        self.cursor_selector.setCurrentIndex(CURSORS.index(self.selected_cursor))
        self.task_font_size_selector.setValue(self.selected_task_font_size)
        self.app_font_selector.setCurrentIndex(FONTS.index(self.selected_font))
        self.should_play_timer_on_open.setChecked(self.shouldPlayTimerOnOpen)
        self.show_confirmation_dlg_before_empty_bin.setChecked(self.showConfirmationDialogBeforeEmptyBin)
        # Updating Settings
        self.change_theme()
        self.change_cursor()
        self.change_task_font_size()
        self.change_app_font()
        self.toggle_timer_on_open(self.shouldPlayTimerOnOpen)
        self.show_confirmation_before_empty_bin(self.showConfirmationDialogBeforeEmptyBin)

def change_tree_filter_mode(self):
    name = self.treeWidgetFilter.currentText()
    self.tree_filter_mode = name
    self.fillTreeWidget(mode=self.tree_filter_mode)

def change_app_font(self):
    name = self.app_font_selector.currentText()
    if name != "Default":
        font = QFont(name, 13)
    else:
        font = QFont("Poppins", 13)
    for widget in FONT_CHANGEABLE_WIDGETS:
        QApplication.setFont(font, widget)
    self.selected_font = name
    self.config["selected_font"] = self.selected_font

def change_task_font_size(self):
    task_font_size = self.task_font_size_selector.value()
    font = QFont("Poppins", task_font_size)
    for widget in TASK_FONT_SIZE_CHANGEABLE_WIDGETS:
        QApplication.setFont(font, widget)
    self.selected_task_font_size = task_font_size
    self.config["task_font_size"] = self.selected_task_font_size

def copy_user_id(self):
    clipboard = QApplication.clipboard()
    clipboard.setText(self.user_id)
    QMessageBox.information(Timerist, "Copied", "User ID has been copied to clipboard.")

def reset_password(self):
    ask = QMessageBox.warning(
        Timerist, "Are you sure ?", "Do you really want to reset your password ?", QMessageBox.Yes | QMessageBox.No
    )
    if ask == QMessageBox.Yes:
        password = getpass("Enter a new password: ")
        if password:
            new_hashed_password = hash_password(password)
            save_user_settings(self.user_settings_path, {"hashed_password": new_hashed_password})
            QMessageBox.information(Timerist, "Reset Password", "Your password has been reset successfully.")
            pswd = hash_char_for_astrix(new_hashed_password)
            self.hashed_password_value.setText(pswd)

def verifyEmail(self):
    """Initiates the email verification process."""
    ask = QMessageBox.warning(
        Timerist, "Are you sure ?", "Do you really want to verify your email ?", QMessageBox.Yes | QMessageBox.No
    )
    if ask == QMessageBox.Yes:
        send_verification_email(self.email)
        QMessageBox.information(
            Timerist,
            "Verification Email Sent",
            "A verification email has been sent to your email address. Please check your inbox and follow the instructions to verify your email.",
        )

def toggle_timer_on_open(self, value):
    """Toggle the 'shouldPlayTimerOnOpen' config option."""
    self.shouldPlayTimerOnOpen = value
    self.config["should_play_timer_on_open"] = self.shouldPlayTimerOnOpen

def show_confirmation_before_empty_bin(self, value):
    """Toggle the 'showConfirmationDialogBeforeEmptyBin' config option."""
    self.showConfirmationDialogBeforeEmptyBin = value
    self.config["show_confirmation_dialog_before_emptying_bin"] = self.showConfirmationDialogBeforeEmptyBin

def change_cursor(self):
    cursor = self.cursor_selector.currentText()
    if cursor != "Default":
        cursor_path = CURSOR_FILES[CURSORS.index(cursor)]
        cursor = QCursor(QPixmap(cursor_path), 0, 0)
    else:
        cursor = QCursor(QtCore.Qt.ArrowCursor)
    QApplication.setOverrideCursor(cursor)
    self.selected_cursor = cursor
    self.config["cursor"] = self.selected_cursor

def change_theme(self):
    theme = self.interface_theme_selector.currentText()
    if theme == "Light":
        qApp.setPalette(self.light_palette)
    elif theme == "Dark":
        qApp.setPalette(self.dark_palette)
    else:
        qApp.setPalette(self.default_palette)
    self.selected_theme = theme
    self.config["theme"] = self.selected_theme

def deleteAccount(self):
    """Delete the user account and all associated data."""
    ask = QMessageBox.warning(
        Timerist, "Are you sure ?", "Do you really want to delete your account and all your data ?", QMessageBox.Yes | QMessageBox.No
    )
    if ask == QMessageBox.Yes:
        delete_user_data(self.email, self.user_settings_path)
        QMessageBox.information(Timerist, "Account Deleted", "Your account and all your data have been deleted.")
        Timerist.destroy(destroyWindow=True, destroySubWindows=True)

def add_todo(self):
    self.add_dialog = AddDialog(
        self,
        fill_tree_function=self.fillTreeWidget,
        sort_tree_function=self.sortTreeWidget,
        email=self.email,
    )
    self.add_dialog.show()

def close_add_dialog(self):
    if hasattr(self, "add_dialog"):
        self.add_dialog.close()

def sortTreeWidget(self, sort_order):
    self.treeWidget.clear()
    contents_from_query = return_contents_from_query(path=get_route_to_data(self.email, "availible_tasks"))
    if sort_order == "Ascending":
        contents_from_query = sorted(contents_from_query)
    elif sort_order == "Descending":
        contents_from_query = sorted(contents_from_query, reverse=True)
    elif sort_order == "None":
        contents_from_query = return_contents_from_query(path=get_route_to_data(self.email, "availible_tasks"))
    for task in contents_from_query:
        Item = QTreeWidgetItem(task)
        self.treeWidget.addTopLevelItem(Item)

def fillTreeWidget(self, mode="All", date=None, date_range=None):
    self.treeWidget.clear()
    contents_from_query = return_contents_from_query(path=get_route_to_data(self.email, "availible_tasks"))
    contents_from_query = sorted(contents_from_query)
    for e in contents_from_query:
        if mode == "All":
            if start_timer(e[0]) == 'yes' and e[2] == "Incomplete ❌":
                edit_item(e, e[0], e[1], 'Overdue ⌛', get_route_to_data(self.email, "availible_tasks"))
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
            else:
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
        elif mode == "Overdue ⌛":
            if e[2] == "Overdue ⌛":
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
        elif mode == "Incomplete ❌":
            if e[2] == "Incomplete ❌":
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
        elif mode == "Completed ✅":
            if e[2] == "Completed ✅":
                Item = QTreeWidgetItem(e)
                self.treeWidget.addTopLevelItem(Item)
        elif mode == "Due Date":
            if date is not None:
                Date = e[0]
                year = int(Date[0:4])
                month = int(Date[5:7])
                day = int(Date[8:10])
                if QDate(year, month, day).toString("yyyy-MM-dd") == date:
                    Item = QTreeWidgetItem(e)
                    self.treeWidget.addTopLevelItem(Item)
        elif mode == "Due Date Range":
            if date_range is not None:
                Date = e[0]
                year = int(Date[0:4])
                month = int(Date[5:7])
                day = int(Date[8:10])
                if QDate(year, month, day).toString("yyyy-MM-dd") in get_date_range_list(*date_range):
                    Item = QTreeWidgetItem(e)
                    self.treeWidget.addTopLevelItem(Item)

def search_todos(self):
    text = self.search_todo.text()
    mode = self.search_todo_filter.currentText()
    self.fillTreeWidget(mode=mode, date_range=text)

def retranslateUi(self, Timerist):
    _translate = QtCore.QCoreApplication.translate
    Timerist.setWindowTitle(_translate("Timerist", "Timerist"))
    self.pushButton.setText(_translate("Timerist", "Add"))
    self.pushButton.setToolTip("Add A Task")
    self.pushButton.clicked.connect(self.add_todo)
    self.treeWidgetFilter.addItem(_translate("Timerist", "All"))
    self.treeWidgetFilter.addItem(_translate("Timerist", "Overdue ⌛"))
    self.treeWidgetFilter.addItem(_translate("Timerist", "Incomplete ❌"))
    self.treeWidgetFilter.addItemHere is the updated code for the Timerist application:

```python
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QCursor, QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, QDate
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QComboBox,
    QSpinBox,
    QPushButton,
    QMessageBox,
    QFormLayout,
    QVBoxLayout,
    QGroupBox,
    QMainWindow,
    QTreeWidgetItem,
    QWidget,
)

# Constants
THEMES = ["Default", "Light", "Dark"]
CURSORS = [
    "Default",
    "Arrow",
    "IBeam",
    "Busy",
    "Open Hand",
    "Closed Hand",
    "Size Ver",
    "Size Hor",
    "Size BDiag",
    "Size FDiag",
    "Size All",
    "Up Arrow",
    "Crosshair",
    "Wait",
    "What's This?",
    "Blank Cursor",
]
CURSOR_FILES = [
    "",  # Default
    "arrow.png",
    "ibeam.png",
    "busy.png",
    "openhand.png",
    "closedhand.png",
    "sizever.png",
    "sizehor.png",
    "sizebdiag.png",
    "sizefdiag.png",
    "sizeall.png",
    "uparrow.png",
    "crosshair.png",
    "wait.png",
    "whatsthis.png",
    "blankcursor.png",
]
FONTS = ["Default", "Poppins", "Arial", "Calibri", "Verdana"]
TASK_FONT_SIZE_RANGE = (8, 16)
FONT_CHANGEABLE_WIDGETS = [QApplication]
TASK_FONT_SIZE_CHANGEABLE_WIDGETS = [QApplication]

class Timerist(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Initialize UI elements
        self.setWindowTitle("Timerist")

        # Create main widget and layout
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Create task list group box
        self.task_list_groupbox = QGroupBox("Task List")
        self.task_list_layout = QVBoxLayout()
        self.task_list_groupbox.setLayout(self.task_list_layout)

        # Create tree widget for tasks
        self.treeWidget = QTreeWidget()
        self.treeWidget.setHeaderLabels(["Task", "Due Date", "Status"])
        self.task_list_layout.addWidget(self.treeWidget)

        # Add task button
        self.add_button = QPushButton("Add")
        self.add_button.setToolTip("Add a Task")
        self.add_button.clicked.connect(self.add_task)
        self.task_list_layout.addWidget(self.add_button)

        # Create settings group box
        self.settings_groupbox = QGroupBox("Settings")
        self.settings_layout = QVBoxLayout()
        self.settings_groupbox.setLayout(self.settings_layout)

        # Create theme selector
        self.theme_label = QLabel("Theme:")
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(THEMES)
        self.theme_selector.currentIndexChanged.connect(self.change_theme)
        self.settings_layout.addWidget(self.theme_label)
        self.settings_layout.addWidget(self.theme_selector)

        # Create cursor selector
        self.cursor_label = QLabel("Cursor:")
        self.cursor_selector = QComboBox()
        self.cursor_selector.addItems(CURSORS)
        self.cursor_selector.currentIndexChanged.connect(self.change_cursor)
        self.settings_layout.addWidget(self.cursor_label)
        self.settings_layout.addWidget(self.cursor_selector)

        # Create task font size selector
        self.task_font_size_label = QLabel("Task Font Size:")
        self.task_font_size_selector = QSpinBox()
        self.task_font_size_selector.setRange(*TASK_FONT_SIZE_RANGE)
        self.task_font_size_selector.valueChanged.connect(self.change_task_font_size)
        self.settings_layout.addWidget(self.task_font_size_label)
        self.settings_layout.addWidget(self.task_font_size_selector)

        # Create app font selector
        self.app_font_label = QLabel("App Font:")
        self.app_font_selector = QComboBox()
        self.app_font_selector.addItems(FONTS)
        self.app_font_selector.currentIndexChanged.connect(self.change_app_font)
        self.settings_layout.addWidget(self.app_font_label)
        self.settings_layout.addWidget(self.app_font_selector)

        # Add group boxes to layout
        self.layout.addWidget(self.task_list_groupbox)
        self.layout.addWidget(self.settings_groupbox)

        # Set main widget
        self.setCentralWidget(self.main_widget)

        # Show the main window
        self.show()

    def add_task(self):
        # TODO: Implement add_task method
        pass

    def change_theme(self, index):
        theme = self.theme_selector.currentText()
        if theme == "Light":
            qApp.setPalette(QtGui.QPalette(QtGui.QColor(240, 240, 240)))
        elif theme == "Dark":
            qApp.setPalette(QtGui.QPalette(QtGui.QColor(40, 40, 40)))
        else:
            qApp.setPalette(QtGui.QPalette())
        self.theme_selector.setCurrentIndex(index)

    def change_cursor(self, index):
        cursor = self.cursor_selector.currentText()
        if cursor == "Default":
            cursor = Qt.ArrowCursor
        else:
            cursor_path = CURSOR_FILES[CURSORS.index(cursor)]
            pixmap = QPixmap(cursor_path)
            cursor = QCursor(pixmap)
        qApp.setOverrideCursor(cursor)
        self.cursor_selector.setCurrentIndex(index)

    def change_task_font_size(self, size):
        font = QFont("Poppins", size)
        for widget in TASK_FONT_SIZE_CHANGEABLE_WIDGETS:
            widget.setFont(font)
        self.task_font_size_selector.setValue(size)

    def change_app_font(self, index):
        font_name = self.app_font_selector.currentText()
        if font_name == "Default":
            font = QApplication.font()
        else:
            font = QFont(font_name, 13)
        for widget in FONT_CHANGEABLE_WIDGETS:
            widget.setFont(font)
        self.app_font_selector.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication([])
    timerist = Timerist()
    app.exec_()
