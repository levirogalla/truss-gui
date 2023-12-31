from PySide6.QtWidgets import QFrame

from .startpage_ui import Ui_StartPage


class StartPage(QFrame):
    """Class for optimization window dialog."""

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_StartPage()
        self.ui.setupUi(self)
        self.main_window = None

    def set_main_window(self, main_window) -> None:
        self.main_window = main_window

        self.ui.newButton.pressed.connect(main_window.handleCreateNewTab)
        self.ui.openButton.pressed.connect(main_window.handleOpenTruss)
