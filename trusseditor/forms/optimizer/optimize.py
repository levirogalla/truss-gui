import sys
import typing

from pytruss import Support
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QDialog
from .optimize_ui import Ui_Dialog
from typing import Callable


class OptimizeForm(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
