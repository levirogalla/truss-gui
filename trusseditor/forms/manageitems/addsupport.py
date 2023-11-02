from PyQt6.QtWidgets import QDialog
from . addsupport_ui import Ui_AddSupportDialog


class AddSupport(QDialog):
    """Class for optimization window dialog."""

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.ui = Ui_AddSupportDialog()
        self.ui.setupUi(self)
        self.type: str = None

        self.ui.doneButton.pressed.connect(self.handleDone)
        self.ui.cancelButton.pressed.connect(self.close)

    def handleDone(self):
        self.type = self.ui.supportType.currentText()
        self.close()

    @staticmethod
    def getType(parent) -> str:
        dialog = AddSupport(parent)
        dialog.exec()
        return dialog.type
