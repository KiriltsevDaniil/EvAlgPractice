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
        self.View.set_step(self.view_to_model_step)
        self.View.set_finish(self.view_to_model_finish) 
        
        self.View.set_get_band_width(self.get_band_width)
        
        self.View.set_change_parameter(self.change_parameter)
        
        self.Model.set_send_data(self.model_to_view)

        self.steps = 0    
    def run(self):
        self.View.show()
        self.View.setFixedSize(self.View.size())
        self.send_parameters()
        sys.exit(self.app.exec_())
    
    # Logs block
    def model_log(self):
        for line in self.Model.get_logs():
            self.View.appendStringToLog(line, False)
    
    # Params block
    def send_parameters(self):
        self.View.setVariablesBox(self.Model.get_parameters())

    def change_parameter(self, key: str, val: int):
        self.Model.set_parameter(key, val)

    # Main alley block
    def view_to_model(self, band_width: int, rects: list, step=False):
        self.Model.process_data(band_width, rects)
        if not step:
            self.Model.solve()
        else:
            self.steps = 0

    def view_to_model_step(self):
        T = self.Model.get_T()
        if self.steps < T:
            self.Model.solve_step()
            self.steps += 1
            if self.steps == T:
                self.View.execute()
        else:
            self.View.appendStringToLog("You cannot do any more steps, press \"Finish\"")
    
    def view_to_model_finish(self):
        T = self.Model.get_T()
        print(f"Finish. T={T}, steps={self.steps}, diff={T-self.steps}")
        if self.steps != T:
            self.Model.solve_step(T - self.steps)
            self.steps = T

    def model_to_view(self, population):
        self.View.receive_population(population)
        self.model_log()

    def get_band_width(self):
        return self.Model.get_band_width()
