from pytruss import Member, Force, Joint, Support

from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget,  QGraphicsScene, QGraphicsView, QMenu
from PyQt6.QtCore import QPointF, Qt,  QRectF
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QColor, QPainterPath, QBrush
from PyQt6.QtWidgets import QWidget

from widgets.contextmenus.jointmenu.jointmenu import JointMenu
from widgets.contextmenus.selectedmenu.selectedmenu import SelectedMenu


class TrussItem(QGraphicsItem):
    """Base class for truss graphics item item."""

    def __init__(self) -> None:
        super().__init__()

    def convertCordinate(self, Y: float) -> float:
        """Converts Y coordinate from scene to cartesian and Vice Versa."""
        new_y = self.sceneBoundingRect().height() - Y
        return new_y

    def getConnection(self, truss_item_id: int) -> Force | Member | Joint | Support | None:
        """Retruns a connection from the widget connections."""
        try:
            item = self.scene().views()[0].connections[truss_item_id]
            return item
        except KeyError as error:
            print(f"{truss_item_id} not found")

    def logChange(self, event) -> None:
        """Logs a change to the edits array."""
        # shouldn't this be local to the truss??
        # maybe both for error tracking
        self.scene().views()[0].edits.append(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        """Handles mouse press event."""

        if event.button() == Qt.MouseButton.LeftButton:
            self.setSelected(not self.isSelected())
            print("Truss Item Mouse Press Event Function", self.isSelected())
            self.scene().views()[0].interacted.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.setSelected(True)
            menu = SelectedMenu(self.scene().views()[0])
            menu.exec(event.screenPos())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        # print("ballsn", self.isSelected())
        # "Handle mouse release event"
        return


class JointItem(TrussItem):
    """Class for Qt Joint Item"""

    def __init__(self, joint: Joint = None, radius=50, preview=False, color=(0, 0, 0), focused_color=(0, 0, 0), border_color=(0, 0, 0)) -> None:
        super().__init__()

        self.joint = joint
        self.__dragging_mode = False
        self.__dragging = False
        self.__preview = preview
        self.__color = color
        self.__focused_color = focused_color
        self.__border_color = border_color
        self.radius = radius

        # make item selectable
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)
        # self.setFlag(self.)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        """Paint the joint item."""
        # Define the circle's properties
        if self.__dragging_mode:
            circle_color = QColor(*self.__focused_color)
        elif self.isSelected():
            circle_color = QColor(175, 220, 255)
        elif self.__preview:
            circle_color = QColor(115, 150, 255, 100)
        else:
            circle_color = QColor(*self.__color)

        brush = QBrush(circle_color, Qt.BrushStyle.SolidPattern)
        border_brush = QBrush(QColor(*self.__border_color))
        pen = QPen(border_brush, self.radius*0.03)

        painter.setPen(pen)
        painter.setBrush(brush)

        # use shape to draw item
        path = self.shape()
        painter.drawPath(path)

    def boundingRect(self) -> QRectF:
        """Gets the bounding rectangle."""
        rect = QRectF(-self.radius/2, -self.radius/2, self.radius, self.radius)
        return rect

    def shape(self) -> QPainterPath:
        """Defines the shape/hitarea of the joint."""
        path = QPainterPath()
        path.addEllipse(-self.radius/2, -self.radius/2,
                        self.radius, self.radius)
        return path

    def itemChange(self, change, value):
        """Update the pytruss joint location on changes the the qt joint item."""
        if change == QGraphicsItem.GraphicsItemChange.ItemSceneHasChanged:
            self.updateSceneLocation()
        elif self.scene() is not None:
            self.updateCartesianLocation()
        return super().itemChange(change, value)

    def updateSceneLocation(self) -> None:
        """Updates the qt joint item location with the pytruss joint coordinates."""
        point = QPointF(self.joint.x_coordinate,
                        self.convertCordinate(
                            self.joint.y_coordinate) - self.radius)
        self.setPos(point)

    def updateCartesianLocation(self) -> None:
        """Updates the pytruss joint coordinates with the qt coordinates."""
        self.joint.set_cordinates(
            [self.scenePos().x(),
             self.convertCordinate(self.scenePos().y()) - self.radius]
        )

    def clearModes(self) -> None:
        """Clears all attributes related to dragging or selecting the joint."""
        self.setSelected(False)
        self.__dragging = False
        self.__dragging_mode = False

    def mouseDoubleClickEvent(self, a0: QMouseEvent | None) -> None:
        """Handle double click event."""
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__dragging_mode = True
            self.offset = a0.pos()
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            self.setSelected(False)
            self.scene().update()
            self.scene().views()[0].interacted.emit()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        """Handle mouse press event."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.__dragging_mode:
                self.__dragging = True
                self.offset = event.pos()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
                self.scene().views()[0].interacted.emit()
            else:
                super().mousePressEvent(event)
                return
            self.scene().views()[0].interacted.emit()

        if event.button() == Qt.MouseButton.RightButton:
            if self.isSelected():
                super().mousePressEvent(event)
            else:
                menu = JointMenu(self.scene().views()[0], self)
                menu.exec(event.screenPos())

    def mouseMoveEvent(self, a0: QGraphicsSceneMouseEvent | None) -> None:
        """Handles mouse move event."""
        if self.__dragging:
            for member in self.joint.members:
                member_item: MemberItem = self.getConnection(
                    id(member))
                member_item.prepareGeometryChange()

            for force in self.joint.forces:
                force_item: ForceItem = self.getConnection(id(force))
                force_item.prepareGeometryChange()

            if self.joint.support is not None:
                support_item: SupportItem = self.getConnection(
                    id(self.joint.support))
                support_item.prepareGeometryChange()

            new_pos = a0.scenePos() - self.offset
            self.setPos(new_pos)
            self.updateCartesianLocation()
            # to redraw the members
            self.scene().update()
            self.scene().views()[0].interacted.emit()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        """Handles mouse release event."""
        if self.__dragging:
            self.clearModes()
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.logChange(f"Item moved too {self.joint}")
            self.scene().views()[0].interacted.emit()

        self.update()
        self.scene().update()


class PreviewJointItem(JointItem):
    """Extends Joint Item to be a preview joint."""

    def __init__(self, radius=50) -> None:
        # initail a new joint object to be added
        super().__init__(Joint(0, 0, False), radius, True)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        return super().paint(painter, option, widget)


class MemberItem(TrussItem):
    """Class for Qt Member Item."""

    def __init__(self, thickness, member: Member, color=(0, 0, 0)):
        super().__init__()
        self.thickness = thickness
        self.member = member
        self.__color = color

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
            color = QColor(*self.__color)

        path = self.shape()

        painter.setPen(color)
        painter.fillPath(path, color)

        if draw_bound_box:
            rect = self.boundingRect()
            painter.drawRect(rect)

    def boundingRect(self) -> QRectF:
        """Returns bounding rect for member."""
        j1: JointItem = self.getConnection(id(self.member.joint_a))
        j2: JointItem = self.getConnection(id(self.member.joint_b))
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
        """Return member shape."""
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

        path.moveTo(p1a)
        path.lineTo(p1b)
        path.lineTo(p2b)
        path.lineTo(p2a)
        path.closeSubpath()

        return path


class SupportItem(TrussItem):
    """Class for Qt Support Item."""

    def __init__(self, size, support: Support, color=(0, 0, 0)) -> None:
        super().__init__()
        self.r = size
        self.support = support
        self.__color = color
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)

        # stack under members
        self.setZValue(-3)

    @property
    def offset(self) -> QPointF:
        """Gets the location of the joint item it is attached to."""
        joint_item = self.getConnection(id(self.support.joint)).scenePos()
        return joint_item

    def shape(self) -> QPainterPath:
        """Return shape of support item."""
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

        elif Support.Base.base_to_code(self.support.base) == "f":
            # Move the pen to the starting point
            path.moveTo(0, 0)
            path.lineTo(-self.r/2, 0)  # Draw a line to a point
            path.lineTo(-self.r/2, self.r)  # Draw another line
            # Draw another line
            path.lineTo(self.r/2, self.r)
            path.lineTo(self.r/2, 0)
            path.lineTo(0, 0)

            return path.translated(self.offset)

    def boundingRect(self) -> QRectF:
        """Retrun bounding rect for support."""
        rect = QRectF(-self.r/2, 0, self.r, self.r)
        return rect.translated(self.offset)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        """Paint the support."""
        draw_bound_box = False

        if self.isSelected():
            color = QColor(175, 220, 255)
        else:
            color = QColor(*self.__color)

        path = self.shape()

        painter.setPen(color)
        painter.fillPath(path, color)

        if draw_bound_box:
            painter.drawRect(self.boundingRect())


class ForceItem(TrussItem):
    """Class for Qt Force Item."""

    def __init__(self, force: Force, thickness, force_scale=10, head_width=10, head_length=30, color=(0, 0, 0)) -> None:
        super().__init__()
        self.force = force
        self.force_scale = force_scale
        self.head_length = head_length
        self.head_width = head_width
        self.thickness = thickness
        self.__color = color
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)

        # stack ontop members
        self.setZValue(-1)

    @property
    def offset(self) -> QPointF:
        """Gets the location the joint item it is attached to."""
        offset = self.getConnection(id(self.force.joint)).scenePos()
        return offset

    def shape(self) -> QPainterPath:
        """Return shape of force item."""
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
        """Return bounding rect of force."""
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
        """Paint the force."""
        draw_bound_box = False

        if self.isSelected():
            color = QColor(175, 220, 255)
        else:
            color = QColor(*self.__color)

        path = self.shape()

        painter.setPen(color)
        painter.fillPath(path, color)

        if draw_bound_box:
            painter.drawRect(self.boundingRect())
