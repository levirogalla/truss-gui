# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'optimize.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(645, 478)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.optimize = QWidget()
        self.optimize.setObjectName(u"optimize")
        self.verticalLayout_3 = QVBoxLayout(self.optimize)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.trainingControls = QGroupBox(self.optimize)
        self.trainingControls.setObjectName(u"trainingControls")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trainingControls.sizePolicy().hasHeightForWidth())
        self.trainingControls.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.trainingControls)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.controlButton = QHBoxLayout()
        self.controlButton.setObjectName(u"controlButton")
        self.startButton = QPushButton(self.trainingControls)
        self.startButton.setObjectName(u"startButton")

        self.controlButton.addWidget(self.startButton)

        self.stopButton = QPushButton(self.trainingControls)
        self.stopButton.setObjectName(u"stopButton")

        self.controlButton.addWidget(self.stopButton)

        self.saveButton = QPushButton(self.trainingControls)
        self.saveButton.setObjectName(u"saveButton")

        self.controlButton.addWidget(self.saveButton)


        self.verticalLayout_4.addLayout(self.controlButton)

        self.progressBar = QProgressBar(self.trainingControls)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setMinimumSize(QSize(0, 0))
        self.progressBar.setValue(0)
        self.progressBar.setOrientation(Qt.Horizontal)

        self.verticalLayout_4.addWidget(self.progressBar)


        self.verticalLayout_3.addWidget(self.trainingControls)

        self.tabWidget.addTab(self.optimize, "")
        self.settings = QWidget()
        self.settings.setObjectName(u"settings")
        self.verticalLayout = QVBoxLayout(self.settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.trainingSetting = QWidget(self.settings)
        self.trainingSetting.setObjectName(u"trainingSetting")
        self.horizontalLayout = QHBoxLayout(self.trainingSetting)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.optimizationSettings = QGroupBox(self.trainingSetting)
        self.optimizationSettings.setObjectName(u"optimizationSettings")
        self.formLayout_2 = QFormLayout(self.optimizationSettings)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.epochsLabel = QLabel(self.optimizationSettings)
        self.epochsLabel.setObjectName(u"epochsLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.epochsLabel)

        self.epochsSpinBox = QSpinBox(self.optimizationSettings)
        self.epochsSpinBox.setObjectName(u"epochsSpinBox")
        self.epochsSpinBox.setMaximum(999999999)
        self.epochsSpinBox.setSingleStep(100)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.epochsSpinBox)

        self.updateMetricsIntervalLabel = QLabel(self.optimizationSettings)
        self.updateMetricsIntervalLabel.setObjectName(u"updateMetricsIntervalLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.updateMetricsIntervalLabel)

        self.updateMetricsIntervalSpinBox = QSpinBox(self.optimizationSettings)
        self.updateMetricsIntervalSpinBox.setObjectName(u"updateMetricsIntervalSpinBox")
        self.updateMetricsIntervalSpinBox.setMaximum(999999999)
        self.updateMetricsIntervalSpinBox.setSingleStep(10)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.updateMetricsIntervalSpinBox)

        self.constraintAggressionLabel = QLabel(self.optimizationSettings)
        self.constraintAggressionLabel.setObjectName(u"constraintAggressionLabel")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.constraintAggressionLabel)

        self.constraintAggressionLineEdit = QLineEdit(self.optimizationSettings)
        self.constraintAggressionLineEdit.setObjectName(u"constraintAggressionLineEdit")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.constraintAggressionLineEdit)

        self.learningRateLabel = QLabel(self.optimizationSettings)
        self.learningRateLabel.setObjectName(u"learningRateLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.learningRateLabel)

        self.learningRateLineEdit = QLineEdit(self.optimizationSettings)
        self.learningRateLineEdit.setObjectName(u"learningRateLineEdit")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.learningRateLineEdit)

        self.optimizerLabel = QLabel(self.optimizationSettings)
        self.optimizerLabel.setObjectName(u"optimizerLabel")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.optimizerLabel)

        self.optimizerComboBox = QComboBox(self.optimizationSettings)
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.addItem("")
        self.optimizerComboBox.setObjectName(u"optimizerComboBox")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.optimizerComboBox)

        self.frameRateLabel = QLabel(self.optimizationSettings)
        self.frameRateLabel.setObjectName(u"frameRateLabel")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.frameRateLabel)

        self.frameRateSpinBox = QSpinBox(self.optimizationSettings)
        self.frameRateSpinBox.setObjectName(u"frameRateSpinBox")
        self.frameRateSpinBox.setMaximum(30)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.frameRateSpinBox)


        self.horizontalLayout.addWidget(self.optimizationSettings)

        self.constraintSettings = QGroupBox(self.trainingSetting)
        self.constraintSettings.setObjectName(u"constraintSettings")
        self.formLayout = QFormLayout(self.constraintSettings)
        self.formLayout.setObjectName(u"formLayout")
        self.memberCostLabel = QLabel(self.constraintSettings)
        self.memberCostLabel.setObjectName(u"memberCostLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.memberCostLabel)

        self.memberCostLineEdit = QLineEdit(self.constraintSettings)
        self.memberCostLineEdit.setObjectName(u"memberCostLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.memberCostLineEdit)

        self.jointCostLabel = QLabel(self.constraintSettings)
        self.jointCostLabel.setObjectName(u"jointCostLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.jointCostLabel)

        self.jointCostLineEdit = QLineEdit(self.constraintSettings)
        self.jointCostLineEdit.setObjectName(u"jointCostLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.jointCostLineEdit)

        self.minMemberLenghtLabel = QLabel(self.constraintSettings)
        self.minMemberLenghtLabel.setObjectName(u"minMemberLenghtLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.minMemberLenghtLabel)

        self.minMemberLenghtLineEdit = QLineEdit(self.constraintSettings)
        self.minMemberLenghtLineEdit.setObjectName(u"minMemberLenghtLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.minMemberLenghtLineEdit)

        self.maxMemberLengthLabel = QLabel(self.constraintSettings)
        self.maxMemberLengthLabel.setObjectName(u"maxMemberLengthLabel")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.maxMemberLengthLabel)

        self.maxMemberLengthLineEdit = QLineEdit(self.constraintSettings)
        self.maxMemberLengthLineEdit.setObjectName(u"maxMemberLengthLineEdit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.maxMemberLengthLineEdit)

        self.maxTensileForceLabel = QLabel(self.constraintSettings)
        self.maxTensileForceLabel.setObjectName(u"maxTensileForceLabel")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.maxTensileForceLabel)

        self.maxTensileForceLineEdit = QLineEdit(self.constraintSettings)
        self.maxTensileForceLineEdit.setObjectName(u"maxTensileForceLineEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.maxTensileForceLineEdit)

        self.maxCompressiveForceLabel = QLabel(self.constraintSettings)
        self.maxCompressiveForceLabel.setObjectName(u"maxCompressiveForceLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.maxCompressiveForceLabel)

        self.maxCompressiveForceLineEdit = QLineEdit(self.constraintSettings)
        self.maxCompressiveForceLineEdit.setObjectName(u"maxCompressiveForceLineEdit")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.maxCompressiveForceLineEdit)


        self.horizontalLayout.addWidget(self.constraintSettings)


        self.verticalLayout.addWidget(self.trainingSetting)

        self.otherSettings = QGroupBox(self.settings)
        self.otherSettings.setObjectName(u"otherSettings")
        self.otherSettings.setFlat(False)
        self.otherSettings.setCheckable(False)
        self.verticalLayout_5 = QVBoxLayout(self.otherSettings)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(12, 12, 12, 12)
        self.saveSettings = QHBoxLayout()
#ifndef Q_OS_MAC
        self.saveSettings.setSpacing(-1)
#endif
        self.saveSettings.setObjectName(u"saveSettings")
        self.saveFrequencyLabel = QLabel(self.otherSettings)
        self.saveFrequencyLabel.setObjectName(u"saveFrequencyLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.saveFrequencyLabel.sizePolicy().hasHeightForWidth())
        self.saveFrequencyLabel.setSizePolicy(sizePolicy2)

        self.saveSettings.addWidget(self.saveFrequencyLabel)

        self.saveFrequencySpinBox = QSpinBox(self.otherSettings)
        self.saveFrequencySpinBox.setObjectName(u"saveFrequencySpinBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.saveFrequencySpinBox.sizePolicy().hasHeightForWidth())
        self.saveFrequencySpinBox.setSizePolicy(sizePolicy3)
        self.saveFrequencySpinBox.setMaximum(999999999)
        self.saveFrequencySpinBox.setSingleStep(100)

        self.saveSettings.addWidget(self.saveFrequencySpinBox)

        self.savePathLabel = QLabel(self.otherSettings)
        self.savePathLabel.setObjectName(u"savePathLabel")
        sizePolicy2.setHeightForWidth(self.savePathLabel.sizePolicy().hasHeightForWidth())
        self.savePathLabel.setSizePolicy(sizePolicy2)

        self.saveSettings.addWidget(self.savePathLabel)

        self.savePathSelection = QLabel(self.otherSettings)
        self.savePathSelection.setObjectName(u"savePathSelection")
        sizePolicy.setHeightForWidth(self.savePathSelection.sizePolicy().hasHeightForWidth())
        self.savePathSelection.setSizePolicy(sizePolicy)
        self.savePathSelection.setAutoFillBackground(True)
        self.savePathSelection.setFrameShape(QFrame.NoFrame)
        self.savePathSelection.setMargin(2)
        self.savePathSelection.setIndent(0)

        self.saveSettings.addWidget(self.savePathSelection)

        self.selectPathButton = QPushButton(self.otherSettings)
        self.selectPathButton.setObjectName(u"selectPathButton")
        sizePolicy3.setHeightForWidth(self.selectPathButton.sizePolicy().hasHeightForWidth())
        self.selectPathButton.setSizePolicy(sizePolicy3)

        self.saveSettings.addWidget(self.selectPathButton)


        self.verticalLayout_5.addLayout(self.saveSettings)

        self.buttonMenu = QHBoxLayout()
        self.buttonMenu.setObjectName(u"buttonMenu")
        self.applySettingsButton = QPushButton(self.otherSettings)
        self.applySettingsButton.setObjectName(u"applySettingsButton")

        self.buttonMenu.addWidget(self.applySettingsButton)

        self.resetSettingsButton = QPushButton(self.otherSettings)
        self.resetSettingsButton.setObjectName(u"resetSettingsButton")

        self.buttonMenu.addWidget(self.resetSettingsButton)


        self.verticalLayout_5.addLayout(self.buttonMenu)


        self.verticalLayout.addWidget(self.otherSettings)

        self.tabWidget.addTab(self.settings, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Optimize", None))
        self.startButton.setText(QCoreApplication.translate("Dialog", u"Start", None))
        self.stopButton.setText(QCoreApplication.translate("Dialog", u"Stop", None))
        self.saveButton.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optimize), QCoreApplication.translate("Dialog", u"Optimize", None))
        self.optimizationSettings.setTitle(QCoreApplication.translate("Dialog", u"Optimization", None))
        self.epochsLabel.setText(QCoreApplication.translate("Dialog", u"Epochs", None))
        self.updateMetricsIntervalLabel.setText(QCoreApplication.translate("Dialog", u"Update Metrics Interval", None))
        self.constraintAggressionLabel.setText(QCoreApplication.translate("Dialog", u"Constraint Aggression", None))
        self.learningRateLabel.setText(QCoreApplication.translate("Dialog", u"Learning Rate", None))
        self.optimizerLabel.setText(QCoreApplication.translate("Dialog", u"Optimizer", None))
        self.optimizerComboBox.setItemText(0, QCoreApplication.translate("Dialog", u"SGD", None))
        self.optimizerComboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Adam", None))

        self.frameRateLabel.setText(QCoreApplication.translate("Dialog", u"Frame Rate", None))
        self.constraintSettings.setTitle(QCoreApplication.translate("Dialog", u"Constraints", None))
        self.memberCostLabel.setText(QCoreApplication.translate("Dialog", u"Member Cost", None))
        self.jointCostLabel.setText(QCoreApplication.translate("Dialog", u"Joint Cost", None))
        self.minMemberLenghtLabel.setText(QCoreApplication.translate("Dialog", u"Min Member Length", None))
        self.maxMemberLengthLabel.setText(QCoreApplication.translate("Dialog", u"Max Member Length", None))
        self.maxTensileForceLabel.setText(QCoreApplication.translate("Dialog", u"Max Tensile Force", None))
        self.maxCompressiveForceLabel.setText(QCoreApplication.translate("Dialog", u"Max Compressive Force", None))
        self.otherSettings.setTitle("")
        self.saveFrequencyLabel.setText(QCoreApplication.translate("Dialog", u"Save Frequency", None))
        self.savePathLabel.setText(QCoreApplication.translate("Dialog", u"Save Path:", None))
        self.savePathSelection.setText("")
        self.selectPathButton.setText(QCoreApplication.translate("Dialog", u"Path...", None))
        self.applySettingsButton.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.resetSettingsButton.setText(QCoreApplication.translate("Dialog", u"Reset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), QCoreApplication.translate("Dialog", u"Settings", None))
    # retranslateUi

