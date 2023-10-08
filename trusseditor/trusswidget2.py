import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget, QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsEllipseItem
from pytruss import Mesh, Member, Force, Joint

import pickle
import sys
import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QEvent, QObject, QPointF, Qt, pyqtSignal, QRectF, QSizeF
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QCursor, QKeyEvent, QColor, QPainterPath
from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QGestureEvent, QPinchGesture
from .supports.supports import SupportForm
from .forces.forces import ForceForm

from pytruss import Member, Mesh, Support, Joint, Force
from matplotlib import pyplot as plt


FORCE_SCALE = 10
JOINT_SIZE = 20
SUPPORT_SIZE = JOINT_SIZE*2
FORCE_SIZE = 2
MEMBER_SIZE = 10
FORCE_HEAD_LENGTH = 20
FORCE_HEAD_WIDTH = 10


class TrussItem(QGraphicsItem):
    def __init__(self) -> None:
        super().__init__()

    def convertCordinate(self, Y):
        """Converts Y coordinate from scene to cartesian and Vice Versa."""
        new_y = self.sceneBoundingRect().height() - Y
        return new_y

    def getConnection(self, truss_item_id):
        "Retruns a connection from the widget connections."
        try:
            item = self.scene().views()[0].connections[truss_item_id]
            return item
        except KeyError as error:
            print(f"{truss_item_id} not found")


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
        # self.setFlag(self.)

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
                member_item: MemberItem = self.getConnection(id(member))
                member_item.prepareGeometryChange()

            for force in self.joint.forces:
                force_item: ForceItem = self.getConnection(id(force))
                force_item.prepareGeometryChange()

            if self.joint.support is not None:
                support_item: SupportItem = self.getConnection(
                    id(self.joint.support))
                support_item.prepareGeometryChange()

            new_pos = self.mapToParent(a0.pos() - self.offset)
            self.setPos(new_pos)
            self.updateCartesianLocation()
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
        j1 = self.getConnection(id(self.member.joint_a))
        j2 = self.getConnection(id(self.member.joint_b))
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

        return rect

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        p1: QPointF = self.getConnection(id(self.member.joint_a)).scenePos()
        p2: QPointF = self.getConnection(id(self.member.joint_b)).scenePos()

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


class SupportItem(TrussItem):
    def __init__(self, size, support: Support) -> None:
        super().__init__()
        self.r = size
        self.support = support
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)

        # stack under members
        self.setZValue(-3)

    @property
    def offset(self) -> QPointF:
        joint_item = self.getConnection(id(self.support.joint)).scenePos()
        return joint_item

    def shape(self) -> QPainterPath:
        path = QPainterPath()

        if Support.Base.base_to_code(self.support.base) == "p":
            # Define your custom shape here
            # Move the pen to the starting point
            path.moveTo(0, 0)
            path.lineTo(-self.r/2, self.r/2)  # Draw a line to a point
            path.lineTo(self.r/2, self.r/2)  # Draw another line
            # Draw another line
            path.lineTo(0, 0)
            path.moveTo(-self.r/2, self.r/2)
            path.lineTo(-self.r/2, self.r)
            path.lineTo(self.r/2, self.r)
            path.lineTo(self.r/2, self.r/2)

            return path.translated(self.offset)

        elif Support.Base.base_to_code(self.support.base) == "rp":
            # Move the pen to the starting point
            path.moveTo(0, 0)
            path.lineTo(-self.r/2, self.r/2)  # Draw a line to a point
            path.lineTo(self.r/2, self.r/2)  # Draw another line
            # Draw another line
            path.lineTo(0, 0)
            path.addEllipse(-self.r/2, self.r/2, self.r/2, self.r/2)
            path.addEllipse(0, self.r/2, self.r/2, self.r/2)

            return path.translated(self.offset)

    def boundingRect(self) -> QRectF:
        rect = QRectF(-self.r/2, 0, self.r, self.r)
        return rect.translated(self.offset)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        draw_bound_box = False

        # self.setPos(self.mapToScene(self.support.joint.x_coordinate,
        #             self.convertCordinate(self.support.joint.y_coordinate)))

        if self.isSelected():
            color = QColor(175, 220, 255)
        else:
            color = QColor(0, 0, 0)

        path = self.shape()

        painter.setPen(color)
        painter.fillPath(path, color)

        if draw_bound_box:
            painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self.setSelected(not self.isSelected())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        pass


class ForceItem(TrussItem):
    def __init__(self, force: Force, thickness, force_scale=10, head_width=10, head_length=30) -> None:
        super().__init__()
        self.force = force
        self.force_scale = force_scale
        self.head_length = head_length
        self.head_width = head_width
        self.thickness = thickness
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)

        # stack ontop members
        self.setZValue(-1)

    @property
    def offset(self) -> QPointF:
        offset = self.getConnection(id(self.force.joint)).scenePos()
        return offset

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        tail: QPointF = self.getConnection(id(self.force.joint)).scenePos()

        dx = self.force.x_component

        # must flip y because of graphics origin
        dy = -self.force.y_component

        norm = ((dy**2 + dx**2)**0.5)
        norm_vector = QPointF(dx, dy)/norm

        head = tail + norm_vector*self.force_scale*norm

        if dy != 0:
            slope = (dx / dy)
        else:
            slope = 10e10

        if slope != 0:
            perp_slope = -1/slope
        else:
            perp_slope = 10e10

        # normalize and apply thickness
        perp_norm = ((perp_slope**2 + 1**2)**0.5)
        perp_vector = (QPointF(perp_slope, 1) / perp_norm) * self.thickness

        p1a = tail + perp_vector
        p1b = tail - perp_vector
        p2a = head + perp_vector - norm_vector*self.head_length
        p2b = head - perp_vector - norm_vector*self.head_length
        p3a = head + perp_vector*self.head_width/2 - norm_vector*self.head_length
        p3b = head
        p3c = head - perp_vector*self.head_width/2 - norm_vector*self.head_length

        path.moveTo(p1a)
        path.lineTo(p1b)
        path.lineTo(p2b)
        path.lineTo(p3c)
        path.lineTo(p3b)
        path.lineTo(p3a)
        path.lineTo(p2a)
        path.closeSubpath()

        return path

    def boundingRect(self) -> QRectF:
        j1: JointItem = self.getConnection(id(self.force.joint))
        tail: QPointF = j1.scenePos()

        dx = self.force.x_component*self.force_scale
        dy = -self.force.y_component*self.force_scale

        # must flip y because of graphics origin
        head = tail + QPointF(dx, dy)

        adjust_both = QPointF(self.thickness+self.head_width,
                              self.thickness+self.head_width)
        adjust_x = QPointF(self.thickness, 0)
        adjust_y = QPointF(0, self.thickness)

        # top left and bottom right
        if tail.x() <= head.x() and tail.y() <= head.y():
            tail = tail - adjust_both
            head = head + adjust_both

        # bottom left and top right
        if tail.x() <= head.x() and tail.y() >= head.y():
            tail = tail + adjust_y - adjust_x
            head = head - adjust_y + adjust_x

        # top left and bottom right
        if tail.x() >= head.x() and tail.y() >= head.y():
            tail = tail + adjust_both
            head = head - adjust_both

        # bottom left and top right
        if tail.x() >= head.x() and tail.y() <= head.y():
            tail = tail - adjust_y + adjust_x
            head = head + adjust_y - adjust_x

        rect = QRectF(tail, head).normalized()

        return rect

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        draw_bound_box = False

        if self.isSelected():
            color = QColor(175, 220, 255)
        else:
            color = QColor(0, 0, 0)

        path = self.shape()

        painter.setPen(color)
        painter.fillPath(path, color)

        if draw_bound_box:
            painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self.setSelected(not self.isSelected())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        pass


class TrussWidget(QGraphicsView):

    interacted = pyqtSignal()
    joint_added = pyqtSignal()
    member_added = pyqtSignal()
    support_added = pyqtSignal()
    force_added = pyqtSignal()

    def __init__(self, file: str = None):
        super().__init__()
        self.truss = Mesh()
        self.file = file
        self.truss_scene = QGraphicsScene(self)
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.setScene(self.truss_scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(self.ViewportAnchor.AnchorUnderMouse)
        self.setMouseTracking(False)
        self.connections = dict()
        self.preview_joint = PreviewJointItem(JOINT_SIZE)
        self.scene().addItem(self.preview_joint)
        self.preview_joint.hide()
        self.forms: set[QWidget] = set()

        self.loadTrussWidgetFromMesh()

    def loadTrussWidgetFromMesh(self, load_from_file=True):
        # delete all existing items on scene
        self.scene().clear()
        self.connections.clear()

        if load_from_file:
            if self.file is not None:
                with open(self.file, "rb") as f:
                    mesh: Mesh = pickle.load(f)

                self.truss = mesh

        # maybe make function to add widget to scene since its used a lot
        for joint in self.truss.joints:
            joint_widget = JointItem(joint, JOINT_SIZE)
            self.connections[id(joint)] = joint_widget
            self.scene().addItem(self.connections[id(joint)])

        for member in self.truss.members:
            member_widget = MemberItem(MEMBER_SIZE, member)
            self.connections[id(member)] = member_widget
            self.scene().addItem(self.connections[id(member)])

        for support in self.truss.supports:
            support_widget = SupportItem(SUPPORT_SIZE, support)
            self.connections[id(support)] = support_widget
            self.scene().addItem(self.connections[id(support)])

        for force in self.truss.forces:
            force_widget = ForceItem(
                force, FORCE_SIZE, FORCE_SCALE, FORCE_HEAD_WIDTH, FORCE_HEAD_LENGTH)
            self.connections[id(force)] = force_widget
            self.scene().addItem(self.connections[id(force)])

        self.scene().update()

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
            self.scene().update()
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

        item = JointItem(new_joint, JOINT_SIZE)
        self.connections[id(new_joint)] = item
        self.scene().addItem(item)
        self.joint_added.emit()

    def addMember(self):
        visted: set[Joint] = set()
        items = self.scene().selectedItems()
        for j1 in items:
            for j2 in items:
                if isinstance(j1, JointItem) and isinstance(j2, JointItem):
                    if j1.joint != j2.joint and j2.joint not in visted:
                        member = Member(j1.joint, j2.joint)
                        self.truss.add_member(member)
                        item = MemberItem(MEMBER_SIZE, member)
                        self.connections[id(member)] = item
                        self.scene().addItem(item)
            visted.add(j1.joint)
        self.scene().clearSelection()
        self.member_added.emit()

    def destroyForm(self, form: QWidget):
        self.forms.remove(form)
        for joint_item in self.findChildren(JointItem):
            joint_item: JointItem
            joint_item.setSelected(False)

    def supportForm(self):
        def addSupport(joint, support_type):
            if support_type == "Fixed Pin":
                support = Support(joint, "p")
                self.truss.add_support(support)
                supWidg = SupportItem(SUPPORT_SIZE, support)
                self.connections[id(support)] = supWidg
                self.scene().addItem(supWidg)
                self.support_added.emit()

            elif support_type == "Roller Pin":
                support = Support(joint, "rp")
                self.truss.add_support(support)
                supWidg = SupportItem(SUPPORT_SIZE, support)
                self.connections[id(support)] = supWidg
                self.scene().addItem(supWidg)
                self.support_added.emit()

            else:
                print(ValueError(
                    f"Support type {support_type} not recognised"))

        no_selected_joints = True
        for selected_joint in self.scene().selectedItems():
            if isinstance(selected_joint, JointItem):
                form = SupportForm(
                    self.truss.joints, selected_joint.joint, self.destroyForm, addSupport)
                form.show()
                self.forms.add(form)
                no_selected_joints = False

        if no_selected_joints:
            form = SupportForm(
                self.truss.joints, None, self.destroyForm, addSupport)
            form.show()
            self.forms.add(form)

    def forceForm(self):
        def addForce(joint: Joint, x: float, y: float):
            force = Force(joint, x, y)
            self.truss.apply_force(force)
            force_item = ForceItem(
                force, FORCE_SIZE, FORCE_SCALE, FORCE_HEAD_WIDTH, FORCE_HEAD_LENGTH)
            self.connections[id(force)] = force_item
            self.scene().addItem(force_item)
            self.force_added.emit()

        no_selected_joints = True
        for selected_joint in self.scene().selectedItems():
            if isinstance(selected_joint, JointItem):
                form = ForceForm(
                    self.truss.joints, selected_joint.joint, self.destroyForm, addForce)
                form.show()
                self.forms.add(form)
                no_selected_joints = False

        if no_selected_joints:
            form = ForceForm(
                self.truss.joints, None, self.destroyForm, addForce)
            form.show()
            self.forms.add(form)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        self.interacted.emit()
        return super().paintEvent(event)


def main():
    app = QApplication(sys.argv)
    window = TrussWidget()

    joint1 = JointItem(Joint(0, 0))
    joint2 = JointItem(Joint(100, 100))

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
