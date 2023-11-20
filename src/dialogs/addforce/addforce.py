from typing import Callable

from PyQt6.QtWidgets import QDialog, QMessageBox
from .addforce_ui import Ui_addForceForm
from pytruss import Force, Joint


class AddForceDialog(QDialog):
    """Class for add force form."""

    def __init__(self, joints: set[Joint], selected_joint: Joint) -> None:
        super().__init__(None)
        self.ui = Ui_addForceForm()
        self.ui.setupUi(self)
        self.joints = dict()
        for joint in joints:
            self.joints[f"{id(joint)}"] = joint
            self.ui.select_joint.addItem(str(id(joint)))
        self.ui.select_joint.setCurrentText(str(id(selected_joint)))
        self.ui.forceButton.clicked.connect(self.close)
        self.selected_joint = selected_joint

    @staticmethod
    def get_force(joints: set[Joint], selected_joint: Joint) -> Force | None:
        dialog = AddForceDialog(joints, selected_joint)
        dialog.exec()
        try:
            x_comp = float(dialog.ui.x_component.text())
            y_comp = float(dialog.ui.y_component.text())
            joint = dialog.joints[dialog.ui.select_joint.currentText()]
            force = Force(joint, x_comp, y_comp)
        except Exception as error:
            print("Invalid Selection", error)
            return None

        return force