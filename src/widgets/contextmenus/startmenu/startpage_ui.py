# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'startpage.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_StartPage(object):
    def setupUi(self, StartPage):
        if not StartPage.objectName():
            StartPage.setObjectName(u"StartPage")
        StartPage.resize(459, 454)
        self.verticalLayout = QVBoxLayout(StartPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.welcomLabel = QLabel(StartPage)
        self.welcomLabel.setObjectName(u"welcomLabel")

        self.verticalLayout.addWidget(self.welcomLabel)

        self.line = QFrame(StartPage)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.newLabel = QLabel(StartPage)
        self.newLabel.setObjectName(u"newLabel")

        self.horizontalLayout.addWidget(self.newLabel)

        self.newButton = QPushButton(StartPage)
        self.newButton.setObjectName(u"newButton")

        self.horizontalLayout.addWidget(self.newButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.openLabel = QLabel(StartPage)
        self.openLabel.setObjectName(u"openLabel")

        self.horizontalLayout_2.addWidget(self.openLabel)

        self.openButton = QPushButton(StartPage)
        self.openButton.setObjectName(u"openButton")

        self.horizontalLayout_2.addWidget(self.openButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.docsLabel = QLabel(StartPage)
        self.docsLabel.setObjectName(u"docsLabel")

        self.horizontalLayout_3.addWidget(self.docsLabel)

        self.docsButton = QPushButton(StartPage)
        self.docsButton.setObjectName(u"docsButton")

        self.horizontalLayout_3.addWidget(self.docsButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(StartPage)

        QMetaObject.connectSlotsByName(StartPage)
    # setupUi

    def retranslateUi(self, StartPage):
        StartPage.setWindowTitle(QCoreApplication.translate("StartPage", u"Start Page", None))
        self.welcomLabel.setText(QCoreApplication.translate("StartPage", u"Welcome to Trussty!", None))
        self.newLabel.setText(QCoreApplication.translate("StartPage", u"Create a new truss:", None))
        self.newButton.setText(QCoreApplication.translate("StartPage", u"New", None))
        self.openLabel.setText(QCoreApplication.translate("StartPage", u"Open a truss:", None))
        self.openButton.setText(QCoreApplication.translate("StartPage", u"Open", None))
        self.docsLabel.setText(QCoreApplication.translate("StartPage", u"See the docs:", None))
        self.docsButton.setText(QCoreApplication.translate("StartPage", u"Help", None))
    # retranslateUi

