from imports import *
from PyQt5 import QtCore

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

def load_from_stylesheet(file):
    '''
    A function that reads a qss stylesheet line-by-line
    and returns the data as a string for PyQt5 to read
    and parse the stylesheet.
    '''
    with open(file, "r") as f:
        data = f.read()
        f.close()
    return str(data)