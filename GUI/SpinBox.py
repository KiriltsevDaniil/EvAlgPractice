from PySide2.QtWidgets import QSpinBox, QDoubleSpinBox
from PySide2.QtCore import Qt

class SpinBox(QSpinBox):
    def __init__(self, func):
        super(SpinBox, self).__init__()
        self.func = func
    def focusInEvent(self, event):
        self.val = self.value()
    def focusOutEvent(self, event):
        self.setValue(self.val)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.func()
            self.val = self.value()
        return super().keyPressEvent(event)

class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, func):
        super(DoubleSpinBox, self).__init__()
        self.func = func
    def focusInEvent(self, event):
        self.val = self.value()
    def focusOutEvent(self, event):
        self.setValue(self.val)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.func()
            self.val = self.value()
        return super().keyPressEvent(event)
