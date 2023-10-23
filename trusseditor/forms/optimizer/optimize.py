import sys
import typing

from pytruss import Support
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QDialog, QFileDialog
from .optimize_ui import Ui_Dialog
from typing import Callable
from ...trusswidget2 import TrussWidget, TrainThread, SavedTruss
from torch import optim
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import copy
import pickle


class OptimizeDialog(QDialog):
    def __init__(self, parent: TrussWidget) -> None:
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.loadSettings()

        # slots
        self.ui.applySettingsButton.pressed.connect(self.applySettings)
        self.ui.selectPathButton.pressed.connect(self.selectPath)
        # implement default settings
        self.ui.startButton.pressed.connect(self.startTraining)
        self.ui.saveButton.pressed.connect(self.handleSave)
        self.ui.stopButton.pressed.connect(self.handleStop)

        # add the figure to the ui
        self.figure = plt.figure()
        self.axes = plt.subplot()
        self.figure.add_axes(self.axes)
        self.new_truss = copy.deepcopy(parent.truss)
        self.new_truss.show(ax=self.axes)

        self.ui.trussPreview = FigureCanvasQTAgg(self.figure)
        self.ui.trussPreview.setObjectName("trussPreview")
        self.ui.verticalLayout_3.addWidget(self.ui.trussPreview)

        self.training_thread = TrainThread(
            self.new_truss, parent.truss_optimization_settings
        )
        self.training_timer = QTimer()
        self.training_timer.timeout.connect(self.updateTrainingData)
        self.training_thread.finished.connect(self.handleFinishedTraining)

    # redefine for type hints

    def parentWidget(self) -> TrussWidget | None:
        return super().parentWidget()

    def loadSettings(self):
        parent = self.parentWidget()

        self.ui.memberCostLineEdit.setText(
            str(parent.truss_optimization_settings["member_cost"])
        )
        self.ui.jointCostLineEdit.setText(
            str(parent.truss_optimization_settings["joint_cost"])
        )
        self.ui.learningRateLineEdit.setText(
            str(parent.truss_optimization_settings["lr"])
        )
        self.ui.epochsSpinBox.setValue(
            parent.truss_optimization_settings["epochs"]
        )
        self.ui.optimizerComboBox.setCurrentText(
            str(parent.truss_optimization_settings["optimizer"])
        )
        self.ui.minMemberLenghtLineEdit.setText(
            str(parent.truss_optimization_settings["min_member_length"])
        )
        self.ui.maxMemberLengthLineEdit.setText(
            str(parent.truss_optimization_settings["max_member_length"])
        )
        self.ui.maxTensileForceLineEdit.setText(
            str(parent.truss_optimization_settings["max_tensile_force"])
        )
        self.ui.maxCompressiveForceLineEdit.setText(
            str(parent.truss_optimization_settings["max_compressive_force"])
        )
        self.ui.constraintAggressionLineEdit.setText(
            str(parent.truss_optimization_settings["constraint_aggression"])
        )
        self.ui.updateMetricsIntervalSpinBox.setValue(
            parent.truss_optimization_settings["update_metrics_interval"]
        )
        self.ui.saveFrequencySpinBox.setValue(
            parent.truss_optimization_settings["save_frequency"]
        )
        self.ui.savePathSelection.setText(
            str(parent.truss_optimization_settings["save_path"])
        )
        self.ui.frameRateSpinBox.setValue(
            parent.truss_optimization_settings["frame_rate"]
        )

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
            parent.truss_optimization_settings["epochs"] = int(
                self.ui.epochsSpinBox.text()
            )
        except ValueError as e:
            print(e)
            self.ui.epochsSpinBox.clear()

        try:
            parent.truss_optimization_settings["optimizer"] = str(
                self.ui.optimizerComboBox.currentText()
            )
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
            parent.truss_optimization_settings["update_metrics_interval"] = int(
                self.ui.updateMetricsIntervalSpinBox.text()
            )
        except ValueError as e:
            print(e)
            self.ui.updateMetricsIntervalSpinBox.clear()

        try:
            parent.truss_optimization_settings["save_frequency"] = int(
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

        try:
            parent.truss_optimization_settings["frame_rate"] = int(
                self.ui.frameRateSpinBox.text()
            )
        except ValueError as e:
            print(e)
            self.ui.frameRateSpinBox.clear()

        print(parent.truss_optimization_settings)

    def selectPath(self):
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        path = dialog.getExistingDirectory(caption="Select Save Path")
        self.ui.savePathSelection.setText(path)

    def startTraining(self):
        print("starting")
        self.ui.progressBar.setMaximum(
            self.parentWidget().truss_optimization_settings["epochs"]
        )
        self.training_thread.start()
        self.training_timer.setInterval(
            int(1000 /
                self.parentWidget().truss_optimization_settings["frame_rate"])
        )
        self.training_timer.start()

    def updateTrainingData(self):
        self.axes.cla()
        self.new_truss.show(ax=self.axes)
        self.figure.canvas.draw_idle()
        self.ui.progressBar.setValue(
            self.new_truss.training_progress()
        )

    def handleFinishedTraining(self):
        self.updateTrainingData()
        self.training_timer.stop()
        self.training_thread.terminate()
        self.handleSave("final-")

    def closeEvent(self, a0) -> None:
        super().closeEvent(a0)

    def handleSave(self, optional_prefix=""):
        settings = self.parentWidget().truss_optimization_settings
        file_name = self.parentWidget().file.split("/")[-1]

        try:
            epoch = self.new_truss.training_progress()
            saved_truss = SavedTruss(
                copy.copy(self.new_truss), settings)

            saved_truss.truss.delete_epochs_counter()

            print(saved_truss.truss.__dict__)

            with open(settings["save_path"] + "/" + optional_prefix + str(epoch) + file_name, "wb") as f:
                pickle.dump(saved_truss, f)

        except Exception as e:
            print(e)

    def handleStop(self):
        print(NotImplemented)
