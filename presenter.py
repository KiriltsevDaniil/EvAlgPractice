from Problem.Model.model import Model
from GUI.widget import Widget

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication

import sys


class Presenter:
    def __init__(self):
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
        self.app = QApplication(sys.argv)

        self.Model = Model()
        self.View = Widget()
        
        self.View.set_send_data(self.view_to_model)
        self.View.set_get_band_width(self.get_band_width)
        self.Model.set_send_data(self.model_to_view)

        self.View.set_change_parameter(self.change_parameter)
    def run(self):
        self.View.show()
        self.View.setFixedSize(self.View.size())
        self.send_parameters()
        sys.exit(self.app.exec_())
    
    # Logs block
    def log(self, logs):
        self.View.appendStringToLog(logs)
    
    # Params block
    def send_parameters(self):
        self.View.setVariablesBox(self.Model.get_parameters())

    def change_parameter(self, key: str, val: int):
        self.Model.set_parameter(key, val)

    # Main alley block
    def view_to_model(self, band_width: int, rects: list):
        self.Model.process_data(band_width, rects)
        self.Model.solve()    # last population, not fittest

    def model_to_view(self, population):
        self.View.receive_population(population)

    def get_band_width(self):
        return Model.get_band_width()

pres = Presenter()
pres.run()
