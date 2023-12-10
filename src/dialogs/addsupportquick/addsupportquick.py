from PyQt6.QtWidgets import QDialog
from .addsupportquick_ui import Ui_AddSupportDialog


class AddSupportQuickDialog(QDialog):
    """Class for add support form. Does not allow for joint selection."""

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
    def get_type(parent) -> str:
        "Show dialog for and get the type for a support"
        dialog = AddSupportQuickDialog(parent)
        dialog.exec()
        return dialog.type
