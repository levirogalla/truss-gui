import sys
import typing

from pytruss import Support
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QDialog, QFileDialog
from .optimize_ui import Ui_Dialog
from typing import Callable
from ...trusswidget2 import TrussWidget
from torch import optim


class OptimizeDialog(QDialog):
    def __init__(self, parent: TrussWidget) -> None:
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # slots
        self.ui.applySettingsButton.pressed.connect(self.applySettings)
        self.ui.selectPathButton.pressed.connect(self.selectPath)

    # redefine for type hints
    def parentWidget(self) -> TrussWidget | None:
        return super().parentWidget()

    def applySettings(self):
        parent = self.parentWidget()

        # try converting input to proper type otherwise clear the input
        try:
            parent.truss_optimization_settings["member_cost"] = float(
                self.ui.memberCostLineEdit.text()
            )
        except ValueError as e:
            print(e)
            self.ui.memberCostLineEdit.clear()

        try:
            parent.truss_optimization_settings["joint_cost"] = float(
                self.ui.jointCostLineEdit.text()
            )
        except ValueError as e:
            print(e)
            self.ui.jointCostLineEdit.clear()

        try:
            parent.truss_optimization_settings["lr"] = float(
                self.ui.learningRateLineEdit.text()
            )
        except ValueError as e:
            print(e)
            self.ui.learningRateLineEdit.clear()

        try:
            parent.truss_optimization_settings["epochs"] = float(
                self.ui.epochsSpinBox.text()
            )
        except ValueError as e:
            print(e)
            self.ui.epochsSpinBox.clear()

        try:
            if self.ui.optimizerComboBox.currentText() == "SGD":
                optimmizer = optim.SGD
            elif self.ui.optimizerComboBox.currentText() == "Adam":
                optimmizer = optim.Adam

            parent.truss_optimization_settings["optimizer"] = optimmizer
        except ValueError as e:
            print(e)
            self.ui.optimizerComboBox.setCurrentIndex(0)

        try:
            parent.truss_optimization_settings["min_member_length"] = float(
                self.ui.minMemberLenghtLineEdit.text()
            )
        except ValueError as e:
            print(e)
            self.ui.minMemberLenghtLineEdit.clear()

        try:
            parent.truss_optimization_settings["max_member_length"] = float(
                self.ui.maxMemberLengthLineEdit.text()
            )
        except ValueError as e:
            print(e)
            self.ui.maxMemberLengthLineEdit.clear()

        try:
            parent.truss_optimization_settings["max_tensile_force"] = float(
                self.ui.maxTensileForceLineEdit.text()
            )
        except ValueError as e:
            print(e)
            self.ui.maxTensileForceLineEdit.clear()

        try:
            parent.truss_optimization_settings["max_compressive_force"] = float(
                self.ui.maxCompressiveForceLineEdit.text()
            )
        except ValueError as e:
            print(e)
            self.ui.maxCompressiveForceLineEdit.clear()

        try:
            parent.truss_optimization_settings["constraint_aggression"] = float(
                self.ui.constraintAggressionLineEdit.text()
            )
        except ValueError as e:
            print(e)
            self.ui.constraintAggressionLineEdit.clear()

        try:
            parent.truss_optimization_settings["update_metrics_interval"] = float(
                self.ui.updateMetricsIntervalSpinBox.text()
            )
        except ValueError as e:
            print(e)
            self.ui.updateMetricsIntervalSpinBox.clear()

        try:
            parent.truss_optimization_settings["save_frequency"] = float(
                self.ui.saveFrequencySpinBox.text()
            )
        except ValueError as e:
            print(e)
            self.ui.saveFrequencySpinBox.clear()

        try:
            parent.truss_optimization_settings["save_path"] = self.ui.savePathSelection.text(
            )
        except ValueError as e:
            print(e)
            self.ui.savePathSelection.clear()

        print(parent.truss_optimization_settings)

    def selectPath(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        path = dialog.getExistingDirectory(caption="Select Save Path")
        self.ui.savePathSelection.setText(path)
