import sys

from mainwindow.mainwindow import MainWindow
from PyQt6.QtWidgets import QApplication, QMessageBox


def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.setWindowTitle("Truss Maker")
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Truss Maker Crashed", str(e))


if __name__ == "__main__":
    main()
