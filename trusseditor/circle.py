import sys
import typing
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QPainter, QColor, QMouseEvent, QEnterEvent
from PyQt6.QtCore import QMimeData, QPointF, QPoint, Qt, pyqtSignal
from pytruss import Joint


class JointWidget(QWidget):
    moved = pyqtSignal()

    def __init__(self, parent_widget, joint: Joint, radius=50):
        self.radius = radius
        self.joint = joint
        super().__init__(parent_widget)
        self.resize(self.radius, self.radius)
        self.dragging = False
        self.dragging_mode = False
        self.adding_member = False
        self.attach_to_cursor = False
        self.offset = QPoint(int(self.radius/2), int(self.radius/2))

    @property
    def location(self):
        return self.mapToParent(self.rect().center())

    def paintEvent(self, event):
        painter = QPainter(self)

        # Define the circle's properties
        if self.dragging_mode:
            circle_color = QColor(85, 120, 255)
        elif self.adding_member:
            circle_color = QColor(175, 220, 255)
        elif self.attach_to_cursor:
            circle_color = QColor(115, 150, 255, 100)
        else:
            circle_color = QColor(115, 150, 255)  # Blue color

        circle_center = self.rect().center()
        circle_radius = self.radius/3

        # Draw the circle
        # painter.setPen(circle_color)
        painter.setBrush(circle_color)
        painter.drawEllipse(circle_center,
                            int(circle_radius),
                            int(circle_radius))

    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.dragging_mode = True
            self.offset = a0.pos()
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            self.parent().highlighted_joints.clear()
            self.adding_member = False
            self.update()

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if self.dragging_mode and a0.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = a0.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

        elif self.attach_to_cursor:
            self.attach_to_cursor = False
            self.setMouseTracking(False)
            pos = self.mapToParent(a0.pos())
            self.parent().addJoint(pos.x(), self.parent().mapCartesian(pos.y()), self)
        else:
            self.selectJoint()

    def selectJoint(self):
        if self.adding_member:
            self.parent().highlighted_joints.remove(self.joint)
        if not self.adding_member:
            self.parent().highlighted_joints.add(self.joint)
        self.adding_member = not self.adding_member
        self.update()

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if self.dragging or self.attach_to_cursor:
            new_pos = self.mapToParent(a0.pos() - self.offset)
            self.move(new_pos)
            self.joint.set_x(self.location.x())
            self.joint.set_y(self.parent().mapCartesian(self.location.y()))
            self.parent().update()
            self.moved.emit()

    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        if self.dragging and self.dragging_mode and a0.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.dragging_mode = False
            self.update()
            self.parent().update()
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def updateLocation(self):
        self.move(
            int(self.joint.x_coordinate - self.radius/2),
            int(self.parent().mapCartesian(
                self.joint.y_coordinate) - self.radius/2),
        )
        self.moved.emit()

    def enterEvent(self, event: QEnterEvent | None) -> None:
        if self.dragging_mode:
            self.setCursor(Qt.CursorShape.OpenHandCursor)

    def leaveEvent(self, event):
        # Set the cursor shape when the mouse leaves the widget
        self.setCursor(Qt.CursorShape.ArrowCursor)
