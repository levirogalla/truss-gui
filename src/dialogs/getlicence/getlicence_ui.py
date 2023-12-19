# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'getlicence.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_LicenceDialog(object):
    def setupUi(self, LicenceDialog):
        if not LicenceDialog.objectName():
            LicenceDialog.setObjectName(u"LicenceDialog")
        LicenceDialog.setWindowModality(Qt.ApplicationModal)
        LicenceDialog.resize(402, 134)
        LicenceDialog.setLayoutDirection(Qt.RightToLeft)
        LicenceDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(LicenceDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.licence = QTextEdit(LicenceDialog)
        self.licence.setObjectName(u"licence")

        self.horizontalLayout.addWidget(self.licence)

        self.label = QLabel(LicenceDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.okButton = QPushButton(LicenceDialog)
        self.okButton.setObjectName(u"okButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.okButton.sizePolicy().hasHeightForWidth())
        self.okButton.setSizePolicy(sizePolicy)
        self.okButton.setMinimumSize(QSize(65, 0))
        self.okButton.setLayoutDirection(Qt.RightToLeft)

        self.verticalLayout.addWidget(self.okButton)


        self.retranslateUi(LicenceDialog)

        QMetaObject.connectSlotsByName(LicenceDialog)
    # setupUi

    def retranslateUi(self, LicenceDialog):
        LicenceDialog.setWindowTitle(QCoreApplication.translate("LicenceDialog", u"Licence", None))
        self.label.setText(QCoreApplication.translate("LicenceDialog", u"Licence Key", None))
        self.okButton.setText(QCoreApplication.translate("LicenceDialog", u"Ok", None))
    # retranslateUi

