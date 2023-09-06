import sys

from pytruss import Support
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from .circle import JointWidget


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
