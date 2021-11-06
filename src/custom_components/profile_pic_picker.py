from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

class ProfilePicPicker(QtWidgets.QToolButton):
    def __init__(self, parent, profile_pic, save_to, func):
        super().__init__(parent=parent)
        self.profile_pic = profile_pic
        self.save_to = save_to
        self.func = func
        self.setAutoFillBackground(True)
        self.setIcon(QIcon(self.profile_pic))
        self.big = None
        self.icon_size = QSize(50, 50)
        self.setIconSize(self.icon_size)
        self.setToolTip("Profile Picture")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def make_big(self, big):
        self.big = big

    def mouseDoubleClickEvent(self, event):
        image = QtWidgets.QFileDialog.getOpenFileName(self, "Insert Image", ".", "PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)")
        image_path = image[0]
        if image_path != "":
            self.profile_pic = image_path
            self.setIcon(QIcon(self.profile_pic))
            self.setIconSize(self.icon_size)
            if self.big != None:
                self.big.setIcon(QIcon(self.profile_pic))
                self.big.setIconSize(self.big.icon_size)
            self.func(self.save_to, {"background-image":image_path})


class BigProfilePicPicker(ProfilePicPicker):
    def __init__(self, parent, profile_pic, save_to, func, change_to):
        super().__init__(parent=parent, profile_pic=profile_pic, save_to=save_to, func=func)
        self.profile_pic = profile_pic
        self.save_to = save_to
        self.func = func
        self.change_to = change_to
        self.setAutoFillBackground(True)
        self.setIcon(QIcon(self.profile_pic))
        self.icon_size = QSize(150, 150)
        self.setIconSize(self.icon_size)
        self.setToolTip("Profile Picture")
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mouseDoubleClickEvent(self, event):
        image = QtWidgets.QFileDialog.getOpenFileName(self, "Insert Image", ".", "PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)")
        image_path = image[0]
        if image_path != "":
            self.profile_pic = image_path
            self.setIcon(QIcon(self.profile_pic))
            self.setIconSize(self.icon_size)
            self.change_to.setIcon(QIcon(self.profile_pic))
            self.change_to.setIconSize(self.change_to.icon_size)
            self.func(self.save_to, {"background-image":image_path})

    