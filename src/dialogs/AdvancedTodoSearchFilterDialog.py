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

        self.filters = ["None", "Due Date", "Time Till Overdue"]
        self.match_types = ["EXACTLY", "LESS_THAN", "GREATER_THAN"] # exactly, less than, or greater than the time given to be due
        self.time_units = ["Years", "Months", "Days", "Hours", "Minutes", "Seconds"]
        self.selected_filter = self.filters[0] # None
        self.selected_match_type = self.match_types[0] # Exactly
        self.selected_time_unit = self.time_units[0] # Years

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

        self.time_values_label = QLabel("Time Unit: ")
        self.time_values_label.setFont(self.label_font)

        self.time_values_widget = QComboBox()
        self.time_values_widget.setCurrentIndex(self.time_units.index(self.selected_time_unit))
        for time_unit in self.time_units:
            self.time_values_widget.addItem(time_unit)
        self.time_values_widget.activated.connect(self.change_time_unit)

        self.time_values_label.setHidden(True)
        self.time_values_widget.setHidden(True)

        self.form_layout.addRow(self.time_values_label, self.time_values_widget)

        self.time_value_input_label = QLabel("Value: ")
        self.time_value_input_label.setFont(self.label_font)
        self.time_value_input = QSpinBox()
        self.time_value_input.setMinimumWidth(135)
        self.time_value_input.setMaximum(MAXIMUM_TIME_INPUT)

        self.time_value_input_label.setHidden(True)
        self.time_value_input.setHidden(True)

        self.form_layout.addRow(self.time_value_input_label, self.time_value_input)

        self.match_type_lbl = QLabel("Matching Target: ")

        self.match_type_selector = QComboBox()
        self.match_type_selector.setCurrentIndex(self.match_types.index(self.selected_match_type))
        for match_type in self.match_types:
            self.match_type_selector.addItem(match_type)
        self.match_type_selector.activated.connect(self.change_match_type)

        self.match_type_lbl.setHidden(True)
        self.match_type_selector.setHidden(True)

        self.form_layout.addRow(self.match_type_lbl, self.match_type_selector)

        self.group_box.setLayout(self.form_layout)

        self.window_layout.addWidget(self.group_box)
        self.window_layout.addWidget(self.button_box, QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.window_layout)

        self.resize(350, 250)

    def change_match_type(self):
        self.selected_match_type = self.match_type_selector.currentText()

    def change_time_unit(self):
        self.selected_time_unit = self.time_values_widget.currentText()

    def close_win(self):
        self.destroy(True)

    def filter_tasks(self):
        if self.selected_filter == "Due Date":
            date = self.due_date_picker.date().toString("yyyy-MM-dd")
            self.fill_tree_function(mode=self.selected_filter, date=date)
        if self.selected_filter == "Time Till Overdue":
            time_value = self.time_value_input.value()
            self.fill_tree_function(mode=self.selected_filter, time_unit=self.selected_time_unit, time_value=time_value, match_type=self.selected_match_type)


    def renderConfigurations(self):
        """Show the rest of the options based on the selected filter."""
        text = self.filter_by.currentText()
        if text == "None":
            self.due_date_label.setHidden(True) 
            self.due_date_picker.setHidden(True)
            self.time_values_label.setHidden(True)
            self.time_values_widget.setHidden(True)
            self.time_value_input_label.setHidden(True)
            self.time_value_input.setHidden(True)
            self.match_type_lbl.setHidden(True)
            self.match_type_selector.setHidden(True)
        elif text == "Due Date":
            # Find tasks that match the specific due date.
            self.due_date_label.setHidden(False) 
            self.due_date_picker.setHidden(False)
            self.time_values_label.setHidden(True)
            self.time_values_widget.setHidden(True)
            self.time_value_input_label.setHidden(True)
            self.time_value_input.setHidden(True)
            self.match_type_lbl.setHidden(True)
            self.match_type_selector.setHidden(True)
            self.selected_filter = text
        elif text == "Time Till Overdue":
            # Find tasks that are due within a range of Years, Months, hours, minutes & seconds.
            self.time_values_label.setHidden(False)
            self.time_values_widget.setHidden(False)
            self.due_date_label.setHidden(True) 
            self.due_date_picker.setHidden(True)
            self.time_value_input_label.setHidden(False)
            self.time_value_input.setHidden(False)
            self.match_type_lbl.setHidden(False)
            self.match_type_selector.setHidden(False)
            self.selected_filter = text



