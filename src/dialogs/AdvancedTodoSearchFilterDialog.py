from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QDateEdit, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget

# Constants
MAXIMUM_TIME_INPUT = 10000

class AdvancedTodoSearchFilterDialog(QtWidgets.QDialog):
    """A dialog window for searching through tasks with advanced filters."""
    def __init__(self, parent, fill_tree_function):
        super().__init__(parent=parent)
        self.fill_tree_function = fill_tree_function
        self.setWindowTitle("Advanced Filter...")
        self.window_layout = QVBoxLayout()
        self.group_box = QGroupBox()
        self.form_layout = QFormLayout()
        self.label_font = QFont("Poppins", 15)

        self.button_box = QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.filter_tasks)
        self.button_box.rejected.connect(self.close_win)

        self.filters = ["None", "Due Date"]
        self.selected_filter = self.filters[0] # None

        self.filter_by_lbl = QLabel("Filter By: ")
        self.filter_by_lbl.setFont(self.label_font)

        self.filter_by = QComboBox()
        self.filter_by.setCurrentIndex(self.filters.index(self.selected_filter)) # current filter
        for filter in self.filters:
            self.filter_by.addItem(filter)
        self.filter_by.activated.connect(self.renderConfigurations)

        self.form_layout.addRow(self.filter_by_lbl, self.filter_by)

        self.due_date_label = QLabel("Matching Due Date: ")
        self.due_date_label.setFont(self.label_font)

        self.due_date_picker = QDateEdit()
        current_date = QtCore.QDate.currentDate()
        self.due_date_picker.setDate(current_date)

        self.due_date_label.setHidden(True) 
        self.due_date_picker.setHidden(True)

        self.form_layout.addRow(self.due_date_label, self.due_date_picker)

        self.group_box.setLayout(self.form_layout)

        self.window_layout.addWidget(self.group_box)
        self.window_layout.addWidget(self.button_box, QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.window_layout)

        self.resize(350, 250)

    def close_win(self):
        self.destroy(True)

    def filter_tasks(self):
        if self.selected_filter == "Due Date":
            date = self.due_date_picker.date().toString("yyyy-MM-dd")
            self.fill_tree_function(mode=self.selected_filter, date=date)


    def renderConfigurations(self):
        """Show the rest of the options based on the selected filter."""
        text = self.filter_by.currentText()
        if text == "None":
            self.due_date_label.setHidden(True) 
            self.due_date_picker.setHidden(True)
        elif text == "Due Date":
            # Find tasks that match the specific due date.
            self.due_date_label.setHidden(False) 
            self.due_date_picker.setHidden(False)
            self.selected_filter = text


