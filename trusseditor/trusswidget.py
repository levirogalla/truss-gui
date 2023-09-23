import sys
import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QCursor, QKeyEvent
from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene

from .supports.supports import RollerPin, FixedPin, SupportAddWidget
from .forces.forces import ForceAddWidget, ArrowWidget
from .circle import JointWidget
from pytruss import Member, Mesh, Support, Joint, Force
from matplotlib import pyplot as plt


FORCE_SCALE = 10
JOINT_SIZE = 20
MEMBER_SIZE = 1
FORCE_HEAD_LENGTH = 20
FORCE_HEAD_WIDTH = 10


class TrussWidget(QWidget):

    interacted = pyqtSignal()
    joint_added = pyqtSignal()
    member_added = pyqtSignal()
    support_added = pyqtSignal()
    force_added = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setMouseTracking(True)

        self.truss = Mesh()

        self.adding_joint = False
        self.temp_joint = JointWidget(self, Joint(0, 0), JOINT_SIZE)
        self.temp_joint.hide()

        self.forms = set()

        self.highlighted_joints: set[Joint] = set()

    def addMember(self):
        visted: set[Joint] = set()
        for j1 in self.highlighted_joints:
            for j2 in self.highlighted_joints:
                if j1 != j2 and j2 not in visted:
                    self.truss.add_member(Member(j1, j2))
                    self.update()
            visted.add(j1)
        self.clearMoves()
        self.member_added.emit()

    def destroyForm(self, form):
        self.forms.remove(form)
        self.clearMoves()

    def supportForm(self):

        def addSupport(joint, support_type):

            for joint_widget in self.findChildren(JointWidget):
                if joint == joint_widget.joint:
                    selected_joint = joint_widget

            if support_type == "Fixed Pin":
                support = Support(joint, "p")
                self.truss.add_support(support)
                supWidg = FixedPin(self, JOINT_SIZE, support, selected_joint)
                supWidg.updateLocation()
                supWidg.show()
                self.support_added.emit()

            if support_type == "Roller Pin":
                support = Support(joint, "rp")
                self.truss.add_support(support)
                supWidg = RollerPin(self, JOINT_SIZE, support, selected_joint)
                supWidg.updateLocation()
                supWidg.show()
                self.support_added.emit()

            else:
                print(ValueError(
                    f"Support type {support_type} not recognised"))

        for selected_joint in self.highlighted_joints:
            form = SupportAddWidget(
                self.truss.joints, selected_joint, self.destroyForm, addSupport)
            form.show()
            self.forms.add(form)

        if len(self.highlighted_joints) == 0:
            form = SupportAddWidget(
                self.truss.joints, None, self.destroyForm, addSupport)
            form.show()
            self.forms.add(form)

    def forceForm(self):

        def addForce(joint: Joint, x: float, y: float):
            for joint_widget in self.findChildren(JointWidget):
                if joint == joint_widget.joint:
                    selected_joint = joint_widget

            force = Force(joint, x, y)
            self.truss.apply_force(force)
            self.force_added.emit()

        for selected_joint in self.highlighted_joints:
            form = ForceAddWidget(
                self.truss.joints, selected_joint, self.destroyForm, addForce)
            form.show()
            self.forms.add(form)

        if len(self.highlighted_joints) == 0:
            form = ForceAddWidget(
                self.truss.joints, None, self.destroyForm, addForce)
            form.show()
            self.forms.add(form)

    def addJoint(self, x, y, temp_joint: JointWidget):

        # work around for now because pytruss doesnt allow for singular joints to be added
        joint = Joint(x, y)
        joint_widget = JointWidget(self, joint, JOINT_SIZE)
        joint_temp = Joint(x+1, y+1)
        mem = Member(joint, joint_temp)
        self.truss.add_member(mem)
        self.truss.delete_joint(joint_temp)
        joint_widget.updateLocation()
        joint_widget.show()
        temp_joint.hide()
        self.adding_joint = False
        self.joint_added.emit()

    def previewJoint(self):
        self.adding_joint = True
        self.temp_joint.show()
        self.temp_joint.setMouseTracking(True)
        self.temp_joint.attach_to_cursor = True

    def mapCartesian(self, y):
        return self.height() - y

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        pen = QPen(Qt.GlobalColor.black, MEMBER_SIZE)
        painter.setPen(pen)

        # paint members
        for mem in self.truss.members:
            mem: Member

            painter.drawLine(
                int(mem.joint_a.x_coordinate), self.mapCartesian(
                    int(mem.joint_a.y_coordinate)),
                int(mem.joint_b.x_coordinate), self.mapCartesian(
                    int(mem.joint_b.y_coordinate))
            )

        # paint arrows
        for force in self.truss.forces:
            force: Force
            slope = (force.y_component/force.x_component+1e-10)
            perpendicular_slope = -(1/slope)

            head_x = force.joint.x_coordinate.item()
            head_y = self.mapCartesian(force.joint.y_coordinate.item())

            tail_start_x = head_x - force.x_component
            tail_start_y = head_y - force.y_component
            tail_end_x = head_x - (1/slope)*FORCE_HEAD_LENGTH
            tail_end_y = head_y - slope*FORCE_HEAD_LENGTH

            # tail_start_x = tail_start_x * FORCE_SCALE
            # tail_start_y = tail_start_y * FORCE_SCALE

            head_p1_x = (tail_end_x - (1/perpendicular_slope)
                         * (FORCE_HEAD_WIDTH/2)
                         )

            head_p1_y = tail_end_y - perpendicular_slope*(FORCE_HEAD_WIDTH/2)

            head_p2_x = (tail_end_x + (1/perpendicular_slope)
                         * (FORCE_HEAD_WIDTH/2)
                         )

            head_p2_y = tail_end_y + perpendicular_slope*(FORCE_HEAD_WIDTH/2)

            painter.drawLine(int(tail_start_x), int(tail_start_y),
                             int(tail_end_x), int(tail_end_y))

            # painter.drawLine(int(tail_end_x), int(tail_end_y),
            #                  int(head_p1_x), int(head_p1_y))
            # painter.drawLine(int(tail_end_x), int(tail_end_y),
            #                  int(head_p2_x), int(head_p1_y))
            # painter.drawLine(int(head_p1_x), int(head_p1_y),
            #                  int(head_x), int(head_y))
            # painter.drawLine(int(head_p2_x), int(head_p2_y),
            #                  int(head_x), int(head_y))

        self.interacted.emit()

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if a0.key() == 16777220:
            self.addMember()

    def clearMoves(self):
        for joint in self.findChildren(JointWidget):
            self.highlighted_joints.clear()
            joint.selected = False
            joint.dragging = False
            joint.dragging_mode = False
            joint.update()

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        if self.adding_joint:
            self.temp_joint.joint.set_cordinates([a0.pos().x(), a0.pos().y()])
            self.temp_joint.updateLocation()
            self.adding_joint = False
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
