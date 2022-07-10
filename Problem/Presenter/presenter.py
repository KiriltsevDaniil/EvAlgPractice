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
        self.View.set_model(self.recieve_data)

    def gui(self):

        self.View.show()
        self.View.setFixedSize(self.View.size())
        sys.exit(self.app.exec_())

    def recieve_data(self, band_width: int, rects: list):
        self.model.process_data(band_width, rects)
        return self.model.solve()    # last population, not fittest



pres = Presenter()
pres.gui()
