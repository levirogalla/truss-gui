# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSplitter, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from widgets.contextmenus.startmenu.startpage import StartPage

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 611)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave.setEnabled(True)
        self.actionSave.setShortcutVisibleInContextMenu(True)
        self.actionedit = QAction(MainWindow)
        self.actionedit.setObjectName(u"actionedit")
        self.actionOpen_Optimizer = QAction(MainWindow)
        self.actionOpen_Optimizer.setObjectName(u"actionOpen_Optimizer")
        self.actionView_in_MPL = QAction(MainWindow)
        self.actionView_in_MPL.setObjectName(u"actionView_in_MPL")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionSolve_Reactions = QAction(MainWindow)
        self.actionSolve_Reactions.setObjectName(u"actionSolve_Reactions")
        self.actionSolve_Members = QAction(MainWindow)
        self.actionSolve_Members.setObjectName(u"actionSolve_Members")
        self.actionOptimize = QAction(MainWindow)
        self.actionOptimize.setObjectName(u"actionOptimize")
        self.actionTruss_Preferences = QAction(MainWindow)
        self.actionTruss_Preferences.setObjectName(u"actionTruss_Preferences")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionOpen_Change_Log = QAction(MainWindow)
        self.actionOpen_Change_Log.setObjectName(u"actionOpen_Change_Log")
        self.actionClear_Reactions = QAction(MainWindow)
        self.actionClear_Reactions.setObjectName(u"actionClear_Reactions")
        self.actionClear_Members = QAction(MainWindow)
        self.actionClear_Members.setObjectName(u"actionClear_Members")
        self.actionDelete_Member = QAction(MainWindow)
        self.actionDelete_Member.setObjectName(u"actionDelete_Member")
        self.actionDelete_Force = QAction(MainWindow)
        self.actionDelete_Force.setObjectName(u"actionDelete_Force")
        self.actionJoint = QAction(MainWindow)
        self.actionJoint.setObjectName(u"actionJoint")
        self.actionMember = QAction(MainWindow)
        self.actionMember.setObjectName(u"actionMember")
        self.actionForce = QAction(MainWindow)
        self.actionForce.setObjectName(u"actionForce")
        self.actionSupport = QAction(MainWindow)
        self.actionSupport.setObjectName(u"actionSupport")
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        self.actionStart = QAction(MainWindow)
        self.actionStart.setObjectName(u"actionStart")
        self.actionGeneral_Settings = QAction(MainWindow)
        self.actionGeneral_Settings.setObjectName(u"actionGeneral_Settings")
        self.actionAddJointDrop = QAction(MainWindow)
        self.actionAddJointDrop.setObjectName(u"actionAddJointDrop")
        self.actionAddJointDialog = QAction(MainWindow)
        self.actionAddJointDialog.setObjectName(u"actionAddJointDialog")
        self.actionAddMember = QAction(MainWindow)
        self.actionAddMember.setObjectName(u"actionAddMember")
        self.actionAddSupport = QAction(MainWindow)
        self.actionAddSupport.setObjectName(u"actionAddSupport")
        self.actionAddForce = QAction(MainWindow)
        self.actionAddForce.setObjectName(u"actionAddForce")
        self.actionZoom_In = QAction(MainWindow)
        self.actionZoom_In.setObjectName(u"actionZoom_In")
        self.actionZoom_Out = QAction(MainWindow)
        self.actionZoom_Out.setObjectName(u"actionZoom_Out")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.controls = QWidget(self.centralwidget)
        self.controls.setObjectName(u"controls")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controls.sizePolicy().hasHeightForWidth())
        self.controls.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.controls)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.verticalLayout.setContentsMargins(10, 0, 0, 0)
        self.editMeshOptions = QGroupBox(self.controls)
        self.editMeshOptions.setObjectName(u"editMeshOptions")
        self.editMeshOptions.setEnabled(True)
        sizePolicy.setHeightForWidth(self.editMeshOptions.sizePolicy().hasHeightForWidth())
        self.editMeshOptions.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.editMeshOptions)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.addJointButton = QPushButton(self.editMeshOptions)
        self.addJointButton.setObjectName(u"addJointButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.addJointButton.sizePolicy().hasHeightForWidth())
        self.addJointButton.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.addJointButton)

        self.addMemberButton = QPushButton(self.editMeshOptions)
        self.addMemberButton.setObjectName(u"addMemberButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.addMemberButton.sizePolicy().hasHeightForWidth())
        self.addMemberButton.setSizePolicy(sizePolicy2)
        self.addMemberButton.setMinimumSize(QSize(0, 0))
        self.addMemberButton.setLayoutDirection(Qt.LeftToRight)
        self.addMemberButton.setAutoFillBackground(False)

        self.verticalLayout_2.addWidget(self.addMemberButton)

        self.addForceButton = QPushButton(self.editMeshOptions)
        self.addForceButton.setObjectName(u"addForceButton")
        sizePolicy1.setHeightForWidth(self.addForceButton.sizePolicy().hasHeightForWidth())
        self.addForceButton.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.addForceButton)

        self.addSupportButton = QPushButton(self.editMeshOptions)
        self.addSupportButton.setObjectName(u"addSupportButton")
        sizePolicy1.setHeightForWidth(self.addSupportButton.sizePolicy().hasHeightForWidth())
        self.addSupportButton.setSizePolicy(sizePolicy1)

        self.verticalLayout_2.addWidget(self.addSupportButton)


        self.verticalLayout.addWidget(self.editMeshOptions)


        self.horizontalLayout.addWidget(self.controls)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.widget_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.verticalLayoutWidget = QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayout_5 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy3)
        self.tabWidget.setMinimumSize(QSize(500, 500))
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideLeft)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.start = StartPage()
        self.start.setObjectName(u"start")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy4)
        self.tabWidget.addTab(self.start, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        self.quickData = QFrame(self.verticalLayoutWidget)
        self.quickData.setObjectName(u"quickData")
        self.quickData.setAutoFillBackground(False)
        self.quickData.setFrameShape(QFrame.NoFrame)
        self.quickData.setFrameShadow(QFrame.Raised)
        self.quickData.setMidLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.quickData)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 2, 10, 0)
        self.label = QLabel(self.quickData)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.widget = QWidget(self.quickData)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.zoomOutButton = QPushButton(self.widget)
        self.zoomOutButton.setObjectName(u"zoomOutButton")

        self.horizontalLayout_3.addWidget(self.zoomOutButton)

        self.zoomInButton = QPushButton(self.widget)
        self.zoomInButton.setObjectName(u"zoomInButton")
        self.zoomInButton.setCheckable(False)
        self.zoomInButton.setAutoDefault(False)
        self.zoomInButton.setFlat(False)

        self.horizontalLayout_3.addWidget(self.zoomInButton)


        self.horizontalLayout_2.addWidget(self.widget)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout_5.addWidget(self.quickData)

        self.splitter.addWidget(self.verticalLayoutWidget)
        self.infoWidget = QWidget(self.splitter)
        self.infoWidget.setObjectName(u"infoWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.infoWidget.sizePolicy().hasHeightForWidth())
        self.infoWidget.setSizePolicy(sizePolicy5)
        self.verticalLayout_4 = QVBoxLayout(self.infoWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(10, 0, 0, 0)
        self.jointInfo = QTableWidget(self.infoWidget)
        if (self.jointInfo.columnCount() < 4):
            self.jointInfo.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.jointInfo.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.jointInfo.setObjectName(u"jointInfo")

        self.verticalLayout_4.addWidget(self.jointInfo)

        self.memberInfo = QTableWidget(self.infoWidget)
        if (self.memberInfo.columnCount() < 5):
            self.memberInfo.setColumnCount(5)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.memberInfo.setHorizontalHeaderItem(4, __qtablewidgetitem8)
        self.memberInfo.setObjectName(u"memberInfo")

        self.verticalLayout_4.addWidget(self.memberInfo)

        self.forceInfo = QTableWidget(self.infoWidget)
        if (self.forceInfo.columnCount() < 5):
            self.forceInfo.setColumnCount(5)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.forceInfo.setHorizontalHeaderItem(4, __qtablewidgetitem13)
        self.forceInfo.setObjectName(u"forceInfo")

        self.verticalLayout_4.addWidget(self.forceInfo)

        self.supportInfo = QTableWidget(self.infoWidget)
        if (self.supportInfo.columnCount() < 6):
            self.supportInfo.setColumnCount(6)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(2, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(3, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(4, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.supportInfo.setHorizontalHeaderItem(5, __qtablewidgetitem19)
        self.supportInfo.setObjectName(u"supportInfo")

        self.verticalLayout_4.addWidget(self.supportInfo)

        self.splitter.addWidget(self.infoWidget)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.widget_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 960, 37))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuOpen_Recent = QMenu(self.menuFile)
        self.menuOpen_Recent.setObjectName(u"menuOpen_Recent")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuDelete = QMenu(self.menuEdit)
        self.menuDelete.setObjectName(u"menuDelete")
        self.menuAdd = QMenu(self.menuEdit)
        self.menuAdd.setObjectName(u"menuAdd")
        self.menuJoint = QMenu(self.menuAdd)
        self.menuJoint.setObjectName(u"menuJoint")
        self.menuSolve = QMenu(self.menubar)
        self.menuSolve.setObjectName(u"menuSolve")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSolve.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuOpen_Recent.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuOpen_Recent.addAction(self.actionStart)
        self.menuEdit.addAction(self.actionedit)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.menuDelete.menuAction())
        self.menuEdit.addAction(self.menuAdd.menuAction())
        self.menuDelete.addAction(self.actionJoint)
        self.menuDelete.addAction(self.actionMember)
        self.menuDelete.addAction(self.actionForce)
        self.menuDelete.addAction(self.actionSupport)
        self.menuAdd.addAction(self.menuJoint.menuAction())
        self.menuAdd.addAction(self.actionAddMember)
        self.menuAdd.addAction(self.actionAddSupport)
        self.menuAdd.addAction(self.actionAddForce)
        self.menuJoint.addAction(self.actionAddJointDrop)
        self.menuJoint.addAction(self.actionAddJointDialog)
        self.menuSolve.addAction(self.actionSolve_Reactions)
        self.menuSolve.addAction(self.actionSolve_Members)
        self.menuSolve.addSeparator()
        self.menuSolve.addAction(self.actionClear_Reactions)
        self.menuSolve.addAction(self.actionClear_Members)
        self.menuSolve.addSeparator()
        self.menuSolve.addAction(self.actionOpen_Optimizer)
        self.menuView.addAction(self.actionView_in_MPL)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionTruss_Preferences)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionZoom_In)
        self.menuView.addAction(self.actionZoom_Out)
        self.menuSettings.addAction(self.actionGeneral_Settings)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.zoomInButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionedit.setText(QCoreApplication.translate("MainWindow", u"Undo", None))
        self.actionOpen_Optimizer.setText(QCoreApplication.translate("MainWindow", u"Open Optimizer...", None))
        self.actionView_in_MPL.setText(QCoreApplication.translate("MainWindow", u"View in MPL", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New Truss", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
#if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSolve_Reactions.setText(QCoreApplication.translate("MainWindow", u"Solve Reactions", None))
        self.actionSolve_Members.setText(QCoreApplication.translate("MainWindow", u"Solve Members", None))
        self.actionOptimize.setText(QCoreApplication.translate("MainWindow", u"Optimize", None))
        self.actionTruss_Preferences.setText(QCoreApplication.translate("MainWindow", u"Truss Preferences", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", u"Redo", None))
        self.actionOpen_Change_Log.setText(QCoreApplication.translate("MainWindow", u"Open Change Log", None))
        self.actionClear_Reactions.setText(QCoreApplication.translate("MainWindow", u"Clear Reactions", None))
        self.actionClear_Members.setText(QCoreApplication.translate("MainWindow", u"Clear Members", None))
        self.actionDelete_Member.setText(QCoreApplication.translate("MainWindow", u"Delete Member...", None))
        self.actionDelete_Force.setText(QCoreApplication.translate("MainWindow", u"Delete Force...", None))
        self.actionJoint.setText(QCoreApplication.translate("MainWindow", u"Joints...", None))
        self.actionMember.setText(QCoreApplication.translate("MainWindow", u"Members...", None))
        self.actionForce.setText(QCoreApplication.translate("MainWindow", u"Forces...", None))
        self.actionSupport.setText(QCoreApplication.translate("MainWindow", u"Supports...", None))
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.actionStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.actionGeneral_Settings.setText(QCoreApplication.translate("MainWindow", u"General Settings...", None))
        self.actionAddJointDrop.setText(QCoreApplication.translate("MainWindow", u"Drop", None))
#if QT_CONFIG(shortcut)
        self.actionAddJointDrop.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+J", None))
#endif // QT_CONFIG(shortcut)
        self.actionAddJointDialog.setText(QCoreApplication.translate("MainWindow", u"Dialog...", None))
#if QT_CONFIG(shortcut)
        self.actionAddJointDialog.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+Shift+J", None))
#endif // QT_CONFIG(shortcut)
        self.actionAddMember.setText(QCoreApplication.translate("MainWindow", u"Member", None))
#if QT_CONFIG(shortcut)
        self.actionAddMember.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+M", None))
#endif // QT_CONFIG(shortcut)
        self.actionAddSupport.setText(QCoreApplication.translate("MainWindow", u"Support", None))
#if QT_CONFIG(shortcut)
        self.actionAddSupport.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionAddForce.setText(QCoreApplication.translate("MainWindow", u"Force", None))
#if QT_CONFIG(shortcut)
        self.actionAddForce.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionZoom_In.setText(QCoreApplication.translate("MainWindow", u"Zoom In", None))
#if QT_CONFIG(shortcut)
        self.actionZoom_In.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+=", None))
#endif // QT_CONFIG(shortcut)
        self.actionZoom_Out.setText(QCoreApplication.translate("MainWindow", u"Zoom Out", None))
#if QT_CONFIG(shortcut)
        self.actionZoom_Out.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+-", None))
#endif // QT_CONFIG(shortcut)
        self.editMeshOptions.setTitle(QCoreApplication.translate("MainWindow", u"Edit Mesh", None))
        self.addJointButton.setText(QCoreApplication.translate("MainWindow", u"Add Joint", None))
        self.addMemberButton.setText(QCoreApplication.translate("MainWindow", u"Add Member", None))
        self.addForceButton.setText(QCoreApplication.translate("MainWindow", u"Add Force", None))
        self.addSupportButton.setText(QCoreApplication.translate("MainWindow", u"Add Support", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.start), QCoreApplication.translate("MainWindow", u"Start", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Truss Maker v0.0.0", None))
        self.zoomOutButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.zoomInButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        ___qtablewidgetitem = self.jointInfo.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Joint", None));
        ___qtablewidgetitem1 = self.jointInfo.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"X", None));
        ___qtablewidgetitem2 = self.jointInfo.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Y", None));
        ___qtablewidgetitem3 = self.jointInfo.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Movable", None));
        ___qtablewidgetitem4 = self.memberInfo.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Member", None));
        ___qtablewidgetitem5 = self.memberInfo.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Joint A", None));
        ___qtablewidgetitem6 = self.memberInfo.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Joint B", None));
        ___qtablewidgetitem7 = self.memberInfo.horizontalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Internal Force", None));
        ___qtablewidgetitem8 = self.memberInfo.horizontalHeaderItem(4)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Force Type", None));
        ___qtablewidgetitem9 = self.forceInfo.horizontalHeaderItem(0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Force", None));
        ___qtablewidgetitem10 = self.forceInfo.horizontalHeaderItem(1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Joint", None));
        ___qtablewidgetitem11 = self.forceInfo.horizontalHeaderItem(2)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"X Component", None));
        ___qtablewidgetitem12 = self.forceInfo.horizontalHeaderItem(3)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Y Component", None));
        ___qtablewidgetitem13 = self.forceInfo.horizontalHeaderItem(4)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Type", None));
        ___qtablewidgetitem14 = self.supportInfo.horizontalHeaderItem(0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Support", None));
        ___qtablewidgetitem15 = self.supportInfo.horizontalHeaderItem(1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Joint", None));
        ___qtablewidgetitem16 = self.supportInfo.horizontalHeaderItem(2)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Base", None));
        ___qtablewidgetitem17 = self.supportInfo.horizontalHeaderItem(3)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"X Reaction", None));
        ___qtablewidgetitem18 = self.supportInfo.horizontalHeaderItem(4)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Y  Reaction", None));
        ___qtablewidgetitem19 = self.supportInfo.horizontalHeaderItem(5)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Moment Reaction", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOpen_Recent.setTitle(QCoreApplication.translate("MainWindow", u"Open Recent", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuDelete.setTitle(QCoreApplication.translate("MainWindow", u"Manage", None))
        self.menuAdd.setTitle(QCoreApplication.translate("MainWindow", u"Add", None))
        self.menuJoint.setTitle(QCoreApplication.translate("MainWindow", u"Joint", None))
        self.menuSolve.setTitle(QCoreApplication.translate("MainWindow", u"Solve", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

