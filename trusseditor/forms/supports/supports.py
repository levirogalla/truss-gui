from typing import Callable

from PyQt6.QtWidgets import QDialog
from .supportAddForm_ui import Ui_addSupportForm
from pytruss import Support, Joint


class SupportForm(QDialog):
    """Class for add support form."""

    def __init__(self, joints: set[Joint], selected_joint: Joint) -> None:
        super().__init__(None)
        self.ui = Ui_addSupportForm()
        self.ui.setupUi(self)
        self.joints = dict()
        for joint in joints:
            self.joints[f"{id(joint)}"] = joint
            self.ui.select_joint.addItem(str(id(joint)))
        self.ui.select_joint.setCurrentText(str(id(selected_joint)))
        self.ui.supportButton.pressed.connect(self.close)
        self.selected_joint = selected_joint

    @staticmethod
    def get_support(joints: set[Joint], selected_joint: Joint) -> tuple[Joint, str]:
        dialog = SupportForm(joints, selected_joint)
        dialog.exec()
        try:
            support_type = dialog.ui.select_type.currentText()
            joint = dialog.joints[dialog.ui.select_joint.currentText()]
        except KeyError as error:
            print("Invalid Selection", error)
            return None
        return joint, support_type
