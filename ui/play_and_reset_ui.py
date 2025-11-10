# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'play_and_reset.ui'
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
    QWidget)

class Ui_w_play_and_reset(object):
    def setupUi(self, w_play_and_reset):
        if not w_play_and_reset.objectName():
            w_play_and_reset.setObjectName(u"w_play_and_reset")
        w_play_and_reset.resize(681, 494)
        w_play_and_reset.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(w_play_and_reset)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_play = QPushButton(w_play_and_reset)
        self.pb_play.setObjectName(u"pb_play")
        self.pb_play.setStyleSheet(u"QPushButton {\n"
"    background-color: #2B5DD1;\n"
"    color: #FFFFFF;\n"
"    border-style: outset;\n"
"    padding: 2px;\n"
"    font: bold 20px;\n"
"    border-width: 6px;\n"
"    border-radius: 10px;\n"
"    border-color: #2752B8;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgreen;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: blue;\n"
"}")

        self.horizontalLayout.addWidget(self.pb_play)

        self.pb_reset = QPushButton(w_play_and_reset)
        self.pb_reset.setObjectName(u"pb_reset")
        self.pb_reset.setStyleSheet(u"QPushButton {\n"
"    background-color: #2B5DD1;\n"
"    color: #FFFFFF;\n"
"    border-style: outset;\n"
"    padding: 2px;\n"
"    font: bold 20px;\n"
"    border-width: 6px;\n"
"    border-radius: 10px;\n"
"    border-color: #2752B8;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgreen;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: blue;\n"
"}")

        self.horizontalLayout.addWidget(self.pb_reset)


        self.retranslateUi(w_play_and_reset)

        QMetaObject.connectSlotsByName(w_play_and_reset)
    # setupUi

    def retranslateUi(self, w_play_and_reset):
        w_play_and_reset.setWindowTitle(QCoreApplication.translate("w_play_and_reset", u"Form", None))
        self.pb_play.setText(QCoreApplication.translate("w_play_and_reset", u"Play", None))
        self.pb_reset.setText(QCoreApplication.translate("w_play_and_reset", u"Reset Animation and Sliders", None))
    # retranslateUi

