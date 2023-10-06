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


class SupportForm(QWidget):
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
        self.selected_joint = selected_joint

    def addSupport(self):
        try:
            self.addSupportToGui(
                self.joints[self.ui.select_joint.currentText()], self.ui.select_type.currentText())
            self.destroySupportFormReference(self)
        except KeyError as error:
            print("Invalid Selection", error)

    def closeEvent(self, a0) -> None:
        self.destroySupportFormReference(self)
        return super().closeEvent(a0)
