from PySide6.QtWidgets import QDialog

from .generalsettings_ui import Ui_generalSettings
from widgets.trussview.graphicsview import TrussWidget
from utils.saveopen import SavedTruss


class GeneralSettings(QDialog):
    """Application general settings."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.ui = Ui_generalSettings()
        self.ui.setupUi(self)
        self.loadCurrentSettings()

        # set up slots
        self.ui.applyButton.pressed.connect(self.applySettings)
        self.ui.cancelButton.pressed.connect(self.cancel)

    def parentWidget(self) -> TrussWidget | None:
        return super().parentWidget()

    def applySettings(self) -> None:
        parent = self.parentWidget()
        parent.general_settings["zoom_sensitivity"] = self.ui.zoomSensitiviySpinBox.value(
        )
        parent.general_settings["zoom_step"] = self.ui.zoomStepSpinBox.value()
        parent.general_settings["pan_button"] = self.ui.panButtonSelection.currentText(
        )
        self.close()
        SavedTruss.save_general_settings(parent.general_settings)

    def cancel(self) -> None:
        self.close()

    def loadCurrentSettings(self) -> None:
        saved_settings = SavedTruss.get_general_settings()

        # do this incase new setting are added that arent in the users version
        self.ui.zoomSensitiviySpinBox.setValue(
            saved_settings["zoom_sensitivity"])
        self.ui.zoomStepSpinBox.setValue(saved_settings["zoom_step"])
        self.ui.panButtonSelection.setCurrentText(saved_settings["pan_button"]
                                                  )
