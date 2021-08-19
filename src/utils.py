from imports import *

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

def start_timer(end_date):
    current_date_time = QtCore.QDateTime.currentDateTime()
    fmt = current_date_time.toString("yyyy-MM-dd hh:mm:ss a")
    if datetime(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]), int(end_date[9:11]), int(end_date[14:16]), int(end_date[17:19])) <= datetime(int(fmt[0:4]), int(fmt[5:7]), int(fmt[8:10]), int(fmt[9:11]), int(fmt[14:16]), int(fmt[17:19])):
        return "yes"
    else:
        return f"{days_in_between(fmt, end_date)} time left."