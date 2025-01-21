# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loading.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QProgressBar, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_LoadingWindow(object):
    def setupUi(self, LoadingWindow):
        if not LoadingWindow.objectName():
            LoadingWindow.setObjectName(u"LoadingWindow")
        LoadingWindow.resize(800, 300)
        LoadingWindow.setMinimumSize(QSize(800, 300))
        LoadingWindow.setMaximumSize(QSize(800, 300))
        LoadingWindow.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        LoadingWindow.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(120, 120, 255);\n"
"}\n"
"QProgressBar {\n"
"	border: 3px solid black;\n"
"}\n"
"QProgressBar::chunk {\n"
"	background-color: rgb(80, 80, 190);\n"
"}")
        self.centralwidget = QWidget(LoadingWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.loading_info = QLabel(self.centralwidget)
        self.loading_info.setObjectName(u"loading_info")
        self.loading_info.setMinimumSize(QSize(0, 100))
        self.loading_info.setMaximumSize(QSize(500, 100))
        font = QFont()
        font.setFamilies([u"Planewalker"])
        font.setPointSize(20)
        self.loading_info.setFont(font)
        self.loading_info.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.loading_info.setWordWrap(True)

        self.verticalLayout.addWidget(self.loading_info)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(500, 50))
        self.progressBar.setMaximumSize(QSize(500, 50))
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(True)
        self.progressBar.setFont(font1)
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.progressBar)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        LoadingWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(LoadingWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        LoadingWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(LoadingWindow)
        self.statusbar.setObjectName(u"statusbar")
        LoadingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoadingWindow)

        QMetaObject.connectSlotsByName(LoadingWindow)
    # setupUi

    def retranslateUi(self, LoadingWindow):
        LoadingWindow.setWindowTitle(QCoreApplication.translate("LoadingWindow", u"Loading...", None))
        self.loading_info.setText(QCoreApplication.translate("LoadingWindow", u"Loading card info sadaduahdiuahdiuahiusdhausdiudhau", None))
        self.label_2.setText(QCoreApplication.translate("LoadingWindow", u"All card data and images are collected from the Scryfall.com api", None))
    # retranslateUi

