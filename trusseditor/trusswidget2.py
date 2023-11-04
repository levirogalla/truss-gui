import copy


from pytruss import Mesh, Member, Force, Joint, Support
from torch import optim

from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget,  QGraphicsScene, QGraphicsView, QMenu
from PyQt6.QtCore import QEvent, QPointF, Qt, pyqtSignal, QRectF, QThread, QLineF
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QColor, QPainterPath, QBrush
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGestureEvent, QPinchGesture

from .forms.supports.supports import SupportForm
from .forms.forces.forces import ForceForm
from .saveopen import SavedTruss, DEFAULT_OPTIMIZATION_SETTINGS, DEFAULT_VIEW_PREFERENCES
from .forms.jointmenu.jointmenu import JointMenu


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
        if a0.button() == Qt.MouseButton.LeftButton:
            self.__dragging_mode = True
            self.offset = a0.pos()
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            self.setSelected(False)
            self.scene().update()
            self.scene().views()[0].interacted.emit()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.__dragging_mode:
                self.__dragging = True
                self.offset = event.pos()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
            else:
                self.setSelected(not self.isSelected())
            self.scene().update()
            self.scene().views()[0].interacted.emit()

        if event.button() == Qt.MouseButton.RightButton:
            menu = JointMenu(self.scene().views()[0], self)
            menu.exec(self.scene().views()[
                      0].mapToGlobal(self.scene().views()[
                          0].mapFromScene(self.scenePos())))

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
            self.scene().views()[0].interacted.emit()

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
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
        rect = QRectF(-self.r/2, 0, self.r, self.r)
        return rect.translated(self.offset)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        draw_bound_box = False

        # self.setPos(self.mapToScene(self.support.joint.x_coordinate,
        #             self.convertCordinate(self.support.joint.y_coordinate)))

        if self.isSelected():
            color = QColor(175, 220, 255)
        else:
            color = QColor(*self.__color)

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
            color = QColor(*self.__color)

        path = self.shape()

        painter.setPen(color)
        painter.fillPath(path, color)

        if draw_bound_box:
            painter.drawRect(self.boundingRect())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self.setSelected(not self.isSelected())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        pass


class TrainThread(QThread):
    """Class for optimizing truss on seperate cpu thread."""
    finished = pyqtSignal()

    def __init__(self, truss: Mesh, settings: dict) -> None:
        super().__init__()
        self.settings = settings
        self.truss = truss
        if settings["optimizer"] == "SGD":
            self.optimizer = optim.SGD
        elif settings["optimizer"] == "Adam":
            self.optimizer = optim.Adam

    def run(self) -> None:
        settings = self.settings
        self.truss.optimize_cost(
            member_cost=settings["member_cost"],
            joint_cost=settings["joint_cost"],
            lr=settings["lr"],
            epochs=settings["epochs"],
            optimizer=self.optimizer,
            print_mesh=False,
            show_at_epoch=False,
            min_member_length=settings["min_member_length"],
            max_member_length=settings["max_member_length"],
            max_tensile_force=settings["max_tensile_force"],
            max_compresive_force=settings["max_compressive_force"],
            constriant_agression=settings["constraint_aggression"],
            progress_bar=True,
            show_metrics=False,
            update_metrics_interval=settings["update_metrics_interval"],
        )
        self.finished.emit()


class TrussWidget(QGraphicsView):
    """Class for the truss graphics view."""
    interacted = pyqtSignal()
    joint_added = pyqtSignal()
    member_added = pyqtSignal()
    support_added = pyqtSignal()
    force_added = pyqtSignal()

    def __init__(self, file: str = None) -> None:
        super().__init__()
        # settings
        self.truss_optimization_settings = copy.copy(
            DEFAULT_OPTIMIZATION_SETTINGS)
        self.truss_view_preferences = copy.copy(DEFAULT_VIEW_PREFERENCES)

        self.truss = Mesh()
        self.file = file
        self.truss_scene = QGraphicsScene(self)
        self.grabGesture(Qt.GestureType.PinchGesture)
        self.setScene(self.truss_scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setTransformationAnchor(self.ViewportAnchor.AnchorUnderMouse)
        self.setMouseTracking(False)
        self.connections = dict()
        self.preview_joint = PreviewJointItem(
            self.truss_view_preferences["joint_radius"])
        self.scene().addItem(self.preview_joint)
        self.preview_joint.hide()
        self.forms: set[QWidget] = set()
        self.setMouseTracking(True)
        self.showing_preview_joint = False

        # origin lines
        self.origin = {
            self.scene().addLine(
                QLineF(0, self.width()/2, 0, -self.width()/2)),
            self.scene().addLine(
                QLineF(self.width()/2, 0, -self.width()/2, 0))
        }

        # track changes made
        self.edits = []
        self.scale(10, 10)
        self.updateOrigin()
        self.loadTrussWidgetFromMesh(load_from_file=True)

    def updateOrigin(self, draw_new=False) -> None:
        """Update the size of the origin relative to zoom."""

        view_size = 1/self.transform().m11() * self.sceneRect().width()

        if self.width() < self.height():
            pen = QPen(QColor(0, 0, 0), view_size*0.005)
        else:
            pen = QPen(QColor(0, 0, 0), view_size*0.005)

        if not draw_new:
            self.scene().removeItem(self.origin.pop())
            self.scene().removeItem(self.origin.pop())

        h_line = self.scene().addLine(
            QLineF(view_size/15, 0, -view_size/15, 0), pen
        )
        v_line = self.scene().addLine(
            QLineF(0, view_size/15, 0, -view_size/15), pen
        )
        h_line.setZValue(100)
        v_line.setZValue(100)

        self.origin = {
            h_line,
            v_line
        }

    def saveTruss(self, optional_suffix="") -> None:
        """Save truss."""
        save_object = SavedTruss(
            self.truss, self.truss_optimization_settings, self.truss_view_preferences)
        save_object.save(self.file, optional_suffix)
        self.edits.clear()

    def __clearScene(self) -> None:
        """Clears all truss items of scene. Everything must be redrawn after this."""
        self.scene().clear()
        self.connections.clear()
        self.preview_joint = PreviewJointItem(
            self.truss_view_preferences["joint_radius"])
        self.scene().addItem(self.preview_joint)
        self.updateOrigin(draw_new=True)
        self.preview_joint.hide()

    def loadTrussWidgetFromMesh(self, load_from_file: bool = True) -> None:
        """Clears all current truss items and redraws them either from a file or from memory."""

        # delete all existing items on scene
        self.__clearScene()

        if load_from_file and self.file is not None:
            saved_truss = SavedTruss.load(self.file)
            self.truss = saved_truss.truss
            self.truss_optimization_settings = saved_truss.optimization_settings
            self.truss_view_preferences = saved_truss.view_preferences

        # maybe make function to add widget to scene since its used a lot
        for joint in self.truss.joints:
            joint_widget = JointItem(
                joint,
                self.truss_view_preferences["joint_radius"],
                False,
                self.truss_view_preferences["joint_color"],
                self.truss_view_preferences["joint_focused_color"])

            self.connections[id(joint)] = joint_widget
            self.scene().addItem(self.connections[id(joint)])

        for member in self.truss.members:
            member_widget = MemberItem(
                self.truss_view_preferences["member_size"],
                member,
                self.truss_view_preferences["member_color"]
            )
            self.connections[id(member)] = member_widget
            self.scene().addItem(self.connections[id(member)])

        for support in self.truss.supports:
            support_widget = SupportItem(
                self.truss_view_preferences["support_size"],
                support,
                self.truss_view_preferences["support_color"]
            )
            self.connections[id(support)] = support_widget
            self.scene().addItem(self.connections[id(support)])

        for force in self.truss.forces:
            force_widget = ForceItem(
                force,
                self.truss_view_preferences["member_size"],
                self.truss_view_preferences["scale_factor"],
                self.truss_view_preferences["force_head_width"],
                self.truss_view_preferences["force_head_length"],
                self.truss_view_preferences["force_color"]
            )
            self.connections[id(force)] = force_widget
            self.scene().addItem(self.connections[id(force)])

        self.scene().update()
        self.interacted.emit()

    def event(self, event: QEvent | None) -> bool:
        if event.type() == QEvent.Type.Gesture:
            self.gestureEvent(event)
        return super().event(event)

    def gestureEvent(self, event: QGestureEvent) -> None:
        if isinstance(event.gesture(Qt.GestureType.PinchGesture), QPinchGesture):
            self.pinchTriggered(event.gesture(Qt.GestureType.PinchGesture))

    def pinchTriggered(self, gesture: QPinchGesture) -> None:
        """Scale the view from pinch gesture."""
        scale_factor = gesture.scaleFactor()
        self.scale(scale_factor, scale_factor)
        self.updateOrigin()

    def previewJoint(self) -> None:
        """Show the preview joint. This is the first function to be called when attempting to add a joint."""
        self.showing_preview_joint = True
        self.preview_joint.show()
        self.interacted.emit()

    def mouseMoveEvent(self, event: QMouseEvent | None) -> None:
        if self.showing_preview_joint:
            self.preview_joint.setPos(self.mapToScene(event.pos()))
            self.preview_joint.updateCartesianLocation()
            self.scene().update()
            self.interacted.emit()
        return super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        # if preview joint is showing add a joint at that location and hid preview
        if self.showing_preview_joint:
            self.showing_preview_joint = False
            self.preview_joint.hide()
            self.addJoint(self.preview_joint.joint)
            return
        super().mousePressEvent(event)
        self.interacted.emit()

    def addJoint(self, joint: Joint) -> None:
        """Adds the joint to the pytruss mesh and the Qt Scene at the location of the preview joint."""
        temp = Joint(0, 10+1e-5)
        new_joint = Joint(joint.x_coordinate, joint.y_coordinate, True)
        mem = Member(temp, new_joint)
        self.truss.add_member(mem)
        self.truss.delete_joint(temp)

        item = JointItem(
            new_joint,
            self.truss_view_preferences["joint_radius"],
            False,
            self.truss_view_preferences["joint_color"],
            self.truss_view_preferences["joint_focused_color"]
        )
        self.connections[id(new_joint)] = item
        self.scene().addItem(item)
        self.joint_added.emit()
        self.interacted.emit()
        self.edits.append("Joint added")

    def deleteJoint(self, joint: Joint) -> None:
        joint_item: JointItem = self.connections[id(joint)]

        for mem in joint.members:
            mem_item: MemberItem = self.connections[id(mem)]
            self.connections.pop(id(mem))
            self.scene().removeItem(mem_item)

        for force in joint.forces:
            force_item: ForceItem = self.connections[id(force)]
            self.connections.pop(id((force)))
            self.scene().removeItem(force_item)

        if joint.support is not None:
            sup_item: SupportItem = self.connections[id((joint.support))]
            self.connections.pop(id(joint.support))
            self.scene().removeItem(sup_item)

        self.connections.pop(id(joint))
        self.truss.delete_joint(joint)
        self.scene().removeItem(joint_item)
        self.interacted.emit()

    def addMember(self) -> None:
        """Adds a member for every combination of the selected joints."""
        visted: set[Joint] = set()
        items = self.scene().selectedItems()
        for j1 in items:
            for j2 in items:
                if isinstance(j1, JointItem) and isinstance(j2, JointItem):
                    if j1.joint != j2.joint and j2.joint not in visted:
                        member = Member(j1.joint, j2.joint)
                        self.truss.add_member(member)
                        item = MemberItem(
                            self.truss_view_preferences["member_size"],
                            member,
                            self.truss_view_preferences["member_color"]
                        )
                        self.connections[id(member)] = item
                        self.scene().addItem(item)
            visted.add(j1.joint)
        self.scene().clearSelection()
        self.member_added.emit()
        self.interacted.emit()
        self.edits.append("Member added")

    def deleteMember(self, member: Member):
        member_item: MemberItem = self.connections[id(member)]
        self.scene().removeItem(member_item)
        self.truss.delete_member(member)
        self.connections.pop(id(member))
        self.interacted.emit()

    def destroyForm(self, form: QWidget) -> None:
        """Destroys a form."""
        self.forms.remove(form)
        for joint_item in self.findChildren(JointItem):
            joint_item: JointItem
            joint_item.setSelected(False)

        self.interacted.emit()

    def addSupport(self, joint, support_type: str) -> None:
        """Callback function to handle selection of joint type."""
        def addSupportDetails(support: Support):
            """Callback function to add the support to the joint and truss."""
            self.truss.add_support(support)
            supWidg = SupportItem(
                self.truss_view_preferences["support_size"],
                support,
                self.truss_view_preferences["support_color"]
            )
            self.connections[id(support)] = supWidg
            self.scene().addItem(supWidg)
            self.support_added.emit()
            self.edits.append(f"{support} added")
            self.interacted.emit()

        if support_type == "Fixed Pin":
            support = Support(joint, "p")
            addSupportDetails(support)

        elif support_type == "Roller Pin":
            support = Support(joint, "rp")
            addSupportDetails(support)

        elif support_type == "Fixed":
            support = Support(joint, "f")
            addSupportDetails(support)

        else:
            print(ValueError(
                f"Support type {support_type} not recognised"))

    def deleteSupport(self, support: Force):
        support_item: SupportItem = self.connections[id(support)]
        self.connections.pop(id(support))
        self.truss.delete_support(support)
        self.scene().removeItem(support_item)
        self.interacted.emit()

    def supportForm(self) -> None:
        """Handles the add support form."""

        no_selected_joints = True
        for selected_joint in self.scene().selectedItems():
            if isinstance(selected_joint, JointItem):
                joint, support_type = SupportForm.get_support(
                    self.truss.joints, selected_joint.joint)
                self.addSupport(joint, support_type)
                no_selected_joints = False
                selected_joint.clearModes()

        if no_selected_joints:
            joint, support_type = SupportForm.get_support(
                self.truss.joints, None)
            self.addSupport(joint, support_type)

    def addForce(self, force: Force) -> None:
        """Callback function to add the force to the joint and truss."""
        self.truss.apply_force(force)
        force_item = ForceItem(
            force,
            self.truss_view_preferences["member_size"],
            self.truss_view_preferences["scale_factor"],
            self.truss_view_preferences["force_head_width"],
            self.truss_view_preferences["force_head_length"],
            self.truss_view_preferences["force_color"]
        )
        self.connections[id(force)] = force_item
        self.scene().addItem(force_item)
        self.force_added.emit()
        self.edits.append(f"{force} added")
        self.interacted.emit()

    def deleteForce(self, force: Force):
        force_item: ForceItem = self.connections[id(force)]
        self.connections.pop(id(force))
        self.truss.delete_force(force)
        self.scene().removeItem(force_item)
        self.interacted.emit()

    def forceForm(self) -> None:
        """Handle the force form."""

        no_selected_joints = True
        for selected_joint in self.scene().selectedItems():
            if isinstance(selected_joint, JointItem):
                force = ForceForm.get_force(
                    self.truss.joints, selected_joint.joint)
                self.addForce(force)
                no_selected_joints = False
                selected_joint.clearModes()

        if no_selected_joints:
            force = ForceForm.get_force(
                self.truss.joints, None)
            self.addForce(force)

    def resetViewSettings(self) -> None:
        """Resets the view settings."""
        self.truss_view_preferences = copy.copy(DEFAULT_VIEW_PREFERENCES)
        self.interacted.emit()

    def resetOptimizationSettings(self) -> None:
        """Resets the optimization settings."""
        self.truss_optimization_settings = copy.copy(
            DEFAULT_OPTIMIZATION_SETTINGS)
        self.interacted.emit()
