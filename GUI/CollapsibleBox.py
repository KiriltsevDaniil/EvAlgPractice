from PySide2.QtWidgets import QWidget, QToolButton, QScrollArea, QSizePolicy, QFrame, QVBoxLayout, QLabel # for Collapsible Box
from PySide2 import QtCore
from PySide2 import QtWidgets


class CollapsibleBox(QWidget):
    def __init__(self, title="", green=False, parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.rootBtn = QToolButton(text=title, checkable=True, checked=False)
        if green:
            self.rootBtn.setStyleSheet("QToolButton { border: none; color:green; font: bold; }")
        else:
            self.rootBtn.setStyleSheet("QToolButton { border: none; color:white; font: bold; }")
        self.rootBtn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.rootBtn.setArrowType(QtCore.Qt.DownArrow)
        self.rootBtn.pressed.connect(self.onPressed)

        self.Animation = QtCore.QParallelAnimationGroup(self)

        self.contentArea = QScrollArea(maximumHeight=0, minimumHeight=0)
        self.contentArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.contentArea.setFrameShape(QFrame.NoFrame)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.rootBtn)
        lay.addWidget(self.contentArea)

        self.Animation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        self.Animation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        self.Animation.addAnimation(QtCore.QPropertyAnimation(self.contentArea, b"maximumHeight"))

    def onPressed(self):
        checked = self.rootBtn.isChecked()
        self.rootBtn.setArrowType(QtCore.Qt.UpArrow if not checked else QtCore.Qt.DownArrow)
        self.Animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not checked
            else QtCore.QAbstractAnimation.Backward)
        self.Animation.start()

    def setContentLayout(self, layout, content_additional_height = 0):
        lay = self.contentArea.layout()
        del lay
        self.contentArea.setLayout(layout)
        self.collapsed_height = (self.sizeHint().height() - self.contentArea.maximumHeight())
        self.content_height = layout.sizeHint().height() + content_additional_height
        for i in range(self.Animation.animationCount()):
            animation = self.Animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(self.collapsed_height)
            animation.setEndValue(self.collapsed_height + self.content_height)

        content_animation = self.Animation.animationAt(self.Animation.animationCount() - 1)
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(self.content_height)
