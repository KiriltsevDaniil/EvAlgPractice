# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from datetime import datetime

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QPushButton, QGraphicsView, QGraphicsScene, QFileDialog, \
     QCheckBox, QProgressBar, QPlainTextEdit, QTreeView, QSystemTrayIcon, QSpinBox, QLineEdit, \
     QToolButton, QScrollArea, QSizePolicy, QFrame, QVBoxLayout, QHBoxLayout, QLabel # for Collapsible Box
from PySide2.QtGui import QRegExpValidator, QIcon, QPen, QBrush
from PySide2.QtCore import QFile, QRegExp, QPoint, Qt
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader

from CollapsibleBox import CollapsibleBox
from VariableLine import VariableLine



class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()
        appIcon = QIcon("icon3.png")
        self.setWindowIcon(appIcon)
        self.inExecution = False
        VarTest ={'T': 15, 'B': 13, 'C': 4, 'A': 15, 'D': 13, 'E': 4, 'F': 15, 'G': 13, 'H': 4}
        self.setVariablesBox(VarTest)
        PopTest = {1: [1, 2, 0, 0, True], 2: [2, 2, 0, 0], 3: [31, 22, 0, 0], 4: [31, 22, 0, 0], 5: [1123, 32, 0, 0],
                   6: [2571, 2572472, 0, 0], 7: [12572, 4372, 0, 0], 8: [1251, 152, 0, 0], 9: [1241, 1242, 0, 0], 10: [141, 42, 0, 0]}
        self.setPopulationBox(PopTest)
        self.Canvas = QGraphicsScene()
        self.CanvasView.setScene(self.Canvas)
        self.drawTest()
        self.DrawField = QGraphicsScene()
        self.DrawFieldView.setScene(self.DrawField)
        self.drawMut()

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
        self.MutBtn = self.findChild(QPushButton, 'MutBtn')
        self.TrayBtn = self.findChild(QPushButton, 'TrayBtn')
        self.StepBtn = self.findChild(QPushButton, 'StepBtn')
        self.RunBtn = self.findChild(QPushButton, 'RunBtn')
        self.StepBox = self.findChild(QCheckBox, 'StepBox')
        self.PopulationBox = self.findChild(QScrollArea, 'PopulationBox')
        self.VariablesBox = self.findChild(QScrollArea, 'VariablesBox')

        # Add functionality
        self.ExitBtn.clicked.connect(self.close)
        self.TrayBtn.clicked.connect(self.showMinimized)
        self.HelpBtn.clicked.connect(self.help)
        self.MutBtn.clicked.connect(self.mutationfunc)
        self.RunBtn.clicked.connect(self.testfunc)
        self.StepBtn.clicked.connect(self.stepClicked)
        self.ImportBtn.clicked.connect(self.importFile)

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
        self.FirstDialog.NumSpinBox.setMinimum(1)
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
        # Set Mutation illustration
        #
        path = os.fspath(Path(__file__).resolve().parent / "MutationWindow.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.MutationWindow = loader.load(ui_file, self)
        ui_file.close()

        self.DrawFieldView = self.MutationWindow.findChild(QGraphicsView, 'DrawField')
        self.MutationWindow.DrawBtn = self.MutationWindow.findChild(QPushButton, 'DrawBtn')
        self.MutationWindow.DrawBtn.clicked.connect(self.drawMut)
        self.MutationWindow.CloseBtn = self.MutationWindow.findChild(QPushButton, 'CloseBtn')
        self.MutationWindow.CloseBtn.clicked.connect(self.MutationWindow.reject)
        self.MutationWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.MutationWindow.hide()
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
        self.MutationWindow.move(250, 250)

    def appendStringToLog(self, line):
        Time = datetime.now()
        TimeForm = Time.strftime("%H:%M:%S")
        log = f"[{TimeForm}] {line}"
        self.LogConsole.appendPlainText(log)

    def clearLog(self):
        self.LogConsole.clear()

    def setProgress(self, percentage):
        self.ProgressBar.setValue(percentage)

    def stepClicked(self):
        self.appendStringToLog('step btn clicked')

    def setPopulationBox(self, data): # supposed to be a dict solNumber: list
        content = QWidget()
        self.PopulationBox.setWidget(content)
        self.PopulationBox.setWidgetResizable(True)
        vlay = QVBoxLayout(content)
        # "Root" layer
        for key in data:
            if len(data[key]) == 5 and data[key][4] == True:
                box = CollapsibleBox(f"Solution {key}", True) # Box represents "Root" and inner objects
            else:
                box = CollapsibleBox(f"Solution {key}")
            vlay.addWidget(box)
            lay = QVBoxLayout()
            # Inside layer
            labels = [QLabel(f"Length     {data[key][0]}"),
                      QLabel(f"Waste      {data[key][1]}"),
                      QLabel(f"Parents    {data[key][2]}, {data[key][3]}")]
            for j in range(3):
                labels[j].setStyleSheet("color : white; font: bold; margin-left: 10px;")
                labels[j].setAlignment(QtCore.Qt.AlignLeft)
                lay.addWidget(labels[j])
            box.setContentLayout(lay)
        vlay.addStretch()

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
            InLay = VariableLine(key, data[key], self.changeParam)
            lay.addLayout(InLay)
        box.setContentLayout(lay)
        vlay.addStretch()

    def changeParam(self, key, val):
        self.appendStringToLog(f"changeParam invoked: user wants to change this parameter: {key, val}")

    def help(self):
        self.HelpBtn.setEnabled(False)
        self.HelpDialog.exec_()
        self.HelpBtn.setEnabled(True)

    def mutationfunc(self):
        self.MutBtn.setEnabled(False)
        self.MutationWindow.exec_()
        self.MutBtn.setEnabled(True)

    def importFile(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Import', dir='.', filter='*.txt')

    def testfunc(self):
        self.RunBtn.setEnabled(False)
        if not self.inExecution: # start execution
            self.FirstDialog.WidthSpinBox.setValue(1)
            self.FirstDialog.NumSpinBox.setValue(1)
            if self.FirstDialog.exec_():
                self.SecondDialog.RectLine.clear()
                if self.SecondDialog.exec_():
                    RectWH = list(map(int, self.SecondDialog.RectLine.text().split()))
                    Width = self.FirstDialog.WidthSpinBox.value()
                    Num = self.FirstDialog.NumSpinBox.value()
                    if len(RectWH) == Num * 2 and 0 not in RectWH:
                        self.RunBtn.setEnabled(True)
                        if self.StepBox.isChecked():
                            self.StepBtn.setEnabled(True)
                            self.StepBtn.setFlat(False)
                        self.StepBox.setEnabled(False)
                        self.RunBtn.setText('Finish')
                        self.inExecution = True
                        #
                        # run alg
                        #
                        self.setProgress(50)
                    else:
                        self.appendStringToLog('Error: wrong Rectangle Line input')
        else: # stop execution
            self.RunBtn.setEnabled(True)
            self.StepBox.setEnabled(True)
            self.RunBtn.setText('Run')
            self.inExecution = False
            self.StepBtn.setFlat(True)
            self.StepBtn.setEnabled(False)
            self.setProgress(0)
        self.appendStringToLog('testfunc executed')
        self.RunBtn.setEnabled(True)

    def drawTest(self):
        self.Canvas.addRect(0, 0, 500, 100)
        self.Canvas.addRect(0, 50, 50, 50)


    def drawMut(self):
        x, y, w, h = 20, 10, 10, 10
        n=10
        for i in range(n):
            x+= 10
            y+= 5
            self.DrawField.addEllipse(x, y, w, h, pen=QPen(), brush=QBrush())

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    widget.setFixedSize(widget.size())
    sys.exit(app.exec_())
