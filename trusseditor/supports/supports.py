import sys
import typing

from pytruss import Support
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from ..circle import JointWidget
from .supportAddForm_ui import Ui_addSupportForm
from typing import Callable


class SupportWidget(QWidget):
    def __init__(self, parent, size, support: Support, jointWidget: JointWidget) -> None:
        super().__init__(parent)
        self.r = size
        self.resize(self.r, self.r)
        self.support = support
        self.stackUnder(jointWidget)
        self.jointWidget = jointWidget
        self.jointWidget.moved.connect(self.updateLocation)

    def updateLocation(self):
        x = self.support.joint.x_coordinate - self.r/2
        y = self.parent().mapCartesian(self.support.joint.y_coordinate)
        self.move(int(x), int(y))


class RollerPin(SupportWidget):
    def __init__(self, parent, size, support, jointWidget: JointWidget) -> None:
        super().__init__(parent, size, support, jointWidget)

    def paintEvent(self, a0: QPaintEvent | None) -> None:

        # Create a QPainter object
        painter = QPainter(self)

        # Create a QPainterPath for the custom shape
        path = QPainterPath()

        # Define your custom shape here
        path.moveTo(self.r/2, 0)  # Move the pen to the starting point
        path.lineTo(0, self.r/2)  # Draw a line to a point
        path.lineTo(self.r, self.r/2)  # Draw another line
        path.lineTo(self.r/2, 0)  # Draw another line
        path.addEllipse(0, self.r/2, self.r/2, self.r/2)
        path.addEllipse(self.r/2, self.r/2, self.r/2, self.r/2)

        # Set the fill color
        painter.setBrush(Qt.GlobalColor.blue)

        # Draw the custom shape
        painter.drawPath(path)


class FixedPin(SupportWidget):
    def __init__(self, parent, size, support, jointWidget: JointWidget) -> None:
        super().__init__(parent, size, support, jointWidget)

    def paintEvent(self, a0: QPaintEvent | None) -> None:

        # Create a QPainter object
        painter = QPainter(self)

        # Create a QPainterPath for the custom shape
        path = QPainterPath()

        # Define your custom shape here
        path.moveTo(self.r/2, 0)  # Move the pen to the starting point
        path.lineTo(0, self.r/2)  # Draw a line to a point
        path.lineTo(self.r, self.r/2)  # Draw another line
        path.lineTo(self.r/2, 0)  # Draw another line
        path.moveTo(0, self.r/2)
        path.lineTo(0, self.r)
        path.lineTo(self.r, self.r)
        path.lineTo(self.r, self.r/2)

        # Set the fill color
        painter.setBrush(Qt.GlobalColor.blue)

        # Draw the custom shape
        painter.drawPath(path)


class SupportAddWidget(QWidget):
    def __init__(self, joints: set, selected_joint, destroySupportFormRefrence: Callable, addSupportToGui: Callable) -> None:
        super().__init__(None)
        self.ui = Ui_addSupportForm()
        self.ui.setupUi(self)
        self.joints = dict()
        for joint in joints:
            self.joints[f"{id(joint)}"] = joint
            self.ui.select_joint.addItem(str(id(joint)))
        self.ui.select_joint.setCurrentText(str(id(selected_joint)))
        self.ui.supportButton.clicked.connect(self.addSupport)
        self.destroySupportFormReference = destroySupportFormRefrence
        self.addSupportToGui = addSupportToGui

    def addSupport(self):
        try:
            self.addSupportToGui(
                self.joints[self.ui.select_joint.currentText()], self.ui.select_type.currentText())
            self.destroySupportFormReference(self)
        except KeyError as error:
            print("Invalid Selection", error)
