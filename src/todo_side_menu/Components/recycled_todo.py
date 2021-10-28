from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from typing import List

class RecycledTodo(QtWidgets.QFrame):
    """Represents an Recycled Todo in the User Interface."""
    def __init__(self, parent, todo_data: List[str]):
        self.Parent = parent
        self.todo_data = todo_data
        self.main_layout2 = QtWidgets.QFormLayout()
        super().__init__(parent=parent)
        self.isSelected = False
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.RenderUI2()

    def selectionEnabled(self):
        """Add the todo to the selection Automatically."""
        if self in self.Parent.selectedTodos:
            return
        self.isSelected = True
        self.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0080ff;}")
        self.Parent.selectedTodos.append(self)
        selection_count = self.Parent.getSelectedTodosCount()
        self.Parent.selected_count.setText(f"Selected: {selection_count}")

    def mousePressEvent(self, event):
        """Add the todo to the selection On Click."""
        if self in self.Parent.selectedTodos:
            return
        self.isSelected = True
        self.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0080ff;}")
        self.Parent.selectedTodos.append(self)
        selection_count = self.Parent.getSelectedTodosCount()
        self.Parent.selected_count.setText(f"Selected: {selection_count}")


    def Unselect(self):
        """Remove the todo from the selection"""
        self.isSelected = False
        self.setStyleSheet("QFrame {border-width: 2;border-radius: 4;border-style: solid;border-color: #0d0e0f;}")
        self.Parent.selectedTodos.remove(self)
        selection_count = self.Parent.getSelectedTodosCount()
        self.Parent.selected_count.setText(f"Selected: {selection_count}")

    def __repr__(self):
        return f"todo_name: {self.todo_data[1]} - todo_date_to_complete : {self.todo_data[0]} -  todo_status: {self.todo_data[2]}"


    def contextMenuEvent(self, event):
        """Context Menu For Recycled Todos"""
        contextMenu = QMenu(self)
        contextMenu.setStyleSheet("""QMenu { 
                           background-color: black; 
                           color: white; 
                           border: black solid 1px
                           }""")

        # checks if it is selected
        if self.isSelected == True:
            unselect = contextMenu.addAction("Unselect")
            action = contextMenu.exec_(self.mapToGlobal(event.pos()))
            if action == unselect:
                self.Unselect()


    def RenderUI2(self):
        self.std_font = QFont()
        self.std_font.setPointSizeF(13.5)
        self.todo_name = QtWidgets.QLabel(self.todo_data[1])
        self.todo_name.setFont(self.std_font)
        self.todo_name.setStyleSheet("color: #fff; background-color: #3b4242;")
        self.todo_date_created = QtWidgets.QLabel(self.todo_data[0])
        self.todo_date_created.setFont(self.std_font)
        self.todo_date_created.setStyleSheet("color: #fff; background-color: #3b4242;")
        self.todo_status = QtWidgets.QLabel(self.todo_data[2])
        self.todo_status.setFont(self.std_font)
        self.todo_status.setStyleSheet("color: #fff; background-color: #3b4242;")
        lbl1 = QLabel("Name: ")
        lbl1.setFont(self.std_font)
        lbl1.setStyleSheet("color: #000; background-color: #DDD9D9;")
        lbl2 = QLabel("Due Date: ")
        lbl2.setFont(self.std_font)
        lbl2.setStyleSheet("color: #000; background-color: #DDD9D9;")
        lbl3 = QLabel("Status: ")
        lbl3.setFont(self.std_font)
        lbl3.setStyleSheet("color: #000; background-color: #DDD9D9;")
        self.main_layout2.addRow(lbl1, self.todo_name)
        self.main_layout2.addRow(lbl2, self.todo_date_created)
        self.main_layout2.addRow(lbl3, self.todo_status)
        self.setLayout(self.main_layout2)
