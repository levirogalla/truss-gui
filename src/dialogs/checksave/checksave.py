from typing import Callable

from PyQt6.QtWidgets import QDialog

from .checksave_ui import Ui_Changes


class CheckSaveDialog(QDialog):
    """Class for check save from."""

    def __init__(self, parent, saveFunc: Callable, dontSaveFunc: Callable, cancelFunc: Callable) -> None:
        super().__init__(parent)
        self.ui = Ui_Changes()
        self.ui.setupUi(self)
        self.saveFunc = saveFunc
        self.dontSaveFunc = dontSaveFunc
        self.cancelFunc = cancelFunc

        # set up slots
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.dontSaveButton.clicked.connect(self.dontSave)
        self.ui.cancelButton.clicked.connect(self.cancel)

    def save(self) -> None:
        """Handles user saving the closed truss."""
        self.saveFunc()
        self.dontSaveFunc()
        self.accept()

    def dontSave(self) -> None:
        """Doesn't save the closed truss."""
        self.dontSaveFunc()
        self.accept()

    def cancel(self) -> None:
        """Doesn't close or save the truss."""
        self.cancelFunc()
        self.accept()
