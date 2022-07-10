from Problem.Model.model import Model
from GUI.widget import Widget

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication

import sys


class Presenter:
    def __init__(self):
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
        self.app = QApplication(sys.argv)

        self.model = Model()
        self.View = Widget()

    def gui(self):

        self.View.show()
        self.View.setFixedSize(self.View.size())
        sys.exit(self.app.exec_())


pres = Presenter()
pres.gui()
