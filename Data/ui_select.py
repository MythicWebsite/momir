# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'select.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QSizePolicy, QStatusBar,
    QWidget)

class Ui_SelectWindow(object):
    def setupUi(self, SelectWindow):
        if not SelectWindow.objectName():
            SelectWindow.setObjectName(u"SelectWindow")
        SelectWindow.resize(1200, 700)
        SelectWindow.setMinimumSize(QSize(1200, 700))
        SelectWindow.setMaximumSize(QSize(1200, 700))
        SelectWindow.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(120, 120, 255);\n"
"}")
        self.centralwidget = QWidget(SelectWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.card_grid = QGridLayout()
        self.card_grid.setObjectName(u"card_grid")
        self.card_grid.setContentsMargins(6, 6, 6, 6)
        self.card_1 = QLabel(self.centralwidget)
        self.card_1.setObjectName(u"card_1")
        self.card_1.setMinimumSize(QSize(390, 0))
        self.card_1.setMaximumSize(QSize(390, 16777215))
        self.card_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_grid.addWidget(self.card_1, 0, 0, 1, 1)

        self.card_2 = QLabel(self.centralwidget)
        self.card_2.setObjectName(u"card_2")
        self.card_2.setMinimumSize(QSize(390, 0))
        self.card_2.setMaximumSize(QSize(390, 16777215))
        self.card_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_grid.addWidget(self.card_2, 0, 1, 1, 1)

        self.card_3 = QLabel(self.centralwidget)
        self.card_3.setObjectName(u"card_3")
        self.card_3.setMinimumSize(QSize(390, 0))
        self.card_3.setMaximumSize(QSize(390, 16777215))
        self.card_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_grid.addWidget(self.card_3, 0, 2, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 50))
        self.label.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_grid.addWidget(self.label, 1, 0, 1, 3)


        self.horizontalLayout.addLayout(self.card_grid)

        SelectWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SelectWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        SelectWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SelectWindow)
        self.statusbar.setObjectName(u"statusbar")
        SelectWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SelectWindow)

        QMetaObject.connectSlotsByName(SelectWindow)
    # setupUi

    def retranslateUi(self, SelectWindow):
        SelectWindow.setWindowTitle(QCoreApplication.translate("SelectWindow", u"Select a card", None))
        self.card_1.setText("")
        self.card_2.setText("")
        self.card_3.setText("")
        self.label.setText(QCoreApplication.translate("SelectWindow", u"Select 1 of the 3 cards", None))
    # retranslateUi

