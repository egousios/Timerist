from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QComboBox, QDateEdit, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget
from backend.time import get_date_range_list, Date

# Constants
SORT_SELECTOR_ICONS = ["default", "images/ascending.png", "images/descending.png"]
SORT_SELECTOR_ICON_SIZE = (50, 50)

class AdvancedTodoSearchFilterDialog(QtWidgets.QDialog):
    """A dialog window for searching through tasks with advanced filters."""
    def __init__(self, parent, fill_tree_function, sort_tree_function):
        super().__init__(parent=parent)
        self.fill_tree_function = fill_tree_function
        self.sort_tree_funcion = sort_tree_function
        self.setWindowTitle("Advanced Filter...")
        self.setWindowIcon(QIcon("images/search.png"))
        self.window_layout = QVBoxLayout()
        self.group_box = QGroupBox()
        self.form_layout = QFormLayout()
        self.label_font = QFont("Poppins", 15)

        self.button_box = QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.filter_tasks)
        self.button_box.rejected.connect(self.close_win)

        self.filters = ["None", "Due Date", "Due Date Range", "Sort By Upcoming"]
        self.sorts = ["Normal", "Ascending", "Descending"]
        self.selected_filter = self.filters[0] # None
        self.selected_sort = self.sorts[0] # Normal

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

        self.starting_due_date_label = QLabel("Matching Due Date (Start): ")
        self.starting_due_date_label.setFont(self.label_font)

        self.ending_due_date_label = QLabel("Matching Due Date (End): ")
        self.ending_due_date_label.setFont(self.label_font)

        self.starting_due_date_picker = QDateEdit()
        current_date = QtCore.QDate.currentDate()
        self.starting_due_date_picker.setDate(current_date)

        self.ending_due_date_picker = QDateEdit()
        current_date = QtCore.QDate.currentDate()
        self.ending_due_date_picker.setDate(current_date)

        self.starting_due_date_label.setHidden(True)
        self.starting_due_date_picker.setHidden(True)
        self.ending_due_date_label.setHidden(True)
        self.ending_due_date_picker.setHidden(True)

        self.form_layout.addRow(self.starting_due_date_label, self.starting_due_date_picker)
        self.form_layout.addRow(self.ending_due_date_label, self.ending_due_date_picker)

        self.sort_by_upcoming_label = QLabel("Sort By Upcoming: ")
        self.sort_by_upcoming_label.setFont(self.label_font)

        self.sort_by_upcoming = QComboBox()
        for i, sort in enumerate(self.sorts):
            self.sort_by_upcoming.addItem(sort)
            if i != 0:
                self.sort_by_upcoming.setItemIcon(i, QIcon(SORT_SELECTOR_ICONS[i]))
        self.sort_by_upcoming.setIconSize(QSize(*SORT_SELECTOR_ICON_SIZE))
        self.sort_by_upcoming.activated.connect(self.change_selected_sort)

        self.sort_by_upcoming_label.setHidden(True)
        self.sort_by_upcoming.setHidden(True)

        self.form_layout.addRow(self.sort_by_upcoming_label, self.sort_by_upcoming)

        self.group_box.setLayout(self.form_layout)

        self.window_layout.addWidget(self.group_box)
        self.window_layout.addWidget(self.button_box, QtCore.Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.window_layout)

        self.resize(self.window_layout.sizeHint())

    def change_selected_sort(self):
        text = self.sort_by_upcoming.currentText()
        self.selected_sort = text

    def close_win(self):
        self.destroy(True)

    def filter_tasks(self):
        if self.selected_filter == "Due Date":
            date = self.due_date_picker.date().toString("yyyy-MM-dd")
            self.fill_tree_function(mode=self.selected_filter, date=date)
        if self.selected_filter == "Due Date Range":
            starting_date = Date(
                self.starting_due_date_picker.date().year(),
                self.starting_due_date_picker.date().month(),
                self.starting_due_date_picker.date().day()
            )
            ending_date = Date(
                self.ending_due_date_picker.date().year(),
                self.ending_due_date_picker.date().month(),
                self.ending_due_date_picker.date().day()
            )
            self.fill_tree_function(mode=self.selected_filter, date_range=(starting_date, ending_date))
        if self.selected_filter == "Sort By Upcoming":
            self.sort_tree_funcion(sort_order=self.selected_sort)


    def renderConfigurations(self):
        """Show the rest of the options based on the selected filter."""
        text = self.filter_by.currentText()
        if text == "None":
            # Hide everything
            self.due_date_label.setHidden(True) 
            self.due_date_picker.setHidden(True)
            self.starting_due_date_label.setHidden(True)
            self.starting_due_date_picker.setHidden(True)
            self.ending_due_date_label.setHidden(True)
            self.ending_due_date_picker.setHidden(True)
            self.sort_by_upcoming_label.setHidden(True)
            self.sort_by_upcoming.setHidden(True)
        elif text == "Due Date":
            # Show the appropriate widgets for the selected filter.
            self.due_date_label.setHidden(False) 
            self.due_date_picker.setHidden(False)
            self.starting_due_date_label.setHidden(True)
            self.starting_due_date_picker.setHidden(True)
            self.ending_due_date_label.setHidden(True)
            self.ending_due_date_picker.setHidden(True)
            self.sort_by_upcoming_label.setHidden(True)
            self.sort_by_upcoming.setHidden(True)
            self.selected_filter = text # update the selected filter to the current
        elif text == "Due Date Range":
            self.due_date_label.setHidden(True) 
            self.due_date_picker.setHidden(True)
            self.starting_due_date_label.setHidden(False)
            self.starting_due_date_picker.setHidden(False)
            self.ending_due_date_label.setHidden(False)
            self.ending_due_date_picker.setHidden(False)
            self.sort_by_upcoming_label.setHidden(True)
            self.sort_by_upcoming.setHidden(True)
            self.selected_filter = text
        elif text == "Sort By Upcoming":
            self.due_date_label.setHidden(True) 
            self.due_date_picker.setHidden(True)
            self.starting_due_date_label.setHidden(True)
            self.starting_due_date_picker.setHidden(True)
            self.ending_due_date_label.setHidden(True)
            self.ending_due_date_picker.setHidden(True)
            self.sort_by_upcoming_label.setHidden(False)
            self.sort_by_upcoming.setHidden(False)
            self.selected_filter = text


