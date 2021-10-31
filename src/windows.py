from imports import *
from windows import *
from code_editors import *
from edit_tabs import *

class EditTodoWindow(QtWidgets.QDialog):
    def __init__(self, Parent, title, text, sound=None, isCompletedTask=False, taskToComplete='', soundAlarm=False, newText='', isTimeShowing=False, prev_date='', prev_status='', tree=None, shouldPlayOnStart=False):
        super().__init__(parent=Parent)
        self.title = title
        self.text = text
        self.is_completed_task = isCompletedTask
        self.task = taskToComplete
        if self.is_completed_task == False:
            self.sound = None
            self.soundAlarm = True
        self.sound = sound
        self.soundAlarm = soundAlarm
        self.newText = newText
        self.isTimeShowing = isTimeShowing
        self.prev_date = prev_date
        self.prev_status = prev_status
        self.tree = tree
        self.shouldPlayOnStart = shouldPlayOnStart
        if self.sound != None:
            if self.isTimeShowing == False:
                if self.shouldPlayOnStart == True:
                    self.sound.play()
        self.width = 520
        self.height = 240
        self.setWindowTitle(self.title)
        #self.setFixedSize(self.width, self.height)
        self.table_widget = EditTodoTabs(self, self.text, self.task, self.soundAlarm, self.sound, newText=self.newText, prev_date=self.prev_date, prev_status=self.prev_status, tree=self.tree)
        e = QVBoxLayout()
        e.addWidget(self.table_widget)
        self.setLayout(e)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        self.destroyed.connect(self.closeEvent)
    
    def closeEvent(self, event):
        if self.sound != None:
            self.sound.stop()
            self.destroy()
        else:
            self.destroy()



