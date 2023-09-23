
import sys
import typing

from pytruss import Support
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from ..circle import JointWidget
from .forceAddForm_ui import Ui_addForceForm
from typing import Callable


class ForceAddWidget(QWidget):
    def __init__(self, joints: set, selected_joint, destroyForceFormRefrence, addForceToGui: Callable) -> None:
        super().__init__(None)
        self.ui = Ui_addForceForm()
        self.ui.setupUi(self)
        self.joints = dict()
        for joint in joints:
            self.joints[f"{id(joint)}"] = joint
            self.ui.select_joint.addItem(str(id(joint)))
        self.ui.select_joint.setCurrentText(str(id(selected_joint)))
        self.ui.forceButton.clicked.connect(self.addForce)
        self.destroyForceFormReference = destroyForceFormRefrence
        self.addForceToGui = addForceToGui

    def addForce(self):
        try:
            self.addForceToGui(
                self.joints[self.ui.select_joint.currentText()],
                float(self.ui.x_component.text()),
                float(self.ui.y_component.text()))
            self.destroyForceFormReference(self)
        except KeyError as error:
            print("Invalid Selection", error)


class ArrowWidget(QWidget):
    FORCE_SCALE = 10
    FORCE_HEAD_LENGTH = 20
    FORCE_HEAD_WIDTH = 10

    def __init__(self, parent: QWidget, x_cord, y_cord, x_mag, y_mag) -> None:
        super().__init__(parent)
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.x_mag = x_mag
        self.y_mag = y_mag

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 1)
        painter.setPen(pen)

        slope = (self.y_mag/self.x_mag+1e-10)
        perpendicular_slope = -(1/slope)

        head_x = self.x_cord
        head_y = self.y_cord

        tail_start_x = head_x - self.x_mag
        tail_start_y = head_y - self.y_mag
        tail_end_x = head_x - (1/slope)*self.FORCE_HEAD_LENGTH
        tail_end_y = head_y - slope*self.FORCE_HEAD_LENGTH

        painter.drawLine(int(tail_start_x), int(tail_start_y),
                         int(tail_end_x), int(tail_end_y))
