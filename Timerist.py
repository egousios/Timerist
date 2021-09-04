### Timerist.py combines all other source files and runs the app.
import sys
sys.path.insert(0, "../")
from auth import Auth, platforms
from auth.Auth import *
from auth.platforms import *

def run():
    app.setPalette(QtWidgets.QApplication.style().standardPalette())
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

run()