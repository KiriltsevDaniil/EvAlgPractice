from PySide2.QtWidgets import QLabel, QHBoxLayout
from PySide2 import QtCore
from GUI.utility.SpinBox import SpinBox, DoubleSpinBox

class VariableLine(QHBoxLayout):
    def __init__(self, key, val, min, max, func, integer = True):
        super(VariableLine, self).__init__()
        self.key = key
        self.func = func
        self.label = QLabel(key)
        self.label.setStyleSheet("color : white; font: bold;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        if integer:
            self.spinbox = SpinBox(self.changeVal)
            self.spinbox.setStyleSheet("""
            QSpinBox {
            border: 0px solid #797979;
            font: bold;
            color: white;
            selection-background-color: #121828;
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
        else:
            self.spinbox = DoubleSpinBox(self.changeVal)
            self.spinbox.setStyleSheet("""
            QDoubleSpinBox {
            border: 0px solid #797979;
            font: bold;
            color: white;
            selection-background-color: #121828;
            }

            QDoubleSpinBox::up-button {
                width: 0;
                height: 0;
            }
            QDoubleSpinBox::down-button {
                width: 0;
                height: 0;
            }
            """)
        self.spinbox.setMinimum(min)
        self.spinbox.setMaximum(max)
        self.spinbox.setValue(val)
        self.addWidget(self.label)
        self.addWidget(self.spinbox)

    def changeVal(self):
        self.func(self.key, self.spinbox.value())
