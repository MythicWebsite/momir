# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'panel.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1837, 1159)
        MainWindow.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(120, 120, 255);\n"
"}\n"
"QPushButton {\n"
"	border: none;\n"
"	border-radius: 16px;\n"
"	color:  black;\n"
"	background-color: rgb(97, 97, 97);\n"
"	font-size: 20px;\n"
"	font-weight: bold;\n"
"	color: white;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.card_display = QLabel(self.centralwidget)
        self.card_display.setObjectName(u"card_display")
        self.card_display.setMinimumSize(QSize(500, 1000))
        self.card_display.setFrameShape(QFrame.Shape.NoFrame)
        self.card_display.setPixmap(QPixmap(u"Magic_card_back.png"))
        self.card_display.setScaledContents(False)
        self.card_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.card_display)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.button_big_down = QPushButton(self.centralwidget)
        self.button_big_down.setObjectName(u"button_big_down")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_big_down.sizePolicy().hasHeightForWidth())
        self.button_big_down.setSizePolicy(sizePolicy)
        self.button_big_down.setMinimumSize(QSize(0, 0))
        self.button_big_down.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout.addWidget(self.button_big_down)

        self.button_med_down = QPushButton(self.centralwidget)
        self.button_med_down.setObjectName(u"button_med_down")
        sizePolicy.setHeightForWidth(self.button_med_down.sizePolicy().hasHeightForWidth())
        self.button_med_down.setSizePolicy(sizePolicy)
        self.button_med_down.setMinimumSize(QSize(0, 0))
        self.button_med_down.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout.addWidget(self.button_med_down)

        self.button_small_down = QPushButton(self.centralwidget)
        self.button_small_down.setObjectName(u"button_small_down")
        sizePolicy.setHeightForWidth(self.button_small_down.sizePolicy().hasHeightForWidth())
        self.button_small_down.setSizePolicy(sizePolicy)
        self.button_small_down.setMinimumSize(QSize(0, 0))
        self.button_small_down.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout.addWidget(self.button_small_down)

        self.contrast_label = QLabel(self.centralwidget)
        self.contrast_label.setObjectName(u"contrast_label")
        self.contrast_label.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setPointSize(50)
        font.setBold(True)
        self.contrast_label.setFont(font)
        self.contrast_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.contrast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.contrast_label)

        self.button_small_up = QPushButton(self.centralwidget)
        self.button_small_up.setObjectName(u"button_small_up")
        sizePolicy.setHeightForWidth(self.button_small_up.sizePolicy().hasHeightForWidth())
        self.button_small_up.setSizePolicy(sizePolicy)
        self.button_small_up.setMinimumSize(QSize(0, 0))
        self.button_small_up.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout.addWidget(self.button_small_up)

        self.button_med_up = QPushButton(self.centralwidget)
        self.button_med_up.setObjectName(u"button_med_up")
        sizePolicy.setHeightForWidth(self.button_med_up.sizePolicy().hasHeightForWidth())
        self.button_med_up.setSizePolicy(sizePolicy)
        self.button_med_up.setMinimumSize(QSize(0, 0))
        self.button_med_up.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout.addWidget(self.button_med_up)

        self.button_big_up = QPushButton(self.centralwidget)
        self.button_big_up.setObjectName(u"button_big_up")
        sizePolicy.setHeightForWidth(self.button_big_up.sizePolicy().hasHeightForWidth())
        self.button_big_up.setSizePolicy(sizePolicy)
        self.button_big_up.setMinimumSize(QSize(0, 0))
        self.button_big_up.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout.addWidget(self.button_big_up)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.check_un = QCheckBox(self.centralwidget)
        self.check_un.setObjectName(u"check_un")
        font1 = QFont()
        font1.setPointSize(24)
        font1.setStrikeOut(True)
        self.check_un.setFont(font1)
        self.check_un.setAutoFillBackground(False)
        self.check_un.setIconSize(QSize(30, 30))
        self.check_un.setTristate(False)

        self.gridLayout_2.addWidget(self.check_un, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 0, 0, 1, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setAutoFillBackground(False)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(200)
        self.line.setMidLineWidth(200)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_2.addWidget(self.line, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 5, 0, 1, 1)

        self.check_noncreature = QCheckBox(self.centralwidget)
        self.check_noncreature.setObjectName(u"check_noncreature")
        self.check_noncreature.setFont(font1)
        self.check_noncreature.setIconSize(QSize(30, 30))

        self.gridLayout_2.addWidget(self.check_noncreature, 3, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 4, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.gridLayout.setContentsMargins(40, 0, 40, 40)
        self.button_14 = QPushButton(self.centralwidget)
        self.button_14.setObjectName(u"button_14")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_14.sizePolicy().hasHeightForWidth())
        self.button_14.setSizePolicy(sizePolicy1)
        self.button_14.setMinimumSize(QSize(100, 100))
        self.button_14.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_14, 7, 3, 1, 1)

        self.button_8 = QPushButton(self.centralwidget)
        self.button_8.setObjectName(u"button_8")
        sizePolicy1.setHeightForWidth(self.button_8.sizePolicy().hasHeightForWidth())
        self.button_8.setSizePolicy(sizePolicy1)
        self.button_8.setMinimumSize(QSize(100, 100))
        self.button_8.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_8, 4, 3, 1, 1)

        self.button_7 = QPushButton(self.centralwidget)
        self.button_7.setObjectName(u"button_7")
        sizePolicy1.setHeightForWidth(self.button_7.sizePolicy().hasHeightForWidth())
        self.button_7.setSizePolicy(sizePolicy1)
        self.button_7.setMinimumSize(QSize(100, 100))
        self.button_7.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_7, 4, 2, 1, 1)

        self.button_6 = QPushButton(self.centralwidget)
        self.button_6.setObjectName(u"button_6")
        sizePolicy1.setHeightForWidth(self.button_6.sizePolicy().hasHeightForWidth())
        self.button_6.setSizePolicy(sizePolicy1)
        self.button_6.setMinimumSize(QSize(100, 100))
        self.button_6.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_6, 4, 1, 1, 1)

        self.button_11 = QPushButton(self.centralwidget)
        self.button_11.setObjectName(u"button_11")
        sizePolicy1.setHeightForWidth(self.button_11.sizePolicy().hasHeightForWidth())
        self.button_11.setSizePolicy(sizePolicy1)
        self.button_11.setMinimumSize(QSize(100, 100))
        self.button_11.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_11, 5, 3, 1, 1)

        self.button_3 = QPushButton(self.centralwidget)
        self.button_3.setObjectName(u"button_3")
        sizePolicy1.setHeightForWidth(self.button_3.sizePolicy().hasHeightForWidth())
        self.button_3.setSizePolicy(sizePolicy1)
        self.button_3.setMinimumSize(QSize(100, 100))
        self.button_3.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_3, 3, 1, 1, 1)

        self.button_2 = QPushButton(self.centralwidget)
        self.button_2.setObjectName(u"button_2")
        sizePolicy1.setHeightForWidth(self.button_2.sizePolicy().hasHeightForWidth())
        self.button_2.setSizePolicy(sizePolicy1)
        self.button_2.setMinimumSize(QSize(100, 100))
        self.button_2.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_2, 1, 3, 1, 1)

        self.button_5 = QPushButton(self.centralwidget)
        self.button_5.setObjectName(u"button_5")
        sizePolicy1.setHeightForWidth(self.button_5.sizePolicy().hasHeightForWidth())
        self.button_5.setSizePolicy(sizePolicy1)
        self.button_5.setMinimumSize(QSize(100, 100))
        self.button_5.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_5, 3, 3, 1, 1)

        self.button_12 = QPushButton(self.centralwidget)
        self.button_12.setObjectName(u"button_12")
        sizePolicy1.setHeightForWidth(self.button_12.sizePolicy().hasHeightForWidth())
        self.button_12.setSizePolicy(sizePolicy1)
        self.button_12.setMinimumSize(QSize(100, 100))
        self.button_12.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_12, 7, 1, 1, 1)

        self.button_1 = QPushButton(self.centralwidget)
        self.button_1.setObjectName(u"button_1")
        sizePolicy1.setHeightForWidth(self.button_1.sizePolicy().hasHeightForWidth())
        self.button_1.setSizePolicy(sizePolicy1)
        self.button_1.setMinimumSize(QSize(100, 100))
        self.button_1.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_1, 1, 2, 1, 1)

        self.button_print = QPushButton(self.centralwidget)
        self.button_print.setObjectName(u"button_print")
        self.button_print.setMinimumSize(QSize(500, 100))

        self.gridLayout.addWidget(self.button_print, 10, 1, 1, 3)

        self.button_15 = QPushButton(self.centralwidget)
        self.button_15.setObjectName(u"button_15")
        sizePolicy1.setHeightForWidth(self.button_15.sizePolicy().hasHeightForWidth())
        self.button_15.setSizePolicy(sizePolicy1)
        self.button_15.setMinimumSize(QSize(100, 100))
        self.button_15.setMaximumSize(QSize(5000, 5000))
        self.button_15.setStyleSheet(u"")

        self.gridLayout.addWidget(self.button_15, 8, 1, 1, 1)

        self.button_0 = QPushButton(self.centralwidget)
        self.button_0.setObjectName(u"button_0")
        sizePolicy1.setHeightForWidth(self.button_0.sizePolicy().hasHeightForWidth())
        self.button_0.setSizePolicy(sizePolicy1)
        self.button_0.setMinimumSize(QSize(100, 100))
        self.button_0.setMaximumSize(QSize(5000, 5000))
        self.button_0.setAutoFillBackground(False)

        self.gridLayout.addWidget(self.button_0, 1, 1, 1, 1)

        self.button_4 = QPushButton(self.centralwidget)
        self.button_4.setObjectName(u"button_4")
        sizePolicy1.setHeightForWidth(self.button_4.sizePolicy().hasHeightForWidth())
        self.button_4.setSizePolicy(sizePolicy1)
        self.button_4.setMinimumSize(QSize(100, 100))
        self.button_4.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_4, 3, 2, 1, 1)

        self.cmc_label = QLabel(self.centralwidget)
        self.cmc_label.setObjectName(u"cmc_label")
        font2 = QFont()
        font2.setPointSize(40)
        font2.setBold(True)
        self.cmc_label.setFont(font2)
        self.cmc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.cmc_label, 0, 1, 1, 3)

        self.button_16 = QPushButton(self.centralwidget)
        self.button_16.setObjectName(u"button_16")
        sizePolicy1.setHeightForWidth(self.button_16.sizePolicy().hasHeightForWidth())
        self.button_16.setSizePolicy(sizePolicy1)
        self.button_16.setMinimumSize(QSize(100, 100))
        self.button_16.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_16, 8, 2, 1, 1)

        self.button_9 = QPushButton(self.centralwidget)
        self.button_9.setObjectName(u"button_9")
        sizePolicy1.setHeightForWidth(self.button_9.sizePolicy().hasHeightForWidth())
        self.button_9.setSizePolicy(sizePolicy1)
        self.button_9.setMinimumSize(QSize(100, 100))
        self.button_9.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_9, 5, 1, 1, 1)

        self.button_10 = QPushButton(self.centralwidget)
        self.button_10.setObjectName(u"button_10")
        sizePolicy1.setHeightForWidth(self.button_10.sizePolicy().hasHeightForWidth())
        self.button_10.setSizePolicy(sizePolicy1)
        self.button_10.setMinimumSize(QSize(100, 100))
        self.button_10.setMaximumSize(QSize(5000, 5000))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setBold(True)
        font3.setItalic(False)
        font3.setStrikeOut(False)
        self.button_10.setFont(font3)

        self.gridLayout.addWidget(self.button_10, 5, 2, 1, 1)

        self.button_13 = QPushButton(self.centralwidget)
        self.button_13.setObjectName(u"button_13")
        sizePolicy1.setHeightForWidth(self.button_13.sizePolicy().hasHeightForWidth())
        self.button_13.setSizePolicy(sizePolicy1)
        self.button_13.setMinimumSize(QSize(100, 100))
        self.button_13.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_13, 7, 2, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 9, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1837, 22))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.card_display.setText("")
        self.button_big_down.setText(QCoreApplication.translate("MainWindow", u"-1", None))
        self.button_med_down.setText(QCoreApplication.translate("MainWindow", u"- 0.5", None))
        self.button_small_down.setText(QCoreApplication.translate("MainWindow", u"- 0.1", None))
        self.contrast_label.setText(QCoreApplication.translate("MainWindow", u"2.0", None))
        self.button_small_up.setText(QCoreApplication.translate("MainWindow", u"+ 0.1", None))
        self.button_med_up.setText(QCoreApplication.translate("MainWindow", u"+ 0.5", None))
        self.button_big_up.setText(QCoreApplication.translate("MainWindow", u"+1", None))
        self.check_un.setText(QCoreApplication.translate("MainWindow", u"  Enable Un-Cards", None))
        self.check_noncreature.setText(QCoreApplication.translate("MainWindow", u"  Enable non-creature \n"
"  cards", None))
        self.button_14.setText(QCoreApplication.translate("MainWindow", u"14", None))
        self.button_8.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.button_7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.button_6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.button_11.setText(QCoreApplication.translate("MainWindow", u"11", None))
        self.button_3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.button_2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.button_5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.button_12.setText(QCoreApplication.translate("MainWindow", u"12", None))
        self.button_1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.button_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.button_15.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.button_0.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.button_4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.cmc_label.setText(QCoreApplication.translate("MainWindow", u"CMC: 0", None))
        self.button_16.setText(QCoreApplication.translate("MainWindow", u"16", None))
        self.button_9.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.button_10.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.button_13.setText(QCoreApplication.translate("MainWindow", u"13", None))
        self.label_3.setText("")
    # retranslateUi

