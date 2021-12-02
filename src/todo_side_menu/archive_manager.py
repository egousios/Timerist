from PyQt5 import QtWidgets, sip
from PyQt5.QtCore import QParallelAnimationGroup, QSize, Qt
from PyQt5.QtGui import QBrush, QFont, QIcon, QKeySequence, QPalette, QPixmap
from PyQt5.QtWidgets import *
from typing import List, Optional
from backend.query import Tree, delete_item_from_query, is_item, return_contents_from_query, is_item
from todo_side_menu.Components.recycled_todo import RecycledTodo
from .Components.archived_todo import ArchivedTodo
import time

class ArchiveManager(QtWidgets.QWidget):
    """Archived Todos Will be Managed Here."""
    def __init__(self, parent, data_source, todo_data: List[List[str]], email, maker, manager):
        self.Parent = parent
        self.data_source = data_source # Keeps the source of the data for restoration later.
        self.todo_data = todo_data # List of Archived todos.
        self.email = email
        self.maker = maker
        self.manager = manager
        self.selectedTodos = []
        self.todos = []
        self.main_layout = QtWidgets.QVBoxLayout()
        self.menu_layout = QHBoxLayout()
        self.Layout = QVBoxLayout()
        super().__init__(parent=parent)
        self.RenderUI()

    def contextMenuEvent(self, event):
        """Context Menu For Archived Todos."""
        contextMenu = QMenu(self)
        contextMenu.setStyleSheet("""QMenu { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")


        select_all = contextMenu.addAction("Select All")
        unselect_all = contextMenu.addAction("Unselect All")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == select_all:
            self.selectAll()
        if action == unselect_all:
            self.unselectAll()

    def selectAll(self):
        for todo in self.todos:
            todo.selectionEnabled()

    def unselectAll(self):
        for todo in self.todos:
            if todo in self.selectedTodos:
                todo.Unselect()





    def getSelectedTodosCount(self):
        """Returns the amount of todos that are selected."""
        return len(self.selectedTodos)

    def RenderUI(self):
        # Ui Font(s)
        self.std_font = QFont()
        self.std_font.setPointSizeF(15.5)

        self.btn_font = QFont()
        self.btn_font.setPointSize(13.5)

        selection_amount = self.getSelectedTodosCount()
        self.selected_count = QtWidgets.QLabel(f"Selected: {selection_amount}")
        self.selected_count.setFont(self.std_font)

        self.actions_label = QtWidgets.QLabel("Actions: ")
        self.actions_label.setFont(self.std_font)

        self.unarchive_btn = QtWidgets.QPushButton()
        self.unarchive_btn.setText("Unarchive")
        self.unarchive_btn.setMinimumSize(QSize(125, 40))
        self.unarchive_btn.setFont(self.btn_font)
        self.unarchive_btn.setToolTip("Unarchive A Todo")
        self.unarchive_btn.setStyleSheet("""QToolTip {background-color: black; 
                        color: white; 
                        border: black solid 1px} QToolButton {text-align: right}""")
        #self.unarchive_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.unarchive_btn.setIcon(QIcon("images/tool.png"))
        self.unarchive_btn.clicked.connect(self.unarchive_todo)

        self.recycle_btn = QtWidgets.QPushButton()
        self.recycle_btn.setText("Recycle")
        self.recycle_btn.setMinimumSize(QSize(110, 40))
        self.recycle_btn.setFont(self.btn_font)
        self.recycle_btn.setToolTip("Recycle A Todo")
        self.recycle_btn.setStyleSheet("""QToolTip {background-color: black; 
                        color: white; 
                        border: black solid 1px} QToolButton {text-align: right}""")
        #self.recycle_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.recycle_btn.setIcon(QIcon("images/tool.png"))
        self.recycle_btn.clicked.connect(self.recycle_todo)

        self.menu_layout.addWidget(self.actions_label, alignment=Qt.AlignTop)
        self.menu_layout.addWidget(self.unarchive_btn, alignment=Qt.AlignTop)
        self.menu_layout.addSpacerItem(QSpacerItem(5, 0))
        self.menu_layout.addWidget(self.recycle_btn, alignment=Qt.AlignTop)
        self.menu_layout.addStretch(3)
        self.menu_layout.addWidget(self.selected_count, alignment=Qt.AlignTop)
        self.menu_layout.addStretch()

        for todo in self.todo_data:
            todo_object = ArchivedTodo(self, todo)
            todo_object.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0d0e0f;}")
            self.todos.append(todo_object)
            self.main_layout.addWidget(todo_object)
        self.Layout.addLayout(self.menu_layout)
        self.Layout.addSpacerItem(QSpacerItem(10, 0))
        self.Layout.addLayout(self.main_layout)
        self.setLayout(self.Layout)

    def unarchive_todo(self):
        for todo in self.selectedTodos:
            if is_item(todo.todo_data, f"users/{self.email}/data.txt"):
                QMessageBox.critical(self, "Error", "Couldn't Unarchive todo because todo is already unarchived.")
            else:
                data = [todo.todo_data[0], todo.todo_data[1], todo.todo_data[2]]
                branch = Tree(branches={
                        "end_time":data[0],
                        "task":data[1],
                        "status":data[2],
                    })
                branch.save(branch.branches, id="all", path=f"users/{self.email}/data.txt")
                items = []
                for i in reversed(range(self.main_layout.count())): 
                    item = self.main_layout.itemAt(i)
                    items.append(item)
                for item in items:
                    wid = item.widget()
                    if isinstance(wid, ArchivedTodo):
                        if wid.todo_data == todo.todo_data:
                            wid.setParent(None)
                self.selectedTodos.remove(todo)
                self.todos.remove(todo)
                selection_amount = self.getSelectedTodosCount()
                self.selected_count.setText(f"Selected: {selection_amount}")
                delete_item_from_query(data, f"users/{self.email}/archived.txt")
        self.manager.Refresh(self.manager.tree_filter_mode)

    def recycle_todo(self):
        for todo in self.selectedTodos:
            if is_item(todo.todo_data, f"users/{self.email}/recycled.txt"):
                QMessageBox.critical(self, "Error", "Couldn't Recycle todo because todo is already recycled.")
            else:
                data = [todo.todo_data[0], todo.todo_data[1], todo.todo_data[2]]
                branch = Tree(branches={
                        "end_time":data[0],
                        "task":data[1],
                        "status":data[2],
                    })
                branch.save(branch.branches, id="all", path=f"users/{self.email}/recycled.txt")
                items = []
                for i in reversed(range(self.main_layout.count())): 
                    item = self.main_layout.itemAt(i)
                    items.append(item)
                for item in items:
                    wid = item.widget()
                    if isinstance(wid, ArchivedTodo):
                        if wid.todo_data == todo.todo_data:
                            wid.setParent(None)
                self.selectedTodos.remove(todo)
                self.todos.remove(todo)
                selection_amount = self.getSelectedTodosCount()
                self.selected_count.setText(f"Selected: {selection_amount}")
                delete_item_from_query(data, f"users/{self.email}/archived.txt")
                todo_object = RecycledTodo(self.manager.RecycledTodos, data)
                todo_object.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0d0e0f;}")
                self.manager.RecycledTodos.todos.append(todo_object)
                self.manager.RecycledTodos.main_layout.addWidget(todo_object)

            
