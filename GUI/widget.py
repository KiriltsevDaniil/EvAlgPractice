# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from datetime import datetime

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QPushButton, QGraphicsView, QGraphicsScene, \
     QCheckBox, QProgressBar, QPlainTextEdit, QTreeView, QSystemTrayIcon, QSpinBox, QLineEdit, \
     QToolButton, QScrollArea, QSizePolicy, QFrame, QVBoxLayout, QHBoxLayout, QLabel # for Collapsible Box
from PySide2.QtGui import QRegExpValidator, QIcon
from PySide2.QtCore import QFile, QRegExp, QPoint
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader

from CollapsibleBox import CollapsibleBox

class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()
        appIcon = QIcon("icon3.png")
        self.setWindowIcon(appIcon)
        self.inExecution = False
        self.setVariablesBox()
        self.setPopulationBox()
        self.Canvas = QGraphicsScene()
        self.CanvasView.setScene(self.Canvas)

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
        self.HelpBtn.clicked.connect(self.help)
        self.RunBtn.clicked.connect(self.testfunc)
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

    def appendStringToLog(self, str):
        Time = datetime.now()
        TimeForm = Time.strftime("%H:%M:%S")
        log = f"[{TimeForm}] {str}"
        self.LogConsole.appendPlainText(log)

    def clearLog(self):
        self.LogConsole.clear()

    def setProgress(self, percentage):
        self.ProgressBar.setValue(percentage)

    def stepClicked(self):
        self.appendStringToLog('step btn clicked')

    def setPopulationBox(self):
        content = QWidget()
        self.PopulationBox.setWidget(content)
        self.PopulationBox.setWidgetResizable(True)
        vlay = QVBoxLayout(content)
        # "Root" layer
        for i in range(1, 11):
            if i == 1:
                box = CollapsibleBox(f"Solution {i}", True) # Box represents "Root" and inner objects
            else:
                box = CollapsibleBox(f"Solution {i}")
            vlay.addWidget(box)
            lay = QVBoxLayout()
            # Inside layer
            labels = [QLabel(f"Width      {2}"),
                      QLabel(f"Waste      {14}"),
                      QLabel(f"Parents    {1}, {4}")]
            for j in range(3):
                labels[j].setStyleSheet("color : white; font: bold; margin-left: 10px;")
                labels[j].setAlignment(QtCore.Qt.AlignLeft)
                lay.addWidget(labels[j])
            box.setContentLayout(lay)
        vlay.addStretch()

    def setVariablesBox(self):
        content = QWidget()
        self.VariablesBox.setWidget(content)
        self.VariablesBox.setWidgetResizable(True)
        vlay = QVBoxLayout(content)
        # "Root" layer
        for i in range(1):
            title = "GA parameters"
            if i == 1:
                title = "Other parameters"
            box = CollapsibleBox(title) # Box represents "Root" and inner objects
            vlay.addWidget(box)
            lay = QVBoxLayout()
            # Inside layer
            for j in range(1, 3):
                InLay = QHBoxLayout()
                label = QLabel(f"Data {j}")
                label.setStyleSheet("color : white; font: bold;")
                label.setAlignment(QtCore.Qt.AlignCenter)
                spinbox = QSpinBox()
                spinbox.setStyleSheet("""
                QSpinBox {
                border: 0px solid #797979;
                font: bold;
                color: white;
                }

                QSpinBox::up-button {
                    width: 0;
                    height: 0;
                }
                QSpinBox::down-button {
                    width: 0;
                    height: 0;
                }
                """)
                InLay.addWidget(label)
                InLay.addWidget(spinbox)
                lay.addLayout(InLay)
            box.setContentLayout(lay)
        vlay.addStretch()


    def help(self):
        self.HelpDialog.exec_()

    def testfunc(self):
        if not self.inExecution: # start execution
            if self.FirstDialog.exec_():
                self.SecondDialog.RectLine.clear()
                if self.SecondDialog.exec_():
                    self.FirstDialog.WidthSpinBox.value()
                    if self.StepBox.isChecked():
                        self.StepBtn.setEnabled(True)
                        self.StepBtn.setFlat(False)
                    self.StepBox.setEnabled(False)
                    self.RunBtn.setText('Finish')
                    self.inExecution = True
                    # run alg
                    self.setProgress(50)
        else: # stop execution
            self.StepBox.setEnabled(True)
            self.RunBtn.setText('Run')
            self.inExecution = False
            self.StepBtn.setFlat(True)
            self.StepBtn.setEnabled(False)
            self.setProgress(0)
        self.appendStringToLog('testfunc executed')


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
#    widget.setFixedSize(widget.size())
    sys.exit(app.exec_())
