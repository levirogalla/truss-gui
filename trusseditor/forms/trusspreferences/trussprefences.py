from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QDialog

from .trusspreferences_ui import Ui_trussPreferences
from ..colorpicker.colorpicker import ColorPicker
from ...trusswidget2 import TrussWidget
from ...saveopen import DEFAULT_VIEW_PREFERENCES


class TrussPreferences(QDialog):
    """Class for truss view preferences dialog."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.ui = Ui_trussPreferences()
        self.ui.setupUi(self)
        self.joint_color = (0, 0, 0)
        self.joint_focused_color = (0, 0, 0)
        self.member_color = (0, 0, 0)
        self.force_color = (0, 0, 0)
        self.support_color = (0, 0, 0)
        self.loadCurrentSettings()

        # set up slots
        self.ui.applyButton.pressed.connect(self.applySettings)
        self.ui.resetButton.pressed.connect(self.resetSettings)

    def parentWidget(self) -> TrussWidget | None:
        return super().parentWidget()

    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:
        clicked_widget = self.childAt(a0.pos())
        color = None
        if clicked_widget == self.ui.supportColorWidget:
            color = ColorPicker.getColorInRGB(self)
            a0.accept()
            self.ui.supportColorWidget.setStyleSheet(
                f"background-color: rgb{color}")
            self.support_color = color
        if clicked_widget == self.ui.forceColorWidget:
            color = ColorPicker.getColorInRGB(self)
            a0.accept()
            self.ui.forceColorWidget.setStyleSheet(
                f"background-color: rgb{color}")
            self.force_color = color
        if clicked_widget == self.ui.memberColorWidget:
            color = ColorPicker.getColorInRGB(self)
            a0.accept()
            self.ui.memberColorWidget.setStyleSheet(
                f"background-color: rgb{color}")
            self.member_color = color
        if clicked_widget == self.ui.jointColorWidget:
            color = ColorPicker.getColorInRGB(self)
            a0.accept()
            self.ui.jointColorWidget.setStyleSheet(
                f"background-color: rgb{color}")
            self.joint_color = color
        if clicked_widget == self.ui.jointFocusedColorWidget:
            color = ColorPicker.getColorInRGB(self)
            self.ui.jointFocusedColorWidget.setStyleSheet(
                f"background-color: rgb{color}")
            self.joint_focused_color = color

            a0.accept()

        return super().mouseDoubleClickEvent(a0)

    def loadCurrentSettings(self) -> None:
        """Loads the current truss settings onto the dialog."""
        settings = self.parentWidget().truss_view_preferences

        self.joint_color = settings['joint_color']
        self.ui.jointColorWidget.setStyleSheet(
            f"background-color: rgb{settings['joint_color']}"
        )
        self.joint_focused_color = settings['joint_focused_color']
        self.ui.jointFocusedColorWidget.setStyleSheet(
            f"background-color: rgb{settings['joint_focused_color']}"
        )
        self.member_color = settings['member_color']
        self.ui.memberColorWidget.setStyleSheet(
            f"background-color: rgb{settings['member_color']}"
        )
        self.force_color = settings['force_color']
        self.ui.forceColorWidget.setStyleSheet(
            f"background-color: rgb{settings['force_color']}"
        )
        self.support_color = settings['support_color']
        self.ui.supportColorWidget.setStyleSheet(
            f"background-color: rgb{settings['support_color']}"
        )

        self.ui.sizeDoubleSpinBox.setValue(settings["support_size"])
        self.ui.radiusDoubleSpinBox.setValue(settings["joint_radius"])
        self.ui.widthDoubleSpinBox.setValue(settings["member_size"])
        self.ui.scaleFactorDoubleSpinBox.setValue(settings["scale_factor"])
        self.ui.headLengthDoubleSpinBox.setValue(settings["force_head_length"])
        self.ui.headWidthDoubleSpinBox.setValue(settings["force_head_width"])

    def applySettings(self) -> None:
        """Applys the new truss settings to the truss."""
        parent = self.parentWidget()
        parent.truss_view_preferences["support_color"] = self.support_color
        parent.truss_view_preferences["force_color"] = self.force_color
        parent.truss_view_preferences["member_color"] = self.member_color
        parent.truss_view_preferences["joint_color"] = self.joint_color
        parent.truss_view_preferences["joint_focused_color"] = self.joint_focused_color

        parent.truss_view_preferences["support_size"] = self.ui.sizeDoubleSpinBox.value(
        )
        parent.truss_view_preferences["joint_radius"] = self.ui.radiusDoubleSpinBox.value(
        )
        parent.truss_view_preferences["member_size"] = self.ui.widthDoubleSpinBox.value(
        )
        parent.truss_view_preferences["scale_factor"] = self.ui.scaleFactorDoubleSpinBox.value(
        )
        parent.truss_view_preferences["force_head_length"] = self.ui.headLengthDoubleSpinBox.value(
        )
        parent.truss_view_preferences["force_head_width"] = self.ui.headWidthDoubleSpinBox.value(
        )

        self.parentWidget().loadTrussWidgetFromMesh(False)

        self.close()

    def resetSettings(self) -> None:
        """Resets truss settings to default."""
        self.parentWidget().resetViewSettings()
        self.loadCurrentSettings()
        print(self.parentWidget().truss_view_preferences)
        self.update()
