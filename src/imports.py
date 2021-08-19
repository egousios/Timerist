from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtPrintSupport, QtWebEngineWidgets, Qsci
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys
import qtwidgets
from qtwidgets import AnimatedToggle
import json
from PyQt5.Qsci import QsciScintilla, QsciLexerJSON
from datetime import datetime
from backend.query import *
from backend.time import *
from json_settings_pckg.editor import load_editor_settings
from json_settings_pckg.editor import save_editor_settings
from document_editor import EditWindow
from edit_tabs import EditTodoTabs
from tabs import CollapseButton, TabBar, TabWidget
from utils import load_from_stylesheet, start_timer, User
from code_editors import SimpleJSONEditor, HTMLEditor
from windows import *

