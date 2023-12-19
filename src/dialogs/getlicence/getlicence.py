from PySide6.QtWidgets import QDialog


# from .trusswidget2 import JointItem, TrussWidget
from .getlicence_ui import Ui_LicenceDialog


class LicenceDialog(QDialog):
    """Class for edit joint coordinates dialog."""

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.ui = Ui_LicenceDialog()
        self.ui.setupUi(self)
        self.ui.okButton.pressed.connect(self.close)

    @staticmethod
    def getLicence(parent=None) -> str:
        """Shows dialog to ask the user for licence key and returns it."""
        dialog = LicenceDialog(parent)
        dialog.exec()
        text = dialog.ui.licence.toPlainText()
        return text
