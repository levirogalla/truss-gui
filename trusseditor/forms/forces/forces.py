from typing import Callable

from PyQt6.QtWidgets import QWidget
from .forceAddForm_ui import Ui_addForceForm


class ForceForm(QWidget):
    """Class for add force form."""

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
        self.selected_joint = selected_joint

    def addForce(self) -> None:
        """Handles adding the force."""
        try:
            self.addForceToGui(
                self.joints[self.ui.select_joint.currentText()],
                float(self.ui.x_component.text()),
                float(self.ui.y_component.text()))
            self.destroyForceFormReference(self)
        except KeyError as error:
            print("Invalid Selection", error)

    def closeEvent(self, a0) -> None:
        self.destroyForceFormReference(self)
        return super().closeEvent(a0)
