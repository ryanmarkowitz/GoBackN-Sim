# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
    QSizePolicy, QSlider, QSpinBox, QWidget)

class Ui_w_settings(object):
    def setupUi(self, w_settings):
        if not w_settings.objectName():
            w_settings.setObjectName(u"w_settings")
        w_settings.resize(935, 245)
        font = QFont()
        font.setFamilies([u"Standard Symbols PS [urw]"])
        w_settings.setFont(font)
        self.gridLayout = QGridLayout(w_settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(w_settings)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setFamilies([u"Sans Serif"])
        self.groupBox.setFont(font1)
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.sl_pkt_loss_per = QSlider(self.groupBox)
        self.sl_pkt_loss_per.setObjectName(u"sl_pkt_loss_per")
        self.sl_pkt_loss_per.setOrientation(Qt.Horizontal)
        self.sl_pkt_loss_per.setTickPosition(QSlider.TicksBelow)

        self.gridLayout_2.addWidget(self.sl_pkt_loss_per, 2, 1, 1, 1)

        self.lbl_pkt_loss_per = QLabel(self.groupBox)
        self.lbl_pkt_loss_per.setObjectName(u"lbl_pkt_loss_per")

        self.gridLayout_2.addWidget(self.lbl_pkt_loss_per, 2, 2, 1, 1)

        self.lbl_prop_delay = QLabel(self.groupBox)
        self.lbl_prop_delay.setObjectName(u"lbl_prop_delay")

        self.gridLayout_2.addWidget(self.lbl_prop_delay, 0, 2, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.sl_prop_delay = QSlider(self.groupBox)
        self.sl_prop_delay.setObjectName(u"sl_prop_delay")
        self.sl_prop_delay.setAutoFillBackground(False)
        self.sl_prop_delay.setInputMethodHints(Qt.ImhNone)
        self.sl_prop_delay.setTracking(True)
        self.sl_prop_delay.setOrientation(Qt.Horizontal)
        self.sl_prop_delay.setTickPosition(QSlider.TicksBelow)

        self.gridLayout_2.addWidget(self.sl_prop_delay, 0, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.lbl_re_timer = QLabel(self.groupBox)
        self.lbl_re_timer.setObjectName(u"lbl_re_timer")

        self.gridLayout_2.addWidget(self.lbl_re_timer, 1, 2, 1, 1)

        self.sl_re_timer = QSlider(self.groupBox)
        self.sl_re_timer.setObjectName(u"sl_re_timer")
        self.sl_re_timer.setOrientation(Qt.Horizontal)
        self.sl_re_timer.setTickPosition(QSlider.TicksBelow)

        self.gridLayout_2.addWidget(self.sl_re_timer, 1, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(w_settings)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font1)
        self.groupBox_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.spin_R = QSpinBox(self.groupBox_2)
        self.spin_R.setObjectName(u"spin_R")
        self.spin_R.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.spin_R, 0, 3, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_8, 0, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.spin_K = QSpinBox(self.groupBox_2)
        self.spin_K.setObjectName(u"spin_K")
        self.spin_K.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.spin_K, 0, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)


        self.retranslateUi(w_settings)

        QMetaObject.connectSlotsByName(w_settings)
    # setupUi

    def retranslateUi(self, w_settings):
        w_settings.setWindowTitle(QCoreApplication.translate("w_settings", u"Settings", None))
        self.groupBox.setTitle(QCoreApplication.translate("w_settings", u"Settings", None))
        self.lbl_pkt_loss_per.setText(QCoreApplication.translate("w_settings", u"0%", None))
        self.lbl_prop_delay.setText(QCoreApplication.translate("w_settings", u"1.0s", None))
        self.label.setText(QCoreApplication.translate("w_settings", u"Propagation Delay", None))
        self.label_2.setText(QCoreApplication.translate("w_settings", u"Retransimission Timer", None))
        self.label_3.setText(QCoreApplication.translate("w_settings", u"Chance of Packet Loss", None))
        self.lbl_re_timer.setText(QCoreApplication.translate("w_settings", u"5.0s", None))
        self.groupBox_2.setTitle("")
        self.label_8.setText(QCoreApplication.translate("w_settings", u"Sender Window Size: R", None))
        self.label_7.setText(QCoreApplication.translate("w_settings", u"Number of Packets: K", None))
    # retranslateUi

