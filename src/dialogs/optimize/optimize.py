import copy
import os

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from PySide6.QtCore import QTimer, QThread, Signal, Qt
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from trussty import Mesh

from torch import optim

from .optimize_ui import Ui_Dialog
from widgets.trussview.graphicsview import TrussWidget
from utils.saveopen import SavedTruss


class OptimizeDialog(QDialog):
    """Class for optimization window dialog."""

    def __init__(self, parent: TrussWidget) -> None:
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.loadSettings()

        # slots
        self.ui.applySettingsButton.pressed.connect(self.applySettings)
        self.ui.resetSettingsButton.pressed.connect(self.resetSettings)
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
        self.training_thread.no_optimizer_parms_error.connect(self.showError)

    # redefine for type hints
    def parentWidget(self) -> TrussWidget | None:
        return super().parentWidget()

    def showError(self) -> None:
        QMessageBox.critical(
            self,
            "Optimization Error",
            "This is likely because all joints are fixed. Set a joints track grad attribute to True to fix this.",
        )

    def loadSettings(self) -> None:
        """Load current settings."""
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

    def applySettings(self) -> None:
        """Apply new settings to truss."""
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

    def selectPath(self) -> None:
        """Handels select path dialog for save path."""
        dialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        path = dialog.getExistingDirectory(caption="Select Save Path")
        self.ui.savePathSelection.setText(path)

    def startTraining(self) -> None:
        """Starts optimizing the truss on a new thread."""
        path = self.parentWidget().truss_optimization_settings["save_path"]
        if path is not None or not os.path.exists(str(path)):
            response = QMessageBox.critical(
                self, "No Save Path", "No save path was specified, the optimized truss will not be save.", QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort)
            if response == QMessageBox.StandardButton.Abort:
                return

        self.ui.progressBar.setMaximum(
            self.parentWidget().truss_optimization_settings["epochs"]
        )
        self.training_thread.start()
        self.training_timer.setInterval(
            int(1000 /
                self.parentWidget().truss_optimization_settings["frame_rate"])
        )
        self.training_timer.start()

    def updateTrainingData(self) -> None:
        """Updates truss optimization data."""
        self.axes.cla()
        self.new_truss.show(ax=self.axes)
        self.figure.canvas.draw_idle()
        self.ui.progressBar.setValue(
            self.new_truss.training_progress()
        )

    def resetSettings(self) -> None:
        """Resets optimization settings to default."""
        self.parentWidget().resetOptimizationSettings()
        self.loadSettings()
        self.update()
        self.applySettings()

    def handleFinishedTraining(self) -> None:
        """Handles finished training."""
        self.handleSave("final-")
        self.updateTrainingData()
        self.training_timer.stop()
        self.training_thread.terminate()

    def closeEvent(self, a0) -> None:
        self.handleStop()
        super().closeEvent(a0)

    def handleSave(self, optional_prefix="") -> None:
        """Handles saving the new truss to saved path."""

        optim_settings = self.parentWidget().truss_optimization_settings
        view_preferences = self.parentWidget().truss_view_preferences
        file_name = self.parentWidget().file.split("/")[-1]

        try:
            epoch = self.new_truss.training_progress()
            saved_truss = SavedTruss(
                copy.copy(self.new_truss), optim_settings, view_preferences)

            saved_truss.truss.delete_epochs_counter()

            if optim_settings["save_path"] is not None:
                saved_truss.save(
                    optim_settings["save_path"] + "/" + optional_prefix + str(epoch) + file_name)

        except FileNotFoundError as e:
            print(e)

    def handleStop(self) -> None:
        """Stops the training."""
        self.new_truss.stop_training()
        self.handleFinishedTraining()


class TrainThread(QThread):
    """Class for optimizing truss on seperate cpu thread."""
    finished = Signal()
    no_optimizer_parms_error = Signal()

    def __init__(self, truss: Mesh, settings: dict) -> None:
        super().__init__()
        self.settings = settings
        self.truss = truss
        if settings["optimizer"] == "SGD":
            self.optimizer = optim.SGD
        elif settings["optimizer"] == "Adam":
            self.optimizer = optim.Adam

    def run(self) -> None:

        try:
            settings = self.settings
            self.truss.optimize_cost(
                member_cost=settings["member_cost"],
                joint_cost=settings["joint_cost"],
                lr=settings["lr"],
                epochs=settings["epochs"],
                optimizer=self.optimizer,
                print_mesh=False,
                show_at_epoch=False,
                min_member_length=settings["min_member_length"],
                max_member_length=settings["max_member_length"],
                max_tensile_force=settings["max_tensile_force"],
                max_compresive_force=settings["max_compressive_force"],
                constriant_agression=settings["constraint_aggression"],
                progress_bar=True,
                show_metrics=False,
                update_metrics_interval=settings["update_metrics_interval"],
            )
            self.finished.emit()
        except ValueError as e:
            self.no_optimizer_parms_error.emit()
