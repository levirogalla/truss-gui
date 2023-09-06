import sys
import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QCursor, QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton

from .supports import RollerPin, FixedPin
from .circle import JointWidget
from pytruss import Member, Mesh, Support, Joint
from matplotlib import pyplot as plt


class TrussWidget(QWidget):

    interacted = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setMouseTracking(True)

        self.truss = Mesh()

        self.adding_joint = False
        self.temp_joint = JointWidget(self, Joint(0, 0), 50)
        self.temp_joint.hide()

        self.highlighted_joints: set[JointWidget] = set()

        # plt.ion()
        # fig, ax = plt.subplots()
        # self.fig = fig
        # self.ax = ax

    def addMember(self):
        visted: set[JointWidget] = set()
        for j1 in self.highlighted_joints:
            for j2 in self.highlighted_joints:
                if j1 != j2 and j2 not in visted:
                    self.truss.add_member(Member(j1, j2))
                    self.update()
            visted.add(j1)

        # self.ax.cla()
        # self.truss.show(ax=self.ax)
        plt.pause(1e-10)

        self.clearMoves()

    def addSupport(self, supportType, jointWidget: JointWidget):
        support = Support(jointWidget.joint, supportType)
        self.truss.add_support(support)
        if supportType == "p":
            supWidg = FixedPin(self, 50, support, jointWidget)
            supWidg.updateLocation()
            supWidg.show()

    def addJoint(self, x, y, temp_joint: JointWidget):

        # work around for now because pytruss doesnt allow for singular joints to be added
        joint = Joint(x, y)
        joint_widget = JointWidget(self, joint, 50)
        joint_temp = Joint(x+1, y+1)
        mem = Member(joint, joint_temp)
        self.truss.add_member(mem)
        self.truss.delete_joint(joint_temp)
        joint_widget.updateLocation()
        joint_widget.show()
        temp_joint.hide()

    def previewJoint(self):
        self.adding_joint = True
        self.temp_joint.show()
        self.temp_joint.setMouseTracking(True)
        self.temp_joint.attach_to_cursor = True

    def mapCartesian(self, y):
        return self.height() - y

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        for mem in self.truss.members:
            mem: Member

            painter.drawLine(
                int(mem.joint_a.x_coordinate), self.mapCartesian(
                    int(mem.joint_a.y_coordinate)),
                int(mem.joint_b.x_coordinate), self.mapCartesian(
                    int(mem.joint_b.y_coordinate))
            )

        self.interacted.emit()

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if a0.key() == 16777220:
            self.addMember()

    def clearMoves(self):
        for joint in self.findChildren(JointWidget):
            self.highlighted_joints.clear()
            joint.adding_member = False
            joint.dragging = False
            joint.dragging_mode = False
            joint.update()

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if self.adding_joint:
            self.temp_joint.joint.set_cordinates([a0.pos().x(), a0.pos().y()])
            self.temp_joint.updateLocation()
        else:
            self.clearMoves()

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if self.adding_joint:
            self.temp_joint.joint.set_cordinates(
                [a0.pos().x(), self.mapCartesian(a0.pos().y())])
            self.temp_joint.updateLocation()

        pass


def main():
    app = QApplication(sys.argv)
    window = TrussWidget()
    app.installEventFilter(window)
    window.setWindowTitle('Circle Example')
    window.setGeometry(100, 100, 400, 400)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
