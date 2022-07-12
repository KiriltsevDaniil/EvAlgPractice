# This Python file uses the following encoding: utf-8
import os
import sys
from pathlib import Path
from datetime import datetime
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QGraphicsView, QGraphicsScene, \
     QCheckBox, QProgressBar, QPlainTextEdit, QSpinBox, QLineEdit, QFileDialog, \
     QScrollArea, QSizePolicy, QFrame, QVBoxLayout, QHBoxLayout, QLabel # for Collapsible Box
from PySide2.QtGui import QRegExpValidator, QIcon, QPen, QBrush, QColor
from PySide2.QtCore import QFile, QRegExp, QPoint, Qt, QFile
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from random import randint, random

from GUI.CollapsibleBox import CollapsibleBox
from GUI.VariableLine import VariableLine
from GUI.SolutionBtn import SolutionButton

class Widget(QWidget):
    def __init__(self, testing=False):
        super(Widget, self).__init__()

        self.load_ui()
        appIcon = QIcon("icon3.png")
        self.setWindowIcon(appIcon)
        self.inExecution = False
        self.testing = testing
        self.send_data = None
        self.finish = None
        self.step = None
        self.get_band_width = None
        self.change_parameter = None
        self.Canvas = QGraphicsScene()
        self.CanvasView.setScene(self.Canvas)
        if testing:
            VarTest ={'T': 15, 'B': 13, 'C': 4, 'A': 15, 'D': 13, 'E': 4, 'F': 15, 'G': 13, 'H': 4}
            self.setVariablesBox(VarTest)
            PopTest = {1: [1, 2, 0, 0, True], 2: [2, 2, 0, 0], 3: [31, 22, 0, 0], 4: [31, 22, 0, 0], 5: [1123, 32, 0, 0],
                    6: [2571, 2572472, 0, 0], 7: [12572, 4372, 0, 0], 8: [1251, 152, 0, 0], 9: [1241, 1242, 0, 0], 10: [141, 42, 0, 0]}
            self.setPopulationBox(PopTest)
            self.drawTest()

    def load_ui(self):
        #
        # Set Main Window UI
        #
        loader = QUiLoader()
        loader.registerCustomWidget(CollapsibleBox)
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
        # Get Main Window UI elements
        self.CanvasView = self.findChild(QGraphicsView, 'Canvas')
        self.StepBox = self.findChild(QCheckBox, 'StepBox')
        self.ProgressBar = self.findChild(QProgressBar, 'progressBar')
        self.LogConsole = self.findChild(QPlainTextEdit, 'LogConsole')
        self.ImportBtn = self.findChild(QPushButton, 'ImportBtn')
        self.HelpBtn = self.findChild(QPushButton, 'HelpBtn')
        self.ExitBtn = self.findChild(QPushButton, 'ExitBtn')
        self.TrayBtn = self.findChild(QPushButton, 'TrayBtn')
        self.StepBtn = self.findChild(QPushButton, 'StepBtn')
        self.RunBtn = self.findChild(QPushButton, 'RunBtn')
        self.StepBox = self.findChild(QCheckBox, 'StepBox')
        self.PopulationBox = self.findChild(QScrollArea, 'PopulationBox')
        self.VariablesBox = self.findChild(QScrollArea, 'VariablesBox')

        # Add functionality
        self.ExitBtn.clicked.connect(self.close)
        self.TrayBtn.clicked.connect(self.showMinimized)
        self.ImportBtn.clicked.connect(self.importFile)
        self.HelpBtn.clicked.connect(self.help)
        self.RunBtn.clicked.connect(self.execute)
        self.StepBtn.clicked.connect(self.stepClicked)
        #
        # Set First Dialog UI
        #
        path = os.fspath(Path(__file__).resolve().parent / "FirstDialog.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.FirstDialog = loader.load(ui_file, self)
        ui_file.close()

        self.FirstDialog.NextBtn = self.FirstDialog.findChild(QPushButton, 'NextBtn')
        self.FirstDialog.CancelBtn = self.FirstDialog.findChild(QPushButton, 'CancelBtn')
        self.FirstDialog.WidthSpinBox = self.FirstDialog.findChild(QSpinBox, 'WidthSpinBox')
        self.FirstDialog.NumSpinBox = self.FirstDialog.findChild(QSpinBox, 'NumSpinBox')
        # Add functionality
        self.FirstDialog.CancelBtn.clicked.connect(self.FirstDialog.reject)
        self.FirstDialog.NextBtn.clicked.connect(self.FirstDialog.accept)
        self.FirstDialog.WidthSpinBox.setMinimum(1)
        self.FirstDialog.NumSpinBox.setMinimum(2)
        self.FirstDialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.FirstDialog.hide()
        #
        # Set Second Dialog UI
        #
        path = os.fspath(Path(__file__).resolve().parent / "SecondDialog.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.SecondDialog = loader.load(ui_file, self)
        ui_file.close()

        self.SecondDialog.NextBtn = self.SecondDialog.findChild(QPushButton, 'NextBtn')
        self.SecondDialog.CancelBtn = self.SecondDialog.findChild(QPushButton, 'CancelBtn')
        self.SecondDialog.RectLine = self.SecondDialog.findChild(QLineEdit, 'RectLine')
        # Add functionality
        self.SecondDialog.CancelBtn.clicked.connect(self.SecondDialog.reject)
        self.SecondDialog.NextBtn.clicked.connect(self.SecondDialog.accept)
        self.SecondDialog.RectLine.setValidator(QRegExpValidator(QRegExp("[0-9 ]+")))
        self.SecondDialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.SecondDialog.hide()
        #
        # Help Dialog UI
        #
        path = os.fspath(Path(__file__).resolve().parent / "help.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.HelpDialog = loader.load(ui_file, self)
        ui_file.close()
        self.HelpDialog.CloseBtn = self.HelpDialog.findChild(QPushButton, 'CloseBtn')
        self.HelpDialog.CloseBtn.clicked.connect(self.HelpDialog.reject)
        self.HelpDialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.HelpDialog.hide()
        #
        # Other stuff
        #
        self.setWindowTitle('Stock problem')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.StepBtn.setEnabled(False)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()
        self.HelpDialog.move(250, 250)
        self.FirstDialog.move(250, 250)
        self.SecondDialog.move(250, 250)
    
    def drawTest(self):
        self.Canvas.addRect(0, 0, 500, 100)
        self.Canvas.addRect(0, 50, 50, 50)

    def appendStringToLog(self, line, timestamp = True):
        if timestamp:
            Time = datetime.now()
            TimeForm = Time.strftime("%H:%M:%S")
            log = f"[{TimeForm}] {line}"
            self.LogConsole.appendPlainText(log)
        else:
            self.LogConsole.appendPlainText(line)

    def clearLog(self):
        self.LogConsole.clear()

    def setProgress(self, percentage):
        self.ProgressBar.setValue(percentage)

    def setPopulationBox(self, populations): # list of populations
        content = QWidget()
        self.PopulationBox.setWidget(content)
        self.PopulationBox.setWidgetResizable(True)
        vlay = QVBoxLayout(content)
        # "Root" layer
        population_number = 0
        for population in populations:
            population_box = CollapsibleBox("Population {}".format(population_number))
            vlay.addWidget(population_box)
            population_lay = QVBoxLayout()
            
            solution_number = 1
            inner_height = 0
            
            for solution in population.get_population():
                if solution_number == 1:
                    solution_box = CollapsibleBox(f"Solution {solution_number}", SolutionButton(solution, self.draw_solution),True)
                else:
                    solution_box = CollapsibleBox(f"Solution {solution_number}", SolutionButton(solution, self.draw_solution))
                solution_lay = QVBoxLayout()
                parents = solution.get_parents()
                if parents is None:
                    parents = ['None', 'None']
                solution_labels = [QLabel(f"Length     {solution.get_length()}"),
                            QLabel(f"Waste      {solution.get_waste()}"),
                            QLabel(f"Parents:"),
                            QLabel(f"{parents[0]}"),
                            QLabel(f"{parents[1]}")]
                for j in range(5):
                    solution_labels[j].setStyleSheet("color : white; font: bold; margin-left: 10px;")
                    solution_labels[j].setAlignment(QtCore.Qt.AlignLeft)
                    solution_lay.addWidget(solution_labels[j])
                solution_box.setContentLayout(solution_lay)
                solution_number += 1
                inner_height += solution_box.content_height
                population_lay.addWidget(solution_box)

            population_number +=1
            population_box.setContentLayout(population_lay, inner_height)
        
        vlay.addStretch()

        self.draw_solution(populations[-1].get_fittest())

    def setVariablesBox(self, data): # supposed to be a dict string: val
        content = QWidget()
        self.VariablesBox.setWidget(content)
        self.VariablesBox.setWidgetResizable(True)
        vlay = QVBoxLayout(content)
        # "Root" layer
        title = "GA parameters"
        box = CollapsibleBox(title) # Box represents "Root" and inner objects
        vlay.addWidget(box)
        lay = QVBoxLayout()
        # Inside layer
        for key in data:
            InLay = VariableLine(key, data[key][0], data[key][1], data[key][2], self.changeParam, data[key][3])
            lay.addLayout(InLay)
        box.setContentLayout(lay)
        vlay.addStretch()

    def help(self):
        self.HelpBtn.setEnabled(False)
        self.HelpDialog.exec_()
        self.HelpBtn.setEnabled(True)

    def importFile(self):
        filename, _ = QFileDialog.getOpenFileName(parent=self, caption='Import', dir='.', filter='*.txt')
        if filename != '':
            file = open(filename, 'r')
            if file.closed:
                self.appendStringToLog('Error reading file')
                return
            values = list(map(int, file.readlines()[0].split()))
            RectWH = values[2:]
            Width = values[0]
            Num = values[1]
            if len(RectWH) == Num * 2 and 0 not in RectWH and all(Width >= i for i in RectWH[1::2]):
                self.RunBtn.setEnabled(True)
                self.appendStringToLog('data sent from a file')
                if self.StepBox.isChecked():
                    self.StepBtn.setEnabled(True)
                    self.StepBtn.setFlat(False)
                    self.StepBox.setEnabled(False)
                    self.RunBtn.setText('Finish')
                    self.inExecution = True
                    self.appendStringToLog("Step By Step")
                    self.send_data(Width, RectWH, True)
                else:
                    self.send_data(Width, RectWH)
            else:
                self.appendStringToLog('Error: wrong file input')

    def execute(self):
        self.RunBtn.setEnabled(False)
        if not self.inExecution: # start execution
            self.setProgress(0)
            self.FirstDialog.WidthSpinBox.setValue(1)
            self.FirstDialog.NumSpinBox.setValue(1)
            if self.FirstDialog.exec_():
                self.SecondDialog.RectLine.clear()
                if self.SecondDialog.exec_():
                    RectWH = list(map(int, self.SecondDialog.RectLine.text().split()))
                    Width = self.FirstDialog.WidthSpinBox.value()
                    Num = self.FirstDialog.NumSpinBox.value()
                    if len(RectWH) == Num * 2 and 0 not in RectWH and all(Width >= i for i in RectWH[1::2]):
                        self.RunBtn.setEnabled(True)
                        self.appendStringToLog('data sent')
                        if self.StepBox.isChecked():
                            self.StepBtn.setEnabled(True)
                            self.StepBtn.setFlat(False)
                            self.StepBox.setEnabled(False)
                            self.RunBtn.setText('Finish')
                            self.ImportBtn.setEnabled(False)
                            self.inExecution = True
                            self.appendStringToLog("Step By Step")
                            self.send_data(Width, RectWH, True)
                        else:
                            self.send_data(Width, RectWH)
                    else:
                        self.appendStringToLog('Error: wrong Rectangle Line input')
        else: # stop execution
            self.RunBtn.setEnabled(True)
            self.StepBox.setEnabled(True)
            self.RunBtn.setText('Run')
            self.RunBtn.setEnabled(False)
            self.ImportBtn.setEnabled(True)
            self.finish()
            self.inExecution = False
            self.StepBtn.setFlat(True)
            self.StepBtn.setEnabled(False)
            self.setProgress(0)
            self.appendStringToLog('finished')
        self.RunBtn.setEnabled(True)
    
    def stepClicked(self):
        self.step()

    def set_send_data(self, slot):
        self.send_data = slot
    
    def set_step(self, slot):
        self.step = slot
    
    def set_finish(self, slot):
        self.finish = slot
    
    def set_change_parameter(self, slot):
        self.change_parameter = slot
    
    def set_get_band_width(self, slot):
        self.get_band_width = slot
    
    def changeParam(self, key, val):
        self.appendStringToLog(f"User wants to change this parameter: {key, val}")
        self.change_parameter(key, val)

    def receive_population(self, populations):
        self.setProgress(100)
        self.setPopulationBox(populations)

    def draw_solution(self, solution):
        band_width = self.get_band_width()
        mlt = 10
        if band_width > solution.get_length():
            mlt = (3/4) / (band_width / self.CanvasView.height()) 
        else:
            mlt = (3/4) / (solution.get_length() / self.CanvasView.width())
        self.Canvas.clear()
        self.Canvas.addRect(0, 0, solution.get_length() * mlt, -band_width * mlt)
        self.Canvas.addLine(0, 0, solution.get_length() * mlt * 2, 0)
        self.Canvas.addLine(0, -band_width * mlt, solution.get_length() * mlt * 2, -band_width * mlt)
        for crd in solution.get_coordinates():
            random_brush = QBrush(QColor(randint(0, 255), randint(0, 255), randint(0, 255)))
            print(f"crd: x={crd.get_x() * mlt}, y={crd.get_y() * mlt}, width{crd.get_width() * mlt}, height{crd.get_height() * mlt}")
            self.Canvas.addRect(crd.get_x() * mlt, -(crd.get_y() * mlt), crd.get_width() * mlt, -(crd.get_height() * mlt), brush=random_brush)
        self.CanvasView.update()
            
        


if __name__=='__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    widget.setFixedSize(widget.size())
    sys.exit(app.exec_())
