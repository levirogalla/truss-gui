from PySide6.QtWidgets import QDialog
from .addforcequick_ui import Ui_AddForceDialog


class AddForceQuickDialog(QDialog):
    """Dialog for specifying force detail, the joint can not be selected with this dialog."""

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.ui = Ui_AddForceDialog()
        self.ui.setupUi(self)
        self.x_comp: float = None
        self.y_comp: float = None

        self.ui.doneButton.pressed.connect(self.handleDone)
        self.ui.cancelButton.pressed.connect(self.close)

    def handleDone(self) -> None:
        self.x_comp = float(self.ui.xComponent.text())
        self.y_comp = float(self.ui.yComponent.text())
        self.close()

    @staticmethod
    def get_components(parent) -> tuple[float, float]:
        """Return x_component, y_component entered in dialog."""
        dialog = AddForceQuickDialog(parent)
        dialog.exec()
        return (dialog.x_comp, dialog.y_comp)
