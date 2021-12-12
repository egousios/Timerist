from PyQt5 import QtWidgets
from PyQt5.QtCore import QParallelAnimationGroup, QSize, Qt
from PyQt5.QtGui import QBrush, QFont, QIcon, QKeySequence, QPalette, QPixmap, QWindow
from PyQt5.QtWidgets import *
from typing import List, Optional
from backend.query import Tree, delete_item_from_query, is_item, return_contents_from_query, is_item
from todo_side_menu.Components.recycled_todo import RecycledTodo


class RecycleBin(QtWidgets.QWidget):
    """Recycled Todos Will be Managed Here."""
    def __init__(self, parent, data_source, todo_data: List[List[str]], email, maker, manager, showConfirmationBeforeEmpty):
        self.Parent = parent
        self.data_source = data_source # Keeps the source of the data for restoration later.
        self.todo_data = todo_data # List of Recycled todos.
        self.email = email
        self.maker = maker
        self.manager = manager
        self.showConfirmationBeforeEmpty = showConfirmationBeforeEmpty
        self.selectedTodos = []
        self.todos = []
        self.main_layout = QtWidgets.QVBoxLayout()
        self.menu_layout = QHBoxLayout()
        self.Layout = QVBoxLayout()
        super().__init__(parent=parent)
        self.RenderUI()

    def contextMenuEvent(self, event):
        """Context Menu For Recycled Todos."""
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

        self.delete_btn = QtWidgets.QPushButton()
        self.delete_btn.setText("Delete")
        self.delete_btn.setMinimumSize(QSize(90, 40))
        self.delete_btn.setFont(self.btn_font)
        self.delete_btn.setToolTip("Delete A Todo")
        self.delete_btn.setStyleSheet("""QToolTip {background-color: black; 
                        color: white; 
                        border: black solid 1px} QToolButton {text-align: right}""")
        self.delete_btn.setIcon(QIcon("images/tool.png"))
        self.delete_btn.clicked.connect(self.delete_todo)

        self.restore_btn = QtWidgets.QPushButton()
        self.restore_btn.setText("Restore")
        self.restore_btn.setMinimumSize(QSize(90, 40))
        self.restore_btn.setFont(self.btn_font)
        self.restore_btn.setToolTip("Restore A Todo")
        self.restore_btn.setStyleSheet("""QToolTip {background-color: black; 
                        color: white; 
                        border: black solid 1px} QToolButton {text-align: right}""")
        self.restore_btn.setIcon(QIcon("images/tool.png"))
        self.restore_btn.clicked.connect(self.restore_todo)

        self.empty_btn = QtWidgets.QPushButton()
        self.empty_btn.setText("Empty")
        self.empty_btn.setMinimumSize(QSize(90, 40))
        self.empty_btn.setFont(self.btn_font)
        self.empty_btn.setToolTip("Empty the Bin")
        self.empty_btn.setStyleSheet("""QToolTip {background-color: black; 
                        color: white; 
                        border: black solid 1px} QToolButton {text-align: right}""")
        self.empty_btn.setIcon(QIcon("images/tool.png"))
        self.empty_btn.clicked.connect(self.empty_bin)

        self.menu_layout.addWidget(self.actions_label, alignment=Qt.AlignTop)
        self.menu_layout.addWidget(self.restore_btn, alignment=Qt.AlignTop)
        self.menu_layout.addSpacerItem(QSpacerItem(5, 0))
        self.menu_layout.addWidget(self.delete_btn, alignment=Qt.AlignTop)
        self.menu_layout.addSpacerItem(QSpacerItem(5, 0))
        self.menu_layout.addWidget(self.empty_btn, alignment=Qt.AlignTop)
        self.menu_layout.addStretch(4)
        self.menu_layout.addWidget(self.selected_count, alignment=Qt.AlignTop)
        self.menu_layout.addStretch()

        for todo in self.todo_data:
            todo_object = RecycledTodo(self, todo)
            todo_object.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0d0e0f;}")
            self.todos.append(todo_object)
            self.main_layout.addWidget(todo_object)
        self.Layout.addLayout(self.menu_layout)
        self.Layout.addSpacerItem(QSpacerItem(10, 0))
        self.Layout.addLayout(self.main_layout)
        self.setLayout(self.Layout)

    def delete_todo(self):
        for todo in self.selectedTodos:
            data = [todo.todo_data[0], todo.todo_data[1], todo.todo_data[2]]
            items = []
            for i in reversed(range(self.main_layout.count())): 
                item = self.main_layout.itemAt(i)
                items.append(item)
            for item in items:
                wid = item.widget()
                if isinstance(wid, RecycledTodo):
                    if wid.todo_data == todo.todo_data:
                        wid.setParent(None)
            self.selectedTodos.remove(todo)
            self.todos.remove(todo)
            selection_amount = self.getSelectedTodosCount()
            self.selected_count.setText(f"Selected: {selection_amount}")
            delete_item_from_query(data, f"users/{self.email}/recycled.txt")

    def restore_todo(self):
        for todo in self.selectedTodos:
            if is_item(todo.todo_data, f"users/{self.email}/data.txt"):
                QMessageBox.critical(self, "Error", "Couldn't Restore todo because todo is already restored.")
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
                    if isinstance(wid, RecycledTodo):
                        if wid.todo_data == todo.todo_data:
                            wid.setParent(None)
                self.selectedTodos.remove(todo)
                self.todos.remove(todo)
                selection_amount = self.getSelectedTodosCount()
                self.selected_count.setText(f"Selected: {selection_amount}")
                delete_item_from_query(data, f"users/{self.email}/recycled.txt")
        self.manager.Refresh()

    def empty_bin(self):
        if self.manager.showConfirmationDialogBeforeEmptyBin == True:
            ask = QtWidgets.QMessageBox.question(self, "Are you sure ?", "Are you sure that you want to permenantly delete all of your todos ?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            if ask == QtWidgets.QMessageBox.Yes:
                for todo in self.todos:
                    data = [todo.todo_data[0], todo.todo_data[1], todo.todo_data[2]]
                    items = []
                    for i in reversed(range(self.main_layout.count())): 
                        item = self.main_layout.itemAt(i)
                        items.append(item)
                    for item in items:
                        wid = item.widget()
                        if isinstance(wid, RecycledTodo):
                            if wid.todo_data == todo.todo_data:
                                wid.setParent(None)
                    self.todos.remove(todo)
                    delete_item_from_query(data, f"users/{self.email}/recycled.txt")
        else:
            for todo in self.todos:
                data = [todo.todo_data[0], todo.todo_data[1], todo.todo_data[2]]
                items = []
                for i in reversed(range(self.main_layout.count())): 
                    item = self.main_layout.itemAt(i)
                    items.append(item)
                for item in items:
                    wid = item.widget()
                    if isinstance(wid, RecycledTodo):
                        if wid.todo_data == todo.todo_data:
                            wid.setParent(None)
                self.todos.remove(todo)
                delete_item_from_query(data, f"users/{self.email}/recycled.txt")
