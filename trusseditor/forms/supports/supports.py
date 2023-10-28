from typing import Callable

from PyQt6.QtWidgets import QWidget
from .supportAddForm_ui import Ui_addSupportForm


class SupportForm(QWidget):
    """Class for add support form."""

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

    def addSupport(self) -> None:
        """Handles adding support."""
        try:
            self.addSupportToGui(
                self.joints[self.ui.select_joint.currentText()], self.ui.select_type.currentText())
            self.destroySupportFormReference(self)
        except KeyError as error:
            print("Invalid Selection", error)

    def closeEvent(self, a0) -> None:
        self.destroySupportFormReference(self)
        return super().closeEvent(a0)
