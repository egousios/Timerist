from PyQt5.QtWidgets import QDialogButtonBox, QGroupBox
import sys
import os
import subprocess
sys.path.insert(0, "../")
from app import *
from .platforms import executePlatformCompatibleAuthCMD
import pyrebase

firebaseConfig = {
    "apiKey":"AIzaSyA6ct9DXoP9bFJPLdNLjyiycGbmjtLdKVY",
    "authDomain":"timerist-f6564.firebaseapp.com",
    "databaseURL":"https://timerist-f6564-default-rtdb.firebaseio.com",
    "projectId":"timerist-f6564",
    "storageBucket":"timerist-f6564.appspot.com",
    "messagingSenderId":"424996934722",
    "appId":"1:424996934722:web:f4403dcbf2494af0f009db",
    "measurementId":"G-Q30JJLH8QZ"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

def give(s):
    return s

id = QFontDatabase.addApplicationFont("assets/Poppins-Medium.ttf")
_fontstr = QFontDatabase.applicationFontFamilies(id)[0]
_font = QFont(_fontstr, 10)

class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Window properties
        self.title = 'Login'
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("app_icon.ico"))
        self.setWindowFlags(Qt.Window)
        self.resize(200, 200)
        self.tool_btn_size = QSize(50, 50)

        # Fonts
        id = QFontDatabase.addApplicationFont("assets/Poppins-Medium.ttf")
        _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
        _font = QFont(_fontstr, 30)

        id2 = QFontDatabase.addApplicationFont("assets/Segoe UI.ttf")
        _fontstr2 = QFontDatabase.applicationFontFamilies(id2)[0]
        field_font = QFont(_fontstr2, 15)

        id3 = QFontDatabase.addApplicationFont("assets/Ubuntu-Medium.ttf")
        _fontstr3 = QFontDatabase.applicationFontFamilies(id3)[0]
        font3 = QFont(_fontstr3, 30)

        # Validity
        self.invalid = QLabel("Invalid Username Or Password!")
        f = field_font
        f.setPointSize(20)
        self.invalid.setFont(f)
        self.invalid.setVisible(False)
        self.retry = QtWidgets.QToolButton()
        self.retry.setStyleSheet("border: none;")
        self.retry.setIcon(QIcon("images/retry.png"))
        self.retry.setIconSize(self.tool_btn_size)
        self.retry.clicked.connect(self.Retry)
        self.retry.setVisible(False)

        # Widgets & Layouts for Resize
        self.formLayout = QFormLayout()
        self.boxLayout = QVBoxLayout()
        self.groupWidget = QGroupBox()
        self.groupWidget.setStyleSheet('QGroupBox:title {''subcontrol-origin: margin;''subcontrol-position: top center;''padding-left: 10px;''padding-right: 10px;} QGroupBox {font-size: 35px; font-weight: bold; font-family: Poppins-Medium;}')
        self.groupWidget.setTitle('Login')

        # Field Labels
        self.email = QtWidgets.QWidget()
        self.password = QtWidgets.QWidget()
        self.email_label = QLabel("Email: ")
        self.email_label.setFont(font3)
        self.password_label = QLabel("Password: ")
        self.password_label.setFont(font3)

        # Fields
        self.email_field_layout = QHBoxLayout()
        self.password_field_layout = QHBoxLayout()

        self.email_icon = QtWidgets.QToolButton()
        self.email_icon.setStyleSheet("border: none;")
        self.email_icon.setIcon(QIcon("images/email.png"))
        self.email_icon.setIconSize(self.tool_btn_size)
        
        self.password_icon = QtWidgets.QToolButton()
        self.password_icon.setStyleSheet("border: none;")
        self.password_icon.setIcon(QIcon("images/password.png"))
        self.password_icon.setIconSize(self.tool_btn_size)

        self.email_field = QtWidgets.QLineEdit(self.groupWidget)
        self.email_field.setFont(field_font)
        self.email_field.setMinimumSize(170, 50)
        self.email_field.setStyleSheet('QLineEdit {border-radius: 3px; border: 1px solid #000;} QLineEdit:hover {border: 3px solid #79bef2;}')
        self.email_field_layout.addWidget(self.email_icon, 0)
        self.email_field_layout.addWidget(self.email_field, 0)

        self.password_field = QtWidgets.QLineEdit(self.groupWidget)
        self.password_field.setFont(field_font)
        self.password_field.setMinimumSize(170, 50)
        self.password_field.setStyleSheet('QLineEdit {border-radius: 3px; border: 1px solid #000;} QLineEdit:hover {border: 3px solid #79bef2;}')
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout = QVBoxLayout()
        self.password_field_layout.addWidget(self.password_icon, 0)
        self.password_field_layout.addWidget(self.password_field, 0)

        self.email.setLayout(self.email_field_layout)
        self.password.setLayout(self.password_field_layout)

        self.formLayout.addRow(self.email_label, self.email)
        self.formLayout.addRow(self.password_label, self.password)

        self.groupWidget.setLayout(self.formLayout)

        self.buttonBox = QtWidgets.QWidget()
        self.buttonLayout = QHBoxLayout()

        btnfont = _font
        btnfont.setPointSize(15)

        self.verifyBtn = QtWidgets.QPushButton()
        self.verifyBtn.setText("Verify")
        self.verifyBtn.setStyleSheet("QPushButton {border-radius: 5px; background-color: #0d6efd; color: white;} QPushButton:hover {background-color: #0b60de;}")
        self.verifyBtn.setMinimumSize(80, 50)
        self.verifyBtn.setFont(btnfont)
        self.verifyBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.verifyBtn.clicked.connect(self.loginToApp)

        self.registerLbl = QLabel("Don't Already Have An Account ?")
        f = f
        f.setPointSize(12)
        self.registerLbl.setFont(f)
        self.registerBtn = QtWidgets.QToolButton()
        self.registerBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.registerBtn.setIcon(QIcon("images/right-arrow-light.png"))
        self.registerBtn.setIconSize(self.tool_btn_size)
        self.registerBtn.setText("Sign Up")
        self.registerBtn.setStyleSheet("QToolButton {border-radius: 5px; background-color: #28a745; color: white;} QToolButton:hover {background-color: #218f3a;}")
        self.registerBtn.setFont(btnfont)
        self.registerBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.registerBtn.setMaximumHeight(50)
        self.registerBtn.clicked.connect(self.registerWin)

        self.buttonLayout.addWidget(self.verifyBtn, 70)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.registerLbl, 20, Qt.AlignRight)
        self.buttonLayout.addWidget(self.registerBtn, Qt.AlignRight)

        self.buttonBox.setLayout(self.buttonLayout)


        self.invalidBox = QHBoxLayout()
        self.invalidBox.addWidget(self.invalid, 75)
        self.invalidBox.addWidget(self.retry, 25)
        self.invalidBoxWidget = QtWidgets.QWidget()
        self.invalidBoxWidget.setLayout(self.invalidBox)

        self.boxLayout.addWidget(self.groupWidget)
        self.boxLayout.addWidget(self.invalidBoxWidget)
        self.boxLayout.addWidget(self.buttonBox)

        self.setLayout(self.boxLayout)

    def loginToApp(self):
        email = self.email_field.text()
        password = self.password_field.text()
        '''
        try:
            auth.sign_in_with_email_and_password(email,password)
            app.setFont(_font)
            clipboard=app.clipboard()
            sound_file = 'assets/alarm.wav'
            sound = QtMultimedia.QSoundEffect()
            sound.setSource(QtCore.QUrl.fromLocalFile(sound_file))
            sound.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
            sound.setVolume(50)
            ui.setupUi(Timerist, sound, email=email, password=password)
            Timerist.showMaximized()
            self.setParent(Timerist)
            self.destroy()
        except:
            self.invalid.setVisible(True)
            self.retry.setVisible(True)
        '''
        # This is to check for errors in the code

        auth.sign_in_with_email_and_password(email,password)
        app.setFont(_font)
        clipboard=app.clipboard()
        sound_file = 'assets/alarm.wav'
        sound = QtMultimedia.QSoundEffect()
        sound.setSource(QtCore.QUrl.fromLocalFile(sound_file))
        sound.setLoopCount(QtMultimedia.QSoundEffect.Infinite)
        sound.setVolume(50)
        ui.setupUi(Timerist, sound, email=email, password=password)
        Timerist.showMaximized()
        self.setParent(Timerist)
        self.destroy(True)



    def Retry(self):
        self.email_field.setText("")
        self.password_field.setText("")
        self.invalid.setVisible(False)
        self.retry.setVisible(False)

    def registerWin(self):
        register = RegisterWindow()
        register.exec_()

class RegisterWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # Window properties
        self.title = 'Register'
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("app_icon.ico"))
        self.setWindowFlags(Qt.Window)
        self.resize(200, 200)
        self.tool_btn_size = QSize(50, 50)

        # Fonts
        id = QFontDatabase.addApplicationFont("assets/Poppins-Medium.ttf")
        _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
        _font = QFont(_fontstr, 30)

        id2 = QFontDatabase.addApplicationFont("assets/Segoe UI.ttf")
        _fontstr2 = QFontDatabase.applicationFontFamilies(id2)[0]
        field_font = QFont(_fontstr2, 15)

        id3 = QFontDatabase.addApplicationFont("assets/Ubuntu-Medium.ttf")
        _fontstr3 = QFontDatabase.applicationFontFamilies(id3)[0]
        font3 = QFont(_fontstr3, 30)

        # Validity
        self.invalid = QLabel("Your passwords do not match and or your password is taken.")
        self.invalid2 = QLabel("The length of the password must be at least 6 characters.")
        self.invalid3 = QLabel("Your email must include an '@'.")
        f = field_font
        f.setPointSize(20)
        self.invalid.setFont(f)
        self.invalid.setVisible(False)
        self.invalid2.setFont(f)
        self.invalid2.setVisible(False)
        self.invalid3.setFont(f)
        self.invalid3.setVisible(False)
        self.retry = QtWidgets.QToolButton()
        self.retry.setStyleSheet("border: none;")
        self.retry.setIcon(QIcon("images/retry.png"))
        self.retry.setIconSize(self.tool_btn_size)
        self.retry.clicked.connect(self.Retry)
        self.retry.setVisible(False)
        
        self.retry2 = QtWidgets.QToolButton()
        self.retry2.setStyleSheet("border: none;")
        self.retry2.setIcon(QIcon("images/retry.png"))
        self.retry2.setIconSize(self.tool_btn_size)
        self.retry2.clicked.connect(self.Retry)
        self.retry2.setVisible(False)

        self.retry3 = QtWidgets.QToolButton()
        self.retry3.setStyleSheet("border: none;")
        self.retry3.setIcon(QIcon("images/retry.png"))
        self.retry3.setIconSize(self.tool_btn_size)
        self.retry3.clicked.connect(self.Retry)
        self.retry3.setVisible(False)

        self.success = QLabel("Your account has sucessfully been created.")
        self.success.setStyleSheet("color: green;")
        self.success.setFont(f)
        self.success.setVisible(False)

        self.close_success_msg = QtWidgets.QToolButton()
        self.close_success_msg.setStyleSheet("border: none;")
        self.close_success_msg.setIcon(QIcon("images/remove.png"))
        self.close_success_msg.setIconSize(self.tool_btn_size)
        self.close_success_msg.setToolTip("Dismiss")
        self.close_success_msg.clicked.connect(self.CloseSuccessMsg)
        self.close_success_msg.setVisible(False)

        # Widgets & Layouts for Resize
        self.formLayout = QFormLayout()
        self.boxLayout = QVBoxLayout()
        self.groupWidget = QGroupBox()
        self.groupWidget.setStyleSheet('QGroupBox:title {''subcontrol-origin: margin;''subcontrol-position: top center;''padding-left: 10px;''padding-right: 10px;} QGroupBox {font-size: 35px; font-weight: bold; font-family: Poppins-Medium;}')
        self.groupWidget.setTitle('Register')

        # Field Labels
        self.email = QtWidgets.QWidget()
        self.password = QtWidgets.QWidget()
        self.confirm_password = QtWidgets.QWidget()
        self.email_label = QLabel("Email: ")
        self.email_label.setFont(font3)
        self.password_label = QLabel("Password: ")
        self.password_label.setFont(font3)
        self.confirm_password_label = QLabel("Confirm Password: ")
        self.confirm_password_label.setFont(font3)


        # Fields
        self.email_field_layout = QHBoxLayout()
        self.password_field_layout = QHBoxLayout()
        self.confirm_password_field_layout = QHBoxLayout()

        self.email_icon = QtWidgets.QToolButton()
        self.email_icon.setStyleSheet("border: none;")
        self.email_icon.setIcon(QIcon("images/email.png"))
        self.email_icon.setIconSize(self.tool_btn_size)
        
        self.password_icon = QtWidgets.QToolButton()
        self.password_icon.setStyleSheet("border: none;")
        self.password_icon.setIcon(QIcon("images/password.png"))
        self.password_icon.setIconSize(self.tool_btn_size)

        self.confirm_password_icon = QtWidgets.QToolButton()
        self.confirm_password_icon.setStyleSheet("border: none;")
        self.confirm_password_icon.setIcon(QIcon("images/password.png"))
        self.confirm_password_icon.setIconSize(self.tool_btn_size)

        self.email_field = QtWidgets.QLineEdit(self.groupWidget)
        self.email_field.setFont(field_font)
        self.email_field.setMinimumSize(170, 50)
        self.email_field.setStyleSheet('QLineEdit {border-radius: 3px; border: 1px solid #000;} QLineEdit:hover {border: 3px solid #79bef2;}')
        self.email_field_layout.addWidget(self.email_icon, 0)
        self.email_field_layout.addWidget(self.email_field, 0)

        self.password_field = QtWidgets.QLineEdit(self.groupWidget)
        self.password_field.setFont(field_font)
        self.password_field.setMinimumSize(170, 50)
        self.password_field.setStyleSheet('QLineEdit {border-radius: 3px; border: 1px solid #000;} QLineEdit:hover {border: 3px solid #79bef2;}')
        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_field_layout.addWidget(self.password_icon, 0)
        self.password_field_layout.addWidget(self.password_field, 0)

        self.confirm_password_field = QtWidgets.QLineEdit(self.groupWidget)
        self.confirm_password_field.setFont(field_font)
        self.confirm_password_field.setMinimumSize(170, 50)
        self.confirm_password_field.setStyleSheet('QLineEdit {border-radius: 3px; border: 1px solid #000;} QLineEdit:hover {border: 3px solid #79bef2;}')
        self.confirm_password_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_field_layout.addWidget(self.confirm_password_icon, 0)
        self.confirm_password_field_layout.addWidget(self.confirm_password_field, 0)

        self.email.setLayout(self.email_field_layout)
        self.password.setLayout(self.password_field_layout)
        self.confirm_password.setLayout(self.confirm_password_field_layout)

        self.formLayout.addRow(self.email_label, self.email)
        self.formLayout.addRow(self.password_label, self.password)
        self.formLayout.addRow(self.confirm_password_label, self.confirm_password)

        self.groupWidget.setLayout(self.formLayout)

        self.buttonBox = QtWidgets.QWidget()
        self.buttonLayout = QHBoxLayout()

        btnfont = _font
        btnfont.setPointSize(15)

        self.verifyBtn = QtWidgets.QPushButton()
        self.verifyBtn.setText("Proceed")
        self.verifyBtn.setStyleSheet("QPushButton {border-radius: 5px; background-color: #0d6efd; color: white;} QPushButton:hover {background-color: #0b60de;}")
        self.verifyBtn.setMinimumSize(80, 50)
        self.verifyBtn.setFont(btnfont)
        self.verifyBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.verifyBtn.clicked.connect(self.registerToApp)

        self.loginLbl = QLabel("Already Have An Account ?")
        f = f
        f.setPointSize(12)
        self.loginLbl.setFont(f)
        self.loginBtn = QtWidgets.QToolButton()
        self.loginBtn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.loginBtn.setIcon(QIcon("images/right-arrow-light.png"))
        self.loginBtn.setIconSize(self.tool_btn_size)
        self.loginBtn.setText("Login")
        self.loginBtn.setStyleSheet("QToolButton {border-radius: 5px; background-color: #dc3545; color: white;} QToolButton:hover {background-color: #c42d3c;}")
        self.loginBtn.setFont(btnfont)
        self.loginBtn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.loginBtn.setMaximumHeight(50)
        self.loginBtn.clicked.connect(self.loginWin)

        self.buttonLayout.addWidget(self.verifyBtn, 70)
        self.buttonLayout.addStretch()
        self.buttonLayout.addWidget(self.loginLbl, 20, Qt.AlignRight)
        self.buttonLayout.addWidget(self.loginBtn, Qt.AlignRight)

        self.buttonBox.setLayout(self.buttonLayout)


        self.invalidBox = QVBoxLayout()
        self.section4 = QtWidgets.QWidget()
        self.section3 = QtWidgets.QWidget()
        self.section2 = QtWidgets.QWidget()
        self.section1 = QtWidgets.QWidget()
        self.horizontal3 = QHBoxLayout()
        self.horizontal3.addWidget(self.invalid3, 75)
        self.horizontal3.addWidget(self.retry3, 25)
        self.section3.setLayout(self.horizontal3)
        self.horizontal2 = QHBoxLayout()
        self.horizontal2.addWidget(self.invalid2, 75)
        self.horizontal2.addWidget(self.retry2, 25)
        self.section2.setLayout(self.horizontal2)
        self.horizontal = QHBoxLayout()
        self.horizontal.addWidget(self.invalid, 75)
        self.horizontal.addWidget(self.retry, 25)
        self.section1.setLayout(self.horizontal)
        self.horizontal4 = QHBoxLayout()
        self.horizontal4.addWidget(self.success, 75)
        self.horizontal4.addWidget(self.close_success_msg, 25)
        self.section4.setLayout(self.horizontal4)
        self.invalidBox.addWidget(self.section4)
        self.invalidBox.addWidget(self.section3)
        self.invalidBox.addWidget(self.section2)
        self.invalidBox.addWidget(self.section1)
        self.invalidBoxWidget = QtWidgets.QWidget()
        self.invalidBoxWidget.setLayout(self.invalidBox)
        self.boxLayout.addWidget(self.groupWidget)
        self.boxLayout.addWidget(self.invalidBoxWidget)
        self.boxLayout.addWidget(self.buttonBox)

        self.setLayout(self.boxLayout)

    def registerToApp(self):
        email = self.email_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()
        if '@' in email:
            if len(password) > 6:
                if password == confirm_password:
                    try:
                        auth.create_user_with_email_and_password(email,password)
                        try:
                            os.mkdir(f"users/{email}")
                            executePlatformCompatibleAuthCMD(email)
                            self.success.setVisible(True)
                            self.close_success_msg.setVisible(True)
                            self.giveToLogin(self)
                            self.destroy(True)
                        except:
                            pass
                    except:
                        self.invalid.setVisible(True)
                        self.retry.setVisible(True)
            else:
                try:
                    auth.create_user_with_email_and_password(email,password)
                    try:
                        os.mkdir(f"users/{email}")
                        executePlatformCompatibleAuthCMD(email)
                        self.success.setVisible(True)
                        self.close_success_msg.setVisible(True)
                        self.giveToLogin(self)
                        self.destroy(True)
                    except:
                        pass
                except:
                    self.invalid2.setVisible(True)
                    self.retry2.setVisible(True)
        else:
            try:
                auth.create_user_with_email_and_password(email,password)
                try:
                    os.mkdir(f"users/{email}")
                    executePlatformCompatibleAuthCMD(email)
                    self.success.setVisible(True)
                    self.close_success_msg.setVisible(True)
                    self.giveToLogin(self)
                    self.destroy(True)
                except:
                    pass
            except:
                self.invalid3.setVisible(True)
                self.retry3.setVisible(True)

    def Retry(self):
        self.email_field.setText("")
        self.password_field.setText("")
        self.confirm_password_field.setText("")
        self.invalid.setVisible(False)
        self.invalid2.setVisible(False)
        self.invalid2.setVisible(False)
        self.retry.setVisible(False)
        self.retry2.setVisible(False)
        self.retry3.setVisible(False)

    def CloseSuccessMsg(self):
        self.success.setVisible(False)
        self.close_success_msg.setVisible(False)

    def loginWin(self):
        login = LoginWindow()
        login.exec_()

    def giveToLogin(self, child):
        login = LoginWindow()
        child.setParent(login)
        login.show()
