import copy


from pytruss import Mesh, Member, Force, Joint, Support
from torch import optim

from PyQt6.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget,  QGraphicsScene, QGraphicsView, QMenu
from PyQt6.QtCore import QEvent, QPointF, Qt, pyqtSignal, QRectF, QThread, QLineF
from PyQt6.QtGui import QMouseEvent, QPainter, QPen, QPaintEvent, QColor, QPainterPath, QBrush
from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGestureEvent, QPinchGesture

from dialogs.addsupport.addsupport import AddSupportDialog
from dialogs.addforce.addforce import AddForceDialog
from utils.saveopen import SavedTruss, DEFAULT_OPTIMIZATION_SETTINGS, DEFAULT_VIEW_PREFERENCES
from widgets.contextmenus.jointmenu.jointmenu import JointMenu
from widgets.trussview.graphicsitems import JointItem, MemberItem, PreviewJointItem, ForceItem, SupportItem


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
            try:
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
            except ValueError:
                print("Joint has a support already.")

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
                joint, support_type = AddSupportDialog.get_support(
                    self.truss.joints, selected_joint.joint)
                self.addSupport(joint, support_type)
                no_selected_joints = False
                selected_joint.clearModes()

        if no_selected_joints:
            joint, support_type = AddSupportDialog.get_support(
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
                force = AddForceDialog.get_force(
                    self.truss.joints, selected_joint.joint)
                self.addForce(force)
                no_selected_joints = False
                selected_joint.clearModes()

        if no_selected_joints:
            force = AddForceDialog.get_force(
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