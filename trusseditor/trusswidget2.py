import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget, QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt6.QtCore import Qt
from pytruss import Mesh, Member, Force, Joint

import torch
import sys
import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPointF, Qt, pyqtSignal, QRectF, QSizeF
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QCursor, QKeyEvent, QColor, QPainterPath
from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QGestureEvent, QPinchGesture

from pytruss import Member, Mesh, Support, Joint, Force
from matplotlib import pyplot as plt


FORCE_SCALE = 10
JOINT_SIZE = 20
MEMBER_SIZE = 1
FORCE_HEAD_LENGTH = 20
FORCE_HEAD_WIDTH = 10


class TrussItem(QGraphicsItem):
    def __init__(self) -> None:
        super().__init__()

    def convertCordinate(self, Y):
        """Converts Y coordinate from scene to cartesian and Vice Versa."""
        new_y = self.sceneBoundingRect().height() - Y
        return new_y

    def getConnection(self, key):
        "Retruns a connection from the widget connections."
        try:
            item = self.scene().views()[0].connections[key]
            return item
        except KeyError as error:
            print(f"{key} not found")


class JointItem(TrussItem):

    def __init__(self, joint: Joint = None, radius=50, preview=False) -> None:
        super().__init__()

        self.joint = joint
        self.__dragging_mode = False
        self.__dragging = False
        self.__preview = preview
        self.radius = radius

        # make item selectable
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        # Define the circle's properties
        if self.__dragging_mode:
            circle_color = QColor(85, 120, 255)
        elif self.isSelected():
            circle_color = QColor(175, 220, 255)
        elif self.__preview:
            circle_color = QColor(115, 150, 255, 100)
        else:
            circle_color = QColor(115, 150, 255)

        painter.setBrush(circle_color)
        painter.drawEllipse(int(-self.radius/2), int(-self.radius/2),
                            int(self.radius),
                            int(self.radius))

    def boundingRect(self) -> QRectF:
        rect = QRectF(-self.radius/2, -self.radius/2, self.radius, self.radius)
        return rect

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addEllipse(-self.radius/2, -self.radius/2,
                        self.radius, self.radius)
        return path

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemSceneHasChanged:
            self.updateSceneLocation()
        elif self.scene() is not None:
            self.updateCartesianLocation()
        return super().itemChange(change, value)

    def updateSceneLocation(self) -> None:
        point = self.mapToScene(self.joint.x_coordinate,
                                self.convertCordinate(
                                    self.joint.y_coordinate) - self.radius
                                )
        self.setPos(point)

    def updateCartesianLocation(self) -> None:

        self.joint.set_cordinates(
            [self.scenePos().x(),
             self.convertCordinate(self.scenePos().y()) - self.radius]
        )

    def clearModes(self):
        self.setSelected(False)
        self.__dragging = False
        self.__dragging_mode = False

    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__dragging_mode = True
            self.offset = a0.pos()
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            self.setSelected(False)
            self.scene().update()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if self.__dragging_mode and event.button() == Qt.MouseButton.LeftButton:
            self.__dragging = True
            self.offset = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        else:
            self.setSelected(not self.isSelected())

        self.scene().update()

    def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
        if self.__dragging:
            for member in self.joint.members:
                member_item: MemberItem = self.getConnection(member)
                member_item.prepareGeometryChange()

            new_pos = self.mapToParent(a0.pos() - self.offset)
            self.setPos(new_pos)

            # to redraw the members
            self.scene().update()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if self.__dragging:
            self.clearModes()
            self.setCursor(Qt.CursorShape.ArrowCursor)
        self.update()
        self.scene().update()

    def getCenter(self) -> QPointF:
        center = self.scenePos()
        return center


class PreviewJointItem(JointItem):

    def __init__(self, radius=50) -> None:
        # initail a new joint object to be added
        super().__init__(Joint(0, 0), radius, True)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        return super().paint(painter, option, widget)


class MemberItem(TrussItem):

    def __init__(self, thickness, member: Member):
        super().__init__()
        self.thickness = thickness
        self.member = member

        # make item selectable
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

        # stack behind joints and supports
        self.setZValue(-2)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        # set to draw bounding box
        draw_bound_box = True

        if self.isSelected():
            color = QColor(175, 220, 255)
        else:
            color = QColor(0, 0, 0)

        path = self.shape()

        pen = QPen(color)
        painter.setPen(pen)
        painter.drawPath(path)
        painter.fillPath(path, color)

        if draw_bound_box:
            rect = self.boundingRect()
            painter.drawRect(rect)

    def boundingRect(self) -> QRectF:
        j1 = self.getConnection(self.member.joint_a)
        j2 = self.getConnection(self.member.joint_b)
        p1: QPointF = j1.scenePos()
        p2: QPointF = j2.scenePos()

        adjust_both = QPointF(self.thickness, self.thickness)
        adjust_x = QPointF(self.thickness, 0)
        adjust_y = QPointF(0, self.thickness)

        # top left and bottom right
        if p1.x() <= p2.x() and p1.y() <= p2.y():
            p1 = p1 - adjust_both
            p2 = p2 + adjust_both

        # bottom left and top right
        if p1.x() <= p2.x() and p1.y() >= p2.y():
            p1 = p1 + adjust_y - adjust_x
            p2 = p2 - adjust_y + adjust_x

        # top left and bottom right
        if p1.x() >= p2.x() and p1.y() >= p2.y():
            p1 = p1 + adjust_both
            p2 = p2 - adjust_both

        # bottom left and top right
        if p1.x() >= p2.x() and p1.y() <= p2.y():
            p1 = p1 - adjust_y + adjust_x
            p2 = p2 + adjust_y - adjust_x

        rect = QRectF(p1, p2).normalized()

        print(rect)

        return rect

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        p1: QPointF = self.getConnection(self.member.joint_a).scenePos()
        p2: QPointF = self.getConnection(self.member.joint_b).scenePos()

        dx = (p1.x() - p2.x())
        dy = (p1.y() - p2.y())

        if dy != 0:
            slope = (dx / dy)
        else:
            slope = 10e10

        if slope != 0:
            perp_slope = -1/slope
        else:
            perp_slope = 10e10

        # normalize and apply thickness
        norm = ((perp_slope**2 + 1**2)**0.5)
        perp_vector = (QPointF(perp_slope, 1) / norm) * self.thickness

        p1a = p1 + perp_vector
        p1b = p1 - perp_vector
        p2a = p2 + perp_vector
        p2b = p2 - perp_vector

        path.moveTo(p1a.x(), p1a.y())
        path.lineTo(p1b.x(), p1b.y())
        path.lineTo(p2b.x(), p2b.y())
        path.lineTo(p2a.x(), p2a.y())
        path.closeSubpath()

        return path

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self.setSelected(not self.isSelected())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        pass


class SupportItem(QGraphicsItem):
    def __init__(self, size, support: Support):
        super().__init__()
        self.size = size
        self.support = support

        # make item selectable
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

        # stack behind joints
        self.setZValue(-1)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        # set to draw bounding box
        draw_bound_box = False

        if self.isSelected():
            color = QColor(175, 220, 255)
        else:
            color = QColor(0, 0, 0)

        path = self.shape()

        pen = QPen(color)
        painter.setPen(pen)
        painter.drawPath(path)
        painter.fillPath(path, color)

        if draw_bound_box:
            rect = self.boundingRect()
            painter.drawRect(rect)

    def boundingRect(self) -> QRectF:
        j1 = self.getConnection(self.member.joint_a)
        j2 = self.getConnection(self.member.joint_b)
        p1: QPointF = j1.scenePos()
        p2: QPointF = j2.scenePos()

        adjust_both = QPointF(self.thickness, self.thickness)
        adjust_x = QPointF(self.thickness, 0)
        adjust_y = QPointF(0, self.thickness)

        # top left and bottom right
        if p1.x() <= p2.x() and p1.y() <= p2.y():
            p1 = p1 - adjust_both
            p2 = p2 + adjust_both

        # bottom left and top right
        if p1.x() <= p2.x() and p1.y() >= p2.y():
            p1 = p1 + adjust_y - adjust_x
            p2 = p2 - adjust_y + adjust_x

        # top left and bottom right
        if p1.x() >= p2.x() and p1.y() >= p2.y():
            p1 = p1 + adjust_both
            p2 = p2 - adjust_both

        # bottom left and top right
        if p1.x() >= p2.x() and p1.y() <= p2.y():
            p1 = p1 - adjust_y + adjust_x
            p2 = p2 + adjust_y - adjust_x

        rect = QRectF(p1, p2)

        return rect.normalized()

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        p1: QPointF = self.getConnection(self.member.joint_a).scenePos()
        p2: QPointF = self.getConnection(self.member.joint_b).scenePos()

        dx = (p1.x() - p2.x())
        dy = (p1.y() - p2.y())

        if dy != 0:
            slope = (dx / dy)
        else:
            slope = 10e10

        if slope != 0:
            perp_slope = -1/slope
        else:
            perp_slope = 10e10

        # normalize and apply thickness
        norm = ((perp_slope**2 + 1**2)**0.5)
        perp_vector = (QPointF(perp_slope, 1) / norm) * self.thickness

        p1a = p1 + perp_vector
        p1b = p1 - perp_vector
        p2a = p2 + perp_vector
        p2b = p2 - perp_vector

        path.moveTo(p1a.x(), p1a.y())
        path.lineTo(p1b.x(), p1b.y())
        path.lineTo(p2b.x(), p2b.y())
        path.lineTo(p2a.x(), p2a.y())
        path.closeSubpath()

        return path

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self.setSelected(not self.isSelected())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        pass


class ForceItem(QGraphicsLineItem):
    pass


class TrussWidget(QGraphicsView):

    interacted = pyqtSignal()
    joint_added = pyqtSignal()
    member_added = pyqtSignal()
    support_added = pyqtSignal()
    force_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.truss = Mesh()
        self.truss_scene = QGraphicsScene(self)
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.setScene(self.truss_scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(self.ViewportAnchor.AnchorUnderMouse)
        self.setMouseTracking(False)
        self.connections = dict()
        self.preview_joint = PreviewJointItem(50)
        self.scene().addItem(self.preview_joint)
        self.preview_joint.hide()

    def event(self, event: QEvent | None) -> bool:
        if event.type() == QEvent.Type.Gesture:
            self.gestureEvent(event)
        return super().event(event)

    def gestureEvent(self, event: QGestureEvent):
        if isinstance(event.gesture(Qt.GestureType.PinchGesture), QPinchGesture):
            self.pinchTriggered(event.gesture(Qt.GestureType.PinchGesture))

    def pinchTriggered(self, gesture: QPinchGesture):
        scale_factor = gesture.scaleFactor()
        self.scale(scale_factor, scale_factor)

    def previewJoint(self):
        self.setMouseTracking(True)
        self.preview_joint.show()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        # has mouse tracking is only enabled when a joint is being previewed
        if self.hasMouseTracking():
            self.preview_joint.setPos(self.mapToScene(event.pos()))
            self.preview_joint.updateCartesianLocation()
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        # has mouse tracking is only enabled when a joint is being previewed
        if self.hasMouseTracking():
            self.setMouseTracking(False)
            self.preview_joint.hide()
            self.addJoint(self.preview_joint.joint)
            return

        return super().mousePressEvent(event)

    def addJoint(self, joint: Joint):
        temp = Joint(0, 10+1e-5)
        new_joint = Joint(joint.x_coordinate, joint.y_coordinate)
        mem = Member(temp, new_joint)
        self.truss.add_member(mem)
        self.truss.delete_joint(temp)

        item = JointItem(new_joint)
        self.connections[new_joint] = item
        self.scene().addItem(item)

    def addMember(self):
        visted: set[Joint] = set()
        items = self.scene().selectedItems()
        for j1 in items:
            for j2 in items:
                if isinstance(j1, JointItem) and isinstance(j2, JointItem):
                    if j1.joint != j2.joint:
                        member = Member(j1.joint, j2.joint)
                        self.truss.add_member(member)
                        item = MemberItem(10, member)
                        self.connections[member] = item
                        self.scene().addItem(item)
            visted.add(j1.joint)
        self.scene().clearSelection()
        # self.member_added.emit()


# class TrussWidget2(QWidget):

#     interacted = pyqtSignal()
#     joint_added = pyqtSignal()
#     member_added = pyqtSignal()
#     support_added = pyqtSignal()
#     force_added = pyqtSignal()

#     def __init__(self) -> None:
#         super().__init__()
#         self.setMouseTracking(True)

#         self.truss = Mesh()

#         self.adding_joint = False
#         self.temp_joint = JointWidget(self, Joint(0, 0), JOINT_SIZE)
#         self.temp_joint.hide()

#         self.forms = set()

#         self.highlighted_joints: set[Joint] = set()

#     def addMember(self):
#         visted: set[Joint] = set()
#         for j1 in self.highlighted_joints:
#             for j2 in self.highlighted_joints:
#                 if j1 != j2 and j2 not in visted:
#                     self.truss.add_member(Member(j1, j2))
#                     self.update()
#             visted.add(j1)
#         self.clearMoves()
#         self.member_added.emit()

#     def destroyForm(self, form):
#         self.forms.remove(form)
#         self.clearMoves()

#     def supportForm(self):

#         def addSupport(joint, support_type):

#             for joint_widget in self.findChildren(JointWidget):
#                 if joint == joint_widget.joint:
#                     selected_joint = joint_widget

#             if support_type == "Fixed Pin":
#                 support = Support(joint, "p")
#                 self.truss.add_support(support)
#                 supWidg = FixedPin(self, JOINT_SIZE, support, selected_joint)
#                 supWidg.updateLocation()
#                 supWidg.show()
#                 self.support_added.emit()

#             if support_type == "Roller Pin":
#                 support = Support(joint, "rp")
#                 self.truss.add_support(support)
#                 supWidg = RollerPin(self, JOINT_SIZE, support, selected_joint)
#                 supWidg.updateLocation()
#                 supWidg.show()
#                 self.support_added.emit()

#             else:
#                 print(ValueError(
#                     f"Support type {support_type} not recognised"))

#         for selected_joint in self.highlighted_joints:
#             form = SupportAddWidget(
#                 self.truss.joints, selected_joint, self.destroyForm, addSupport)
#             form.show()
#             self.forms.add(form)

#         if len(self.highlighted_joints) == 0:
#             form = SupportAddWidget(
#                 self.truss.joints, None, self.destroyForm, addSupport)
#             form.show()
#             self.forms.add(form)

#     def forceForm(self):

#         def addForce(joint: Joint, x: float, y: float):
#             for joint_widget in self.findChildren(JointWidget):
#                 if joint == joint_widget.joint:
#                     selected_joint = joint_widget

#             force = Force(joint, x, y)
#             self.truss.apply_force(force)
#             self.force_added.emit()

#         for selected_joint in self.highlighted_joints:
#             form = ForceAddWidget(
#                 self.truss.joints, selected_joint, self.destroyForm, addForce)
#             form.show()
#             self.forms.add(form)

#         if len(self.highlighted_joints) == 0:
#             form = ForceAddWidget(
#                 self.truss.joints, None, self.destroyForm, addForce)
#             form.show()
#             self.forms.add(form)

#     def addJoint(self, x, y, temp_joint: JointWidget):

#         # work around for now because pytruss doesnt allow for singular joints to be added
#         joint = Joint(x, y)
#         joint_widget = JointWidget(self, joint, JOINT_SIZE)
#         joint_temp = Joint(x+1, y+1)
#         mem = Member(joint, joint_temp)
#         self.truss.add_member(mem)
#         self.truss.delete_joint(joint_temp)
#         joint_widget.updateLocation()
#         joint_widget.show()
#         temp_joint.hide()
#         self.adding_joint = False
#         self.joint_added.emit()

#     def previewJoint(self):
#         self.adding_joint = True
#         self.temp_joint.show()
#         self.temp_joint.setMouseTracking(True)
#         self.temp_joint.attach_to_cursor = True

#     def mapCartesian(self, y):
#         return self.height() - y

#     def paintEvent(self, a0: QPaintEvent | None) -> None:
#         painter = QPainter(self)
#         pen = QPen(Qt.GlobalColor.black, MEMBER_SIZE)
#         painter.setPen(pen)

#         # paint members
#         for mem in self.truss.members:
#             mem: Member

#             painter.drawLine(
#                 int(mem.joint_a.x_coordinate), self.mapCartesian(
#                     int(mem.joint_a.y_coordinate)),
#                 int(mem.joint_b.x_coordinate), self.mapCartesian(
#                     int(mem.joint_b.y_coordinate))
#             )

#         # paint arrows
#         for force in self.truss.forces:
#             force: Force
#             slope = (force.y_component/force.x_component+1e-10)
#             perpendicular_slope = -(1/slope)

#             head_x = force.joint.x_coordinate.item()
#             head_y = self.mapCartesian(force.joint.y_coordinate.item())

#             tail_start_x = head_x - force.x_component
#             tail_start_y = head_y - force.y_component
#             tail_end_x = head_x - (1/slope)*FORCE_HEAD_LENGTH
#             tail_end_y = head_y - slope*FORCE_HEAD_LENGTH

#             # tail_start_x = tail_start_x * FORCE_SCALE
#             # tail_start_y = tail_start_y * FORCE_SCALE

#             head_p1_x = (tail_end_x - (1/perpendicular_slope)
#                          * (FORCE_HEAD_WIDTH/2)
#                          )

#             head_p1_y = tail_end_y - perpendicular_slope*(FORCE_HEAD_WIDTH/2)

#             head_p2_x = (tail_end_x + (1/perpendicular_slope)
#                          * (FORCE_HEAD_WIDTH/2)
#                          )

#             head_p2_y = tail_end_y + perpendicular_slope*(FORCE_HEAD_WIDTH/2)

#             painter.drawLine(int(tail_start_x), int(tail_start_y),
#                              int(tail_end_x), int(tail_end_y))

#             # painter.drawLine(int(tail_end_x), int(tail_end_y),
#             #                  int(head_p1_x), int(head_p1_y))
#             # painter.drawLine(int(tail_end_x), int(tail_end_y),
#             #                  int(head_p2_x), int(head_p1_y))
#             # painter.drawLine(int(head_p1_x), int(head_p1_y),
#             #                  int(head_x), int(head_y))
#             # painter.drawLine(int(head_p2_x), int(head_p2_y),
#             #                  int(head_x), int(head_y))

#         self.interacted.emit()

#     def keyPressEvent(self, a0: QKeyEvent | None) -> None:
#         if a0.key() == 16777220:
#             self.addMember()

#     def clearMoves(self):
#         for joint in self.findChildren(JointWidget):
#             self.highlighted_joints.clear()
#             joint.selected = False
#             joint.dragging = False
#             joint.dragging_mode = False
#             joint.update()

#     def mousePressEvent(self, a0: QMouseEvent | None) -> None:
#         if self.adding_joint:
#             self.temp_joint.joint.set_cordinates([a0.pos().x(), a0.pos().y()])
#             self.temp_joint.updateLocation()
#             self.adding_joint = False
#         else:
#             self.clearMoves()

#     def mouseMoveEvent(self, a0: QMouseEvent | None) -> None:
#         if self.adding_joint:
#             self.temp_joint.joint.set_cordinates(
#                 [a0.pos().x(), self.mapCartesian(a0.pos().y())])
#             self.temp_joint.updateLocation()

#         pass


def main():
    app = QApplication(sys.argv)
    window = TrussWidget()

    joint1 = JointItem(Joint(0, 0))
    joint2 = JointItem(Joint(100, 100))

    # window.scene().addItem(joint2)
    window.addJoint(joint1.joint)
    window.addJoint(joint2.joint)
    joint1.setSelected(True)
    joint2.setSelected(True)

    window.addMember()

    app.installEventFilter(window)
    window.setWindowTitle('Circle Example')
    window.setGeometry(100, 100, 400, 400)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
