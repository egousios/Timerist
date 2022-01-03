import sys, os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon
from PyQt5.QtWidgets import QComboBox, QDialog, QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox, QPushButton, QScrollArea, QScrollBar, QSizePolicy, QSpacerItem, QSpinBox, QToolButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from custom_components.color_value_shower import ColorValueShower
from custom_components.single_line_text_input import SingleLineTextInput
from custom_components.search_bar import SearchBar
from utils import write_and_save_json_data, load_json_data_from_json_file

# get the paths to the themes.
def get_theme_paths(themes_directory):
    return [os.path.join(themes_directory, file) for file in os.listdir(themes_directory) if file.endswith(".qss")]

# Program Constants
WINDOW_TITLE = "Theme Editor"
WINDOW_ICON = "images/color_wheel.png"
WINDOW_SIZE = (980, 600)
WINDOW_STYLESHEET = """
QMessageBox {
    background-color: #fff;
}

QMessageBox QLabel {
    color: #000;
}

QToolButton {
    background: rgba(255, 255, 255, 0.25);
    color: #252424;
    border: 2px solid #233cad;
    border-radius: 5px;
    font-family: OpenSans-SemiBold;
}

QToolButton:hover {
    background: rgba(255, 255, 255, 0.25);
    color: #252424;
    border: 2px solid #50a6cc;
    border-radius: 5px;
}

QMainWindow {
    background-color: #fff;
}

QPushButton {
    background: rgba(255, 255, 255, 0.25);
    color: #252424;
    border: 2px solid #233cad;
    border-radius: 5px;
    font-family: OpenSans-SemiBold;
}

QComboBox {
    background: rgba(255, 255, 255, 0.25);
    color: #252424;
    border: 2px solid #233cad;
    border-radius: 5px;
    font-family: OpenSans-SemiBold;
}

QPushButton:hover {
    background: rgba(255, 255, 255, 0.25);
    color: #252424;
    border: 2px solid #50a6cc;
    border-radius: 5px;
}



QListWidget {
    background: rgba(255, 255, 255, 0.25);
    color: #252424;
    border: 2px solid #233cad;
    border-radius: 5px;
}

QPushButton:disabled {
    background-color: rgba(52, 52, 52, 0.16);
}

QGroupBox:title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding-left: 10px;
    padding-right: 10px;
} 

QGroupBox {
    font-size: 25px; 
    font-family: OpenSans-SemiBold;
}
"""
SCROLLBAR_STYLESHEET = """
QScrollBar:horizontal
{
    height: 15px;
    margin: 3px 15px 3px 15px;
    border: 1px transparent #2A2929;
    border-radius: 4px;
    background-color: white;
}

QScrollBar::handle:horizontal
{
    background-color: black; 
    min-width: 5px;
    border-radius: 4px;
}

QScrollBar:vertical
{
    background-color: white;
    width: 15px;
    margin: 15px 3px 15px 3px;
    border: 1px transparent #2A2929;
    border-radius: 4px;
}

QScrollBar::handle:vertical
{
    background-color: black;
    min-height: 5px;
    border-radius: 4px;
}

QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal
{
    border: none;
    background: none;
    color: none;
}

QScrollBar::add-line:horizontal {
    border: none;
    background: none;
}

QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
}

QScrollBar::right-arrow:vertical, QScrollBar::left-arrow:vertical
{
    border: none;
    background: none;
    color: none;
}

QScrollBar::add-line:vertical {
    border: none;
    background: none;
}

QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
"""
TEXT_INPUT_FONT = ("OpenSans-SemiBold", 12)
BUTTON_FONT = ("OpenSans-SemiBold", 14)
THEME_FILES = get_theme_paths("stylesheets")
THEMES = []
for theme in THEME_FILES:
    theme = theme.removeprefix("stylesheets\\") # remove the directory name
    theme = theme.removesuffix(".qss") # remove the file extension name
    theme = theme.replace(theme[0], theme[0].upper(), 1) # first character should be uppercase 
    theme = theme.replace(" ", "") # remove whitespaces 
    THEMES.append(theme) # We get our name from this character-removal formula

SAVED_THEME_DATAS_SOURCE = "stylesheets/theme_datas"
MAX_BORDER_WIDTH_PX, MAX_BORDER_RADIUS_PX = 50, 40
MAX_PADDING = 50
MIN_PADDING = 5
BORDER_STYLES = [
    "dashed",
    "dot-dash",
    "dot-dot-dash",
    "dotted",
    "double",
    "groved",
    "inset",
    "outset",
    "ridge",
    "solid",
    "none"
]
TEXT_DECORATIONS = [
    "none",
    "underline",
    "overline",
    "line-through"
]

"""APP variable. Don't Touch."""
app = QtWidgets.QApplication(sys.argv)

MAX_FONT_SIZE = 23
FONT_FAMILIES = [font for font in QFontDatabase().families()]
FONT_SIZES = [str(x)+"px" for x in range(MAX_FONT_SIZE) if x >= 15]

class SaveColorThemeData:
    """
    Json-File objects holding information about published color-themes
    in the ThemeEditor.
    """
    def __init__(self, theme_type, theme_base_theme, theme_name, theme_lighter_color, theme_darker_color):
        self.theme_type = theme_type # type of theme
        self.theme_base_theme = theme_base_theme # the theme this theme originates from
        self.theme_name = theme_name # the name of the theme
        self.theme_lighter_color = theme_lighter_color # lighter color of the theme gradient
        self.theme_darker_color = theme_darker_color # darker color of the theme gradient
        self.theme_file_path = f"stylesheets/{self.theme_name}.qss"
        self.theme_data_filepath = f"{SAVED_THEME_DATAS_SOURCE}/{self.theme_name}.json"

        self.theme_data = {
            "theme_type":self.theme_type,
            "theme_file_path":self.theme_file_path,
            "theme_base_theme":self.theme_base_theme,
            "theme_name":self.theme_name,
            "theme_lighter_color":self.theme_lighter_color,
            "theme_darker_color":self.theme_darker_color,
            "theme_data_filepath":self.theme_data_filepath
        }

        write_and_save_json_data(self.theme_data_filepath, self.theme_data)


class SaveCustomThemeData:
    """
    Json-File objects holding information about published custom-themes
    in the ThemeEditor.
    """
    def __init__(self, theme_type, theme_name,
    push_button_background_color,
    push_button_text_color,
    push_button_border_color,
    push_button_border_width,
    push_button_border_radius,
    push_button_border_style,
    push_button_padding,
    push_button_text_decoration,
    push_button_font_family,
    push_button_font_size,
    ):
        self.theme_type = theme_type
        self.theme_name = theme_name
        self.push_button_background_color = push_button_background_color
        self.push_button_text_color = push_button_text_color
        self.push_button_border_color = push_button_border_color
        self.push_button_border_width = push_button_border_width
        self.push_button_border_radius = push_button_border_radius
        self.push_button_border_style = push_button_border_style
        self.push_button_padding = push_button_padding
        self.push_button_text_decoration = push_button_text_decoration
        self.push_button_font_family = push_button_font_family
        self.push_button_font_size = push_button_font_size
        self.theme_file_path = f"stylesheets/{self.theme_name}.qss"
        self.theme_data_filepath = f"{SAVED_THEME_DATAS_SOURCE}/{self.theme_name}.json"

        self.theme_data = {
            "theme_type":self.theme_type,
            "theme_name":self.theme_name,
            "push_button_background_color":self.push_button_background_color,
            "push_button_text_color":self.push_button_text_color,
            "push_button_border_color":self.push_button_border_color,
            "push_button_border_width":self.push_button_border_width,
            "push_button_border_radius":self.push_button_border_radius,
            "push_button_border_style":self.push_button_border_style,
            "push_button_padding":self.push_button_padding,
            "push_button_text_decoration":self.push_button_text_decoration,
            "push_button_font_family":self.push_button_font_family,
            "push_button_font_size":self.push_button_font_size,
            "theme_file_path":self.theme_file_path,
            "theme_data_filepath":self.theme_data_filepath
        }

        write_and_save_json_data(self.theme_data_filepath, self.theme_data)


def get_updated_themes_list():
    """
    Returns an updated version of the 
    themes list.
    """
    THEME_FILES = get_theme_paths("stylesheets")
    THEMES = []
    for theme in THEME_FILES:
        theme = theme.removeprefix("stylesheets\\") # remove the directory name
        theme = theme.removesuffix(".qss") # remove the file extension name
        theme = theme.replace(theme[0], theme[0].upper(), 1) # first character should be uppercase 
        theme = theme.replace(" ", "") # remove whitespaces 
        THEMES.append(theme) # We get our name from this character-removal formula
    return THEMES

def get_updated_theme_files_list():
    """
    Returns an updated version of the theme
    files list.
    """
    THEME_FILES = get_theme_paths("stylesheets")
    return THEME_FILES

class ThemeEditor(QMainWindow):
    """
    This program is not to be used within Timerist;
    it is a seperate program for creating new themes that
    are automatically loaded into Timerist's theme options.
    """
    def __init__(self, parent=None):
        super(ThemeEditor, self).__init__(parent)
        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(WINDOW_ICON))
        self.resize(*WINDOW_SIZE)
        self.label_font = QFont("OpenSans-SemiBold", 13)
        self.tool_btn_size = QSize(60, 60)
        self.btn_font = QFont(*BUTTON_FONT)
        self.editor = QWidget()
        self.Menu = QWidget()
        self.menu_scroll = QScrollArea(widgetResizable=True)
        self.editor_scroll = QScrollArea(widgetResizable=True)
        self.selected_theme_from_menu = None
        self.selected_lighter_color = QColor(0, 0, 0).name()
        self.selected_darker_color = QColor(0, 0, 0).name()
        self.makeMenu()
        self.makeUI()
        self.open_menu()

    def makeUI(self):
        self.window_layout = QVBoxLayout()
        self.window_groupbox = QGroupBox()
        self.window_formlayout = QFormLayout()
        self.form_buttons_layout = QHBoxLayout()
        self.theme_types = ["Color/Element Theme", "Custom Theme"]
        self.selected_theme_type = self.theme_types[0] # first one
        self.color_base_theme = "stylesheets/gemstone.qss"

        self.theme_file_name, self.theme_file_data = None, None

        self.theme_type_lbl = QLabel("Theme Type: ")
        self.theme_type_lbl.setFont(self.label_font)

        self.theme_type_selector = QComboBox()
        self.theme_type_selector.setCurrentIndex(self.theme_types.index(self.selected_theme_type))
        self.theme_type_selector.addItems(self.theme_types)
        self.theme_type_selector.activated.connect(self.renderConfigurations)

        self.window_formlayout.addRow(self.theme_type_lbl, self.theme_type_selector)

        self.color_label_lighter = QLabel("Color - (Lighter Gradient): ")
        self.color_label_lighter.setFont(self.label_font)

        self.color_value_shower_lighter = ColorValueShower(widget_font=self.label_font, current_value=self.selected_lighter_color)

        self.window_formlayout.addRow(self.color_label_lighter, self.color_value_shower_lighter)

        self.color_label_darker = QLabel("Color - (Darker Gradient): ")
        self.color_label_darker.setFont(self.label_font)

        self.color_value_shower_darker = ColorValueShower(widget_font=self.label_font, current_value=self.selected_darker_color)

        self.window_formlayout.addRow(self.color_label_darker, self.color_value_shower_darker)

        self.color_theme_name_label = QLabel("Color/Element Name: ")
        self.color_theme_name_label.setFont(self.label_font)
        self.color_theme_name = SingleLineTextInput(text_input_font=QFont(*TEXT_INPUT_FONT))

        self.window_formlayout.addRow(self.color_theme_name_label, self.color_theme_name)

        self.custom_theme_name_label = QLabel("Theme Name: ")
        self.custom_theme_name_label.setFont(self.label_font)
        self.custom_theme_name = SingleLineTextInput(text_input_font=QFont(*TEXT_INPUT_FONT))

        self.custom_theme_name_label.setHidden(True)
        self.custom_theme_name.setHidden(True)

        self.window_formlayout.addRow(self.custom_theme_name_label, self.custom_theme_name)

        self.customizeable_widgets = ["QPushButton", "QToolButton"]

        self.push_button = QPushButton()
        self.push_button.setText(self.customizeable_widgets[self.customizeable_widgets.index("QPushButton")])

        self.push_button_options = QGroupBox()
        self.push_button_options.setTitle("Options")
        self.push_button_options_fl = QFormLayout()

        self.push_button_background_color = ColorValueShower(widget_font=self.label_font, current_value=QColor(0,0,0).name())
        self.push_button_text_color = ColorValueShower(widget_font=self.label_font, current_value=QColor(255,255,255).name())
        self.push_button_border_color = ColorValueShower(widget_font=self.label_font, current_value=QColor(145,145,145).name())
        self.push_button_border_width = QComboBox()
        self.push_button_border_width.addItems([str(x)+"px" for x in range(MAX_BORDER_WIDTH_PX)])
        self.push_button_border_radius = QComboBox()
        self.push_button_border_radius.addItems([str(x)+"px" for x in range(MAX_BORDER_RADIUS_PX)])
        self.push_button_border_style = QComboBox()
        self.push_button_border_style.addItems(BORDER_STYLES)
        self.push_button_padding = QComboBox()
        self.push_button_padding.addItems([str(x)+"px" for x in range(MAX_PADDING) if x >= MIN_PADDING])
        self.push_button_text_decoration = QComboBox()
        self.push_button_text_decoration.addItems(TEXT_DECORATIONS)
        self.push_button_font_family = QComboBox()
        self.push_button_font_family.addItems(FONT_FAMILIES)
        self.push_button_font_family.setCurrentIndex(FONT_FAMILIES.index("Ink Free"))
        self.push_button_font_size = QComboBox()
        self.push_button_font_size.addItems(FONT_SIZES)
        self.push_button_font_size.setCurrentIndex(0)

        self.push_button_options_labels = ["Background Color: ", "Text Color: ", "Border Color: ", "Border Width: ", "Border Radius: ", "Border Style: ", "Padding: ", "Text Decoration: ", "Font Family: ", "Font Size: "]
        self.push_button_options_list = [self.push_button_background_color, self.push_button_text_color,
        self.push_button_border_color, self.push_button_border_width, self.push_button_border_radius, self.push_button_border_style, self.push_button_padding, self.push_button_text_decoration, self.push_button_font_family, self.push_button_font_size]

        for widget in self.push_button_options_list:
            if isinstance(widget, ColorValueShower):
                widget.change_color_btn.clicked.connect(self.set_push_button_stylesheet)
            elif isinstance(widget, QComboBox):
                widget.activated.connect(self.set_push_button_stylesheet)

        self.set_push_button_stylesheet()

        for label in self.push_button_options_labels:
            Label = QLabel(label)
            Label.setFont(self.label_font)
            self.push_button_options_fl.addRow(Label, self.push_button_options_list[self.push_button_options_labels.index(label)])

        self.push_button_options.setLayout(self.push_button_options_fl)

        self.push_button.setHidden(True)
        self.push_button_options.setHidden(True)

        self.push_button_field = QWidget()
        self.push_button_field_layout = QVBoxLayout()
        self.push_button_field_layout.addWidget(self.push_button, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.push_button_field.setLayout(self.push_button_field_layout)

        self.push_button_options.setFixedWidth(self.push_button_background_color.width())
            
        self.window_formlayout.addRow(self.push_button_field, self.push_button_options)

        self.window_formlayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.submit_theme_btn = QPushButton("Submit")
        self.submit_theme_btn.setFont(self.btn_font)
        self.submit_theme_btn.clicked.connect(self.submit_theme)

        self.publish_theme_btn = QPushButton("Publish")
        self.publish_theme_btn.setFont(self.btn_font)
        self.publish_theme_btn.clicked.connect(self.publish_theme)

        self.menu_btn = QPushButton("Menu")
        self.menu_btn.setFont(self.btn_font)
        self.menu_btn.clicked.connect(self.open_menu)

        self.form_buttons_layout.addWidget(self.submit_theme_btn)
        self.form_buttons_layout.addWidget(self.publish_theme_btn)
        self.form_buttons_layout.addWidget(self.menu_btn)

        self.window_groupbox.setLayout(self.window_formlayout)
        self.window_layout.addWidget(self.window_groupbox)
        self.window_layout.addLayout(self.form_buttons_layout)
        self.setFont(QFont("OpenSans-SemiBold", 14))

    def set_push_button_stylesheet(self):
        self.push_button_stylesheet = "QPushButton" + "{" + f"""
        \tbackground-color: {self.push_button_background_color.current_value};
        \tcolor: {self.push_button_text_color.current_value};
        \tborder-color: {self.push_button_border_color.current_value};
        \tborder-width: {self.push_button_border_width.currentText()};
        \tborder-radius: {self.push_button_border_radius.currentText()};
        \tborder-style: {self.push_button_border_style.currentText()};
        \tpadding: {self.push_button_padding.currentText()};
        \ttext-decoration: {self.push_button_text_decoration.currentText()};
        \tfont-family: {self.push_button_font_family.currentText()};
        \tfont-size: {self.push_button_font_size.currentText()};
        """ + "}"
        self.push_button.setFont(QFont(self.push_button_font_family.currentText(), int(self.push_button_font_size.currentText().removesuffix("px"))))
        self.push_button.setStyleSheet(self.push_button_stylesheet)

    def publish_theme(self): 
        if self.selected_theme_type == "Color/Element Theme":
            if self.theme_file_name != None:
                if len(self.theme_file_name) > 1 and len(self.theme_file_name) < 15:
                    if not self.theme_file_name.lower() in [theme.lower() for theme in THEMES]:
                        theme_path = f"stylesheets/{self.theme_file_name}.qss"
                        theme=open(theme_path, "a").close()
                        with open(theme_path, "w") as file:
                            file.write(self.theme_file_data)
                            file.close()
                        create_theme_data_file = open(f"{SAVED_THEME_DATAS_SOURCE}/{self.theme_file_name}.json", "a").close()
                        save_theme_data = SaveColorThemeData(
                        self.selected_theme_type, 
                        self.color_base_theme, 
                        self.theme_file_name,
                        self.lighter_color,
                        self.darker_color
                        )
                        QMessageBox.information(self, "Success!", "Your theme was sucessfully published.")
                    else:
                        QMessageBox.warning(self, "Name Taken", f"Your theme name was already taken.")
                else:
                    QMessageBox.warning(self, "Too Short/Long", f"Your theme name must be at least one character, and less than 15 characters long.")
            else:
                QMessageBox.critical(self, "Publishing Error", f"You must submit your theme first before publishing it.")
        elif self.selected_theme_type == "Custom Theme":
            if self.custom_theme_name.text() != None:
                if len(self.custom_theme_name.text()) > 1 and len(self.custom_theme_name.text()) < 15:
                    if not self.custom_theme_name.text().lower() in [theme.lower() for theme in THEMES]:
                        theme_path = f"stylesheets/{self.custom_theme_name.text()}.qss"
                        theme=open(theme_path, "a").close()
                        with open(theme_path, "w") as file:
                            file.write(self.theme_file_data)
                            file.close()
                        create_theme_data_file = open(f"{SAVED_THEME_DATAS_SOURCE}/{self.custom_theme_name.text()}.json", "a").close()
                        save_theme_data = SaveCustomThemeData(
                            self.selected_theme_type,
                            self.custom_theme_name.text(),
                            self.push_button_background_color.current_value,
                            self.push_button_text_color.current_value,
                            self.push_button_border_color.current_value,
                            self.push_button_border_width.currentText(),
                            self.push_button_border_radius.currentText(),
                            self.push_button_border_style.currentText(),
                            self.push_button_padding.currentText(),
                            self.push_button_text_decoration.currentText(),
                            self.push_button_font_family.currentText(),
                            self.push_button_font_size.currentText()
                            )
                        QMessageBox.information(self, "Success!", "Your theme was sucessfully published.")
                    else:
                        QMessageBox.warning(self, "Name Taken", f"Your theme name was already taken.")
                else:
                    QMessageBox.warning(self, "Too Short/Long", f"Your theme name must be at least one character, and less than 15 characters long.")
            else:
                QMessageBox.critical(self, "Publishing Error", f"You must submit your theme first before publishing it.")

        
    def makeMenu(self):
        self.menu_layout = QVBoxLayout()

        menu_title = QLabel("Published Themes:")

        self.themes_searchbar = SearchBar()
        self.themes_searchbar.setFont(QFont("OpenSans-SemiBold", 14))
        self.themes_searchbar.setFixedWidth(int(menu_title.width()/2))
        self.themes_searchbar.setStyleSheet(SearchBar().styleSheet()+"""
        border: 2px solid #233cad;
        border-radius: 5px;
        """)
        self.themes_searchbar.textChanged.connect(self.search_themes)

        self.themes_list = QListWidget()
        self.themes_list.setMinimumSize(385, 420)
        self.themes_list.itemClicked.connect(self.change_selected_theme)
        lst = get_updated_themes_list()
        lst.remove("Default")
        self.themes_list.addItems(lst)

        self.view_action = QPushButton("View")
        self.view_action.setFont(self.btn_font)
        self.view_action.clicked.connect(self.view_theme)

        self.new_action = QPushButton("New +")
        self.new_action.setFont(self.btn_font)
        self.new_action.clicked.connect(self.new_theme)

        self.delete_action = QPushButton("Delete")
        self.delete_action.setFont(self.btn_font)
        self.delete_action.clicked.connect(self.delete_theme)

        self.actions_widget = QWidget()
        self.actions_widget_layout = QHBoxLayout()
        self.actions_widget_layout.addWidget(self.delete_action)
        self.actions_widget_layout.addWidget(self.view_action)
        self.actions_widget_layout.addWidget(self.new_action)
        self.actions_widget.setLayout(self.actions_widget_layout)
    
        self.menu_layout.addWidget(menu_title, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.menu_layout.addWidget(self.themes_searchbar, alignment=Qt.AlignCenter)
        self.menu_layout.addWidget(self.themes_list, alignment=Qt.AlignCenter)
        self.menu_layout.addWidget(self.actions_widget)
        self.menu_layout.addStretch(0)

    def refresh_themes_list(self):
        self.themes_list.clear()
        lst = get_updated_themes_list()
        lst.remove("Default")
        self.themes_list.addItems(lst)

    def delete_theme(self):
        if self.selected_theme_from_menu != None:
            ask = QMessageBox.warning(self, "Are you sure ?", "Do you want to delete this theme permanently ?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
            if ask == QtWidgets.QMessageBox.Yes:
                name = self.selected_theme_from_menu.replace(self.selected_theme_from_menu[0], self.selected_theme_from_menu[0].upper())
                stylesheet, json_data_file = f"stylesheets/{name}.qss", f"{SAVED_THEME_DATAS_SOURCE}/{name}.json"
                removal_datas = [stylesheet, json_data_file]
                for removal_data in removal_datas:
                    os.remove(removal_data)
                self.refresh_themes_list()

    def new_theme(self):
        # Set all options to default, or initial to create new theme.
        self.selected_theme_type = self.theme_types[0]
        self.theme_type_selector.setCurrentIndex(self.theme_types.index(self.selected_theme_type))
        self.selected_lighter_color = QColor(0, 0, 0).name()
        self.color_value_shower_lighter.set_color(self.selected_lighter_color)
        self.selected_darker_color = QColor(0, 0, 0).name()
        self.color_value_shower_darker.set_color(self.selected_darker_color)
        self.theme_file_name = ""
        self.color_theme_name.setText(self.theme_file_name)
        self.submit_theme_btn.setDisabled(False)
        self.publish_theme_btn.setDisabled(False)
        self.go_back()

    def view_theme(self):
        if self.selected_theme_from_menu != None:
            try:
                filename = self.selected_theme_from_menu.replace(self.selected_theme_from_menu[0], self.selected_theme_from_menu[0].lower(), 1)
            except:
                filename = self.selected_theme_from_menu
            theme_data_path_var = f"{SAVED_THEME_DATAS_SOURCE}/{filename}.json"
            saved_theme_data = load_json_data_from_json_file(theme_data_path_var)
            """Theme Type and Name will be in both types of themes."""
            theme_type = saved_theme_data["theme_type"]
            theme_name = saved_theme_data["theme_name"]
            if theme_type == "Color/Element Theme":
                theme_lighter_color = saved_theme_data["theme_lighter_color"]
                theme_darker_color = saved_theme_data["theme_darker_color"]
                # setting theme data
                self.selected_theme_type = theme_type
                self.color_theme_name.setText(theme_name)
                self.selected_lighter_color = theme_lighter_color
                self.color_value_shower_lighter.set_color(self.selected_lighter_color)
                self.selected_darker_color = theme_darker_color
                self.color_value_shower_darker.set_color(self.selected_darker_color)
                self.submit_theme_btn.setDisabled(True)
                self.publish_theme_btn.setDisabled(True)
                self.go_back()
            elif theme_type == "Custom Theme":
                pass

    def submit_theme(self):
        if self.selected_theme_type == "Color/Element Theme":
            with open(self.color_base_theme, "r") as f:
                data = f.read()
                f.close()
            self.theme_file_name = self.color_theme_name.text()
            self.lighter_color = self.color_value_shower_lighter.current_value
            self.darker_color = self.color_value_shower_darker.current_value
            self.theme_file_data = data.replace("#bf84f0", self.lighter_color)
            self.theme_file_data = self.theme_file_data.replace("#994e93", self.darker_color)
        elif self.selected_theme_type == "Custom Theme":
            self.theme_file_name = self.custom_theme_name.text()
            self.theme_file_data = open(self.color_base_theme, "r").read() + self.push_button_stylesheet



    def change_selected_theme(self):
        selected_items = self.themes_list.selectedItems()
        self.selected_theme_from_menu = ", ".join([selected_item.text() for selected_item in selected_items])


    def search_themes(self):
        # Get all root nodes
        all_items = self.themes_list.findItems("", Qt.MatchStartsWith)
            # matching items
        match_items = self.themes_list.findItems(self.themes_searchbar.text(), Qt.MatchStartsWith)
            # Hide all root nodes
        for item in all_items:
            item.setHidden(True)
            # Display the root node that meets the conditions
        for item in match_items:
            item.setHidden(False)


    def open_menu(self):
        self.Menu.setLayout(self.menu_layout)
        self.menu_scroll.setWidget(self.Menu)
        self.refresh_themes_list()
        self.takeCentralWidget()
        self.setCentralWidget(self.menu_scroll)

    def go_back(self):
        self.editor.setLayout(self.window_layout)
        self.editor_scroll.setWidget(self.editor)
        self.refresh_themes_list()
        self.takeCentralWidget()
        self.setCentralWidget(self.editor_scroll)

    def renderConfigurations(self):
        """Show the rest of the options based on the selected theme type."""
        text = self.theme_type_selector.currentText()
        if text == "Color/Element Theme":
            self.color_label_lighter.setHidden(False)
            self.color_value_shower_lighter.setHidden(False)
            self.color_label_darker.setHidden(False)
            self.color_value_shower_darker.setHidden(False)
            self.color_theme_name_label.setHidden(False)
            self.color_theme_name.setHidden(False)
            self.custom_theme_name_label.setHidden(True)
            self.custom_theme_name.setHidden(True)
            self.push_button.setHidden(True)
            self.push_button_options.setHidden(True)
            self.selected_theme_type = text
        elif text == "Custom Theme":
            self.color_label_lighter.setHidden(True)
            self.color_value_shower_lighter.setHidden(True)
            self.color_label_darker.setHidden(True)
            self.color_value_shower_darker.setHidden(True)
            self.color_theme_name_label.setHidden(True)
            self.color_theme_name.setHidden(True)
            self.custom_theme_name_label.setHidden(False)
            self.custom_theme_name.setHidden(False)
            self.push_button.setHidden(False)
            self.push_button_options.setHidden(False)
            self.selected_theme_type = text

# Runtime
def run():
    app.setStyle("Fusion")
    app.setStyleSheet(WINDOW_STYLESHEET)
    id = QFontDatabase.addApplicationFont("assets/OpenSans-SemiBold.ttf")
    _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
    APP_FONT = QFont(_fontstr, 15)
    app.setFont(APP_FONT)
    theme_editor = ThemeEditor()
    theme_editor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()