import sys
import typing

from pytruss import Support
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QDialog
from .trusspreferences_ui import Ui_trussPreferences
from typing import Callable
from ..colorpicker.colorpicker import ColorPicker
from ...trusswidget2 import TrussWidget


class TrussPreferences(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.ui = Ui_trussPreferences()
        self.ui.setupUi(self)

        # set up slots

    def parentWidget(self) -> TrussWidget | None:
        return super().parentWidget()

    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:

        clicked_widget = self.childAt(a0.pos())
        color = None
        if clicked_widget == self.ui.supportColorWidget:
            color = ColorPicker.getColorInHEX(self)
            print(color)
            self.ui.supportColorWidget.setStyleSheet(
                f"background-color: #{color}")
        if clicked_widget == self.ui.forceColorWidget:
            color = ColorPicker.getColorInHEX(self)
            self.ui.forceColorWidget.setStyleSheet(
                f"background-color: #{color}")
            print(color)
        if clicked_widget == self.ui.memberColorWidget:
            color = ColorPicker.getColorInHEX(self)
            self.ui.memberColorWidget.setStyleSheet(
                f"background-color: #{color}")
            print(color)
        if clicked_widget == self.ui.jointColorWidget:
            color = ColorPicker.getColorInHEX(self)
            self.ui.jointColorWidget.setStyleSheet(
                f"background-color: #{color}")
            print(color)
        if clicked_widget == self.ui.jointFocusedColorWidget:
            color = ColorPicker.getColorInHEX(self)
            self.ui.jointFocusedColorWidget.setStyleSheet(
                f"background-color: #{color}")
            print(color)

        a0.accept()

        return super().mouseDoubleClickEvent(a0)
