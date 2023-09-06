import sys
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QPainterPath
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton


class RollerPin(QWidget):
    def __init__(self, parent, size) -> None:
        super().__init__(parent)
        self.r = size
        self.resize(self.r, self.r)

    def paintEvent(self, a0: QPaintEvent | None) -> None:

        # Create a QPainter object
        painter = QPainter(self)

        # Create a QPainterPath for the custom shape
        path = QPainterPath()

        # Define your custom shape here
        path.moveTo(self.r/2, 0)  # Move the pen to the starting point
        path.lineTo(0, self.r/2)  # Draw a line to a point
        path.lineTo(self.r, self.r/2)  # Draw another line
        path.lineTo(self.r/2, 0)  # Draw another line
        path.addEllipse(0, self.r/2, self.r/2, self.r/2)
        path.addEllipse(self.r/2, self.r/2, self.r/2, self.r/2)

        # Set the fill color
        painter.setBrush(Qt.GlobalColor.blue)

        # Draw the custom shape
        painter.drawPath(path)


def main():
    app = QApplication(sys.argv)
    window = RollerPin(None, 100)
    app.installEventFilter(window)
    window.setWindowTitle('Circle Example')
    window.setGeometry(100, 100, 400, 400)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
