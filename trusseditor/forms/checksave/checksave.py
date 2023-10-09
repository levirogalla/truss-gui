import sys
import typing

from pytruss import Support
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QDialog
from .checksave_ui import Ui_Changes
from typing import Callable


class CheckSaveForm(QDialog):
    def __init__(self, parent, saveFunc: Callable, dontSaveFunc: Callable, cancelFunc: Callable) -> None:
        super().__init__(parent)
        self.ui = Ui_Changes()
        self.ui.setupUi(self)
        self.saveFunc = saveFunc
        self.dontSaveFunc = dontSaveFunc
        self.cancelFunc = cancelFunc

        # set up slots
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.dontSaveButton.clicked.connect(self.dontSave)
        self.ui.cancelButton.clicked.connect(self.cancel)

    def save(self):
        self.saveFunc()
        self.accept()

    def dontSave(self):
        self.dontSaveFunc()
        self.accept()

    def cancel(self):
        self.cancelFunc()
        self.accept()
