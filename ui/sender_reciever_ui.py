# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sender_reciever.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_w_sender_reciever(object):
    def setupUi(self, w_sender_reciever):
        if not w_sender_reciever.objectName():
            w_sender_reciever.setObjectName(u"w_sender_reciever")
        w_sender_reciever.resize(794, 284)
        w_sender_reciever.setAutoFillBackground(False)
        self.horizontalLayout = QHBoxLayout(w_sender_reciever)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_sender = QPushButton(w_sender_reciever)
        self.pb_sender.setObjectName(u"pb_sender")
        self.pb_sender.setStyleSheet(u"QPushButton#pb_sender {\n"
"    background-color: lightgreen;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton#pb_sender:pressed {\n"
"    background-color: rgb(0, 224, 0);\n"
"    border-style: inset;\n"
"}")

        self.horizontalLayout.addWidget(self.pb_sender)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pb_reciever = QPushButton(w_sender_reciever)
        self.pb_reciever.setObjectName(u"pb_reciever")
        self.pb_reciever.setStyleSheet(u"QPushButton#pb_reciever {\n"
"    background-color: orange;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"")

        self.horizontalLayout.addWidget(self.pb_reciever)


        self.retranslateUi(w_sender_reciever)

        QMetaObject.connectSlotsByName(w_sender_reciever)
    # setupUi

    def retranslateUi(self, w_sender_reciever):
        w_sender_reciever.setWindowTitle(QCoreApplication.translate("w_sender_reciever", u"Sender_Reciever", None))
        self.pb_sender.setText(QCoreApplication.translate("w_sender_reciever", u"Packet #", None))
        self.pb_reciever.setText(QCoreApplication.translate("w_sender_reciever", u"Receiver", None))
    # retranslateUi

