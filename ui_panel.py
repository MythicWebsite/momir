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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QListView, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1964, 1224)
        MainWindow.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(120, 120, 255);\n"
"}\n"
"QPushButton {\n"
"	border: none;\n"
"	border-radius: 16px;\n"
"	color:  black;\n"
"	background-color: rgb(97, 97, 97);\n"
"	font-size: 40px;\n"
"	font-weight: bold;\n"
"	color: white;\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color:rgb(50,50,50);\n"
"}\n"
"QTabWidget::pane{\n"
"	background: rgb(28, 20, 255);\n"
"	border: 0px solid rgb(90, 90, 90);\n"
"	top:-1px;\n"
"}\n"
"QTabWidget::tab-bar{\n"
"	alignment:center;\n"
"}\n"
"QTabBar::tab {\n"
"	background: rgb(80, 80, 190);\n"
"	border: 3px solid black;\n"
"	padding: 5px;\n"
"}\n"
"QTabBar::tab:selected {\n"
"	background: rgb(120, 120, 255);\n"
"	margin-bottom: -3px;\n"
"}\n"
"QScrollBar:vertical {\n"
"	width:100px;\n"
"}\n"
"QListWidget {\n"
"	alternate-background-color: rgb(100, 100, 190);\n"
"	padding: 10px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setPointSize(60)
        self.tabWidget.setFont(font)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setElideMode(Qt.TextElideMode.ElideLeft)
        self.momir_tab = QWidget()
        self.momir_tab.setObjectName(u"momir_tab")
        self.gridLayout_3 = QGridLayout(self.momir_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.gridLayout.setContentsMargins(40, 0, 40, 40)
        self.button_14 = QPushButton(self.momir_tab)
        self.button_14.setObjectName(u"button_14")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_14.sizePolicy().hasHeightForWidth())
        self.button_14.setSizePolicy(sizePolicy)
        self.button_14.setMinimumSize(QSize(100, 100))
        self.button_14.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_14, 7, 3, 1, 1)

        self.button_8 = QPushButton(self.momir_tab)
        self.button_8.setObjectName(u"button_8")
        sizePolicy.setHeightForWidth(self.button_8.sizePolicy().hasHeightForWidth())
        self.button_8.setSizePolicy(sizePolicy)
        self.button_8.setMinimumSize(QSize(100, 100))
        self.button_8.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_8, 4, 3, 1, 1)

        self.button_7 = QPushButton(self.momir_tab)
        self.button_7.setObjectName(u"button_7")
        sizePolicy.setHeightForWidth(self.button_7.sizePolicy().hasHeightForWidth())
        self.button_7.setSizePolicy(sizePolicy)
        self.button_7.setMinimumSize(QSize(100, 100))
        self.button_7.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_7, 4, 2, 1, 1)

        self.button_6 = QPushButton(self.momir_tab)
        self.button_6.setObjectName(u"button_6")
        sizePolicy.setHeightForWidth(self.button_6.sizePolicy().hasHeightForWidth())
        self.button_6.setSizePolicy(sizePolicy)
        self.button_6.setMinimumSize(QSize(100, 100))
        self.button_6.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_6, 4, 1, 1, 1)

        self.button_11 = QPushButton(self.momir_tab)
        self.button_11.setObjectName(u"button_11")
        sizePolicy.setHeightForWidth(self.button_11.sizePolicy().hasHeightForWidth())
        self.button_11.setSizePolicy(sizePolicy)
        self.button_11.setMinimumSize(QSize(100, 100))
        self.button_11.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_11, 5, 3, 1, 1)

        self.button_3 = QPushButton(self.momir_tab)
        self.button_3.setObjectName(u"button_3")
        sizePolicy.setHeightForWidth(self.button_3.sizePolicy().hasHeightForWidth())
        self.button_3.setSizePolicy(sizePolicy)
        self.button_3.setMinimumSize(QSize(100, 100))
        self.button_3.setMaximumSize(QSize(5000, 5000))
        self.button_3.setFlat(False)

        self.gridLayout.addWidget(self.button_3, 3, 1, 1, 1)

        self.button_2 = QPushButton(self.momir_tab)
        self.button_2.setObjectName(u"button_2")
        sizePolicy.setHeightForWidth(self.button_2.sizePolicy().hasHeightForWidth())
        self.button_2.setSizePolicy(sizePolicy)
        self.button_2.setMinimumSize(QSize(100, 100))
        self.button_2.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_2, 1, 3, 1, 1)

        self.button_5 = QPushButton(self.momir_tab)
        self.button_5.setObjectName(u"button_5")
        sizePolicy.setHeightForWidth(self.button_5.sizePolicy().hasHeightForWidth())
        self.button_5.setSizePolicy(sizePolicy)
        self.button_5.setMinimumSize(QSize(100, 100))
        self.button_5.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_5, 3, 3, 1, 1)

        self.button_12 = QPushButton(self.momir_tab)
        self.button_12.setObjectName(u"button_12")
        sizePolicy.setHeightForWidth(self.button_12.sizePolicy().hasHeightForWidth())
        self.button_12.setSizePolicy(sizePolicy)
        self.button_12.setMinimumSize(QSize(100, 100))
        self.button_12.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_12, 7, 1, 1, 1)

        self.button_1 = QPushButton(self.momir_tab)
        self.button_1.setObjectName(u"button_1")
        sizePolicy.setHeightForWidth(self.button_1.sizePolicy().hasHeightForWidth())
        self.button_1.setSizePolicy(sizePolicy)
        self.button_1.setMinimumSize(QSize(100, 100))
        self.button_1.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_1, 1, 2, 1, 1)

        self.button_print_card = QPushButton(self.momir_tab)
        self.button_print_card.setObjectName(u"button_print_card")
        self.button_print_card.setMinimumSize(QSize(500, 100))

        self.gridLayout.addWidget(self.button_print_card, 10, 1, 1, 3)

        self.button_15 = QPushButton(self.momir_tab)
        self.button_15.setObjectName(u"button_15")
        sizePolicy.setHeightForWidth(self.button_15.sizePolicy().hasHeightForWidth())
        self.button_15.setSizePolicy(sizePolicy)
        self.button_15.setMinimumSize(QSize(100, 100))
        self.button_15.setMaximumSize(QSize(5000, 5000))
        self.button_15.setStyleSheet(u"")

        self.gridLayout.addWidget(self.button_15, 8, 1, 1, 1)

        self.button_0 = QPushButton(self.momir_tab)
        self.button_0.setObjectName(u"button_0")
        sizePolicy.setHeightForWidth(self.button_0.sizePolicy().hasHeightForWidth())
        self.button_0.setSizePolicy(sizePolicy)
        self.button_0.setMinimumSize(QSize(100, 100))
        self.button_0.setMaximumSize(QSize(5000, 5000))
        self.button_0.setAutoFillBackground(False)

        self.gridLayout.addWidget(self.button_0, 1, 1, 1, 1)

        self.button_4 = QPushButton(self.momir_tab)
        self.button_4.setObjectName(u"button_4")
        sizePolicy.setHeightForWidth(self.button_4.sizePolicy().hasHeightForWidth())
        self.button_4.setSizePolicy(sizePolicy)
        self.button_4.setMinimumSize(QSize(100, 100))
        self.button_4.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_4, 3, 2, 1, 1)

        self.cmc_label = QLabel(self.momir_tab)
        self.cmc_label.setObjectName(u"cmc_label")
        font1 = QFont()
        font1.setPointSize(60)
        font1.setBold(True)
        self.cmc_label.setFont(font1)
        self.cmc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.cmc_label, 0, 1, 1, 3)

        self.button_16 = QPushButton(self.momir_tab)
        self.button_16.setObjectName(u"button_16")
        sizePolicy.setHeightForWidth(self.button_16.sizePolicy().hasHeightForWidth())
        self.button_16.setSizePolicy(sizePolicy)
        self.button_16.setMinimumSize(QSize(100, 100))
        self.button_16.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_16, 8, 2, 1, 1)

        self.button_9 = QPushButton(self.momir_tab)
        self.button_9.setObjectName(u"button_9")
        sizePolicy.setHeightForWidth(self.button_9.sizePolicy().hasHeightForWidth())
        self.button_9.setSizePolicy(sizePolicy)
        self.button_9.setMinimumSize(QSize(100, 100))
        self.button_9.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_9, 5, 1, 1, 1)

        self.button_10 = QPushButton(self.momir_tab)
        self.button_10.setObjectName(u"button_10")
        sizePolicy.setHeightForWidth(self.button_10.sizePolicy().hasHeightForWidth())
        self.button_10.setSizePolicy(sizePolicy)
        self.button_10.setMinimumSize(QSize(100, 100))
        self.button_10.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_10, 5, 2, 1, 1)

        self.button_13 = QPushButton(self.momir_tab)
        self.button_13.setObjectName(u"button_13")
        sizePolicy.setHeightForWidth(self.button_13.sizePolicy().hasHeightForWidth())
        self.button_13.setSizePolicy(sizePolicy)
        self.button_13.setMinimumSize(QSize(100, 100))
        self.button_13.setMaximumSize(QSize(5000, 5000))

        self.gridLayout.addWidget(self.button_13, 7, 2, 1, 1)

        self.label_3 = QLabel(self.momir_tab)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 9, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 5, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 0, 4, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.card_display = QLabel(self.momir_tab)
        self.card_display.setObjectName(u"card_display")
        self.card_display.setMinimumSize(QSize(800, 1000))
        self.card_display.setFrameShape(QFrame.Shape.NoFrame)
        self.card_display.setPixmap(QPixmap(u"Magic_card_back.png"))
        self.card_display.setScaledContents(False)
        self.card_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_display.setMargin(0)

        self.horizontalLayout.addWidget(self.card_display)


        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_4, 5, 0, 1, 1)

        self.check_un = QCheckBox(self.momir_tab)
        self.check_un.setObjectName(u"check_un")
        font2 = QFont()
        font2.setPointSize(35)
        font2.setStrikeOut(False)
        self.check_un.setFont(font2)
        self.check_un.setAutoFillBackground(False)
        self.check_un.setIconSize(QSize(30, 30))
        self.check_un.setTristate(False)

        self.gridLayout_2.addWidget(self.check_un, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 7, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 1, 0, 1, 1)

        self.check_noncreature = QCheckBox(self.momir_tab)
        self.check_noncreature.setObjectName(u"check_noncreature")
        font3 = QFont()
        font3.setPointSize(35)
        font3.setStrikeOut(True)
        self.check_noncreature.setFont(font3)
        self.check_noncreature.setIconSize(QSize(30, 30))

        self.gridLayout_2.addWidget(self.check_noncreature, 4, 0, 1, 1)

        self.line = QFrame(self.momir_tab)
        self.line.setObjectName(u"line")
        self.line.setAutoFillBackground(False)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(200)
        self.line.setMidLineWidth(200)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_2.addWidget(self.line, 3, 0, 1, 1)

        self.action_list = QListWidget(self.momir_tab)
        self.action_list.setObjectName(u"action_list")
        self.action_list.setMinimumSize(QSize(500, 800))
        font4 = QFont()
        font4.setPointSize(25)
        font4.setBold(True)
        self.action_list.setFont(font4)
        self.action_list.setFrameShape(QFrame.Shape.Box)
        self.action_list.setFrameShadow(QFrame.Shadow.Plain)
        self.action_list.setLineWidth(3)
        self.action_list.setMidLineWidth(3)
        self.action_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.action_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.action_list.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)
        self.action_list.setDefaultDropAction(Qt.DropAction.IgnoreAction)
        self.action_list.setAlternatingRowColors(True)
        self.action_list.setTextElideMode(Qt.TextElideMode.ElideLeft)
        self.action_list.setMovement(QListView.Movement.Free)
        self.action_list.setResizeMode(QListView.ResizeMode.Fixed)
        self.action_list.setSpacing(5)
        self.action_list.setBatchSize(10)
        self.action_list.setWordWrap(True)
        self.action_list.setItemAlignment(Qt.AlignmentFlag.AlignCenter)
        self.action_list.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.action_list, 6, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 0, 6, 1, 1)

        self.tabWidget.addTab(self.momir_tab, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_8 = QHBoxLayout(self.tab)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.button_print_history = QPushButton(self.tab)
        self.button_print_history.setObjectName(u"button_print_history")
        self.button_print_history.setMinimumSize(QSize(500, 100))
        self.button_print_history.setMaximumSize(QSize(600, 16777215))

        self.gridLayout_6.addWidget(self.button_print_history, 1, 0, 1, 1)

        self.history_display = QLabel(self.tab)
        self.history_display.setObjectName(u"history_display")
        self.history_display.setMinimumSize(QSize(500, 0))
        self.history_display.setMaximumSize(QSize(600, 16777215))

        self.gridLayout_6.addWidget(self.history_display, 0, 0, 1, 1)


        self.horizontalLayout_8.addLayout(self.gridLayout_6)

        self.scrollArea_3 = QScrollArea(self.tab)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_3.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea_3.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 1320, 1045))
        self.horizontalLayout_7 = QHBoxLayout(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.history_grid = QGridLayout()
        self.history_grid.setObjectName(u"history_grid")
        self.label_12 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_12.setObjectName(u"label_12")

        self.history_grid.addWidget(self.label_12, 0, 4, 1, 1)

        self.label_13 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_13.setObjectName(u"label_13")

        self.history_grid.addWidget(self.label_13, 0, 0, 1, 1)

        self.label_14 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_14.setObjectName(u"label_14")

        self.history_grid.addWidget(self.label_14, 1, 6, 1, 1)

        self.label_15 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_15.setObjectName(u"label_15")

        self.history_grid.addWidget(self.label_15, 0, 6, 1, 1)

        self.label_16 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_16.setObjectName(u"label_16")

        self.history_grid.addWidget(self.label_16, 0, 1, 1, 1)

        self.label_17 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_17.setObjectName(u"label_17")

        self.history_grid.addWidget(self.label_17, 2, 6, 1, 1)

        self.label_18 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_18.setObjectName(u"label_18")

        self.history_grid.addWidget(self.label_18, 0, 2, 1, 1)

        self.label_19 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_19.setObjectName(u"label_19")

        self.history_grid.addWidget(self.label_19, 0, 3, 1, 1)

        self.label_20 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_20.setObjectName(u"label_20")

        self.history_grid.addWidget(self.label_20, 0, 5, 1, 1)

        self.label_21 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_21.setObjectName(u"label_21")

        self.history_grid.addWidget(self.label_21, 3, 6, 1, 1)


        self.horizontalLayout_7.addLayout(self.history_grid)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.horizontalLayout_8.addWidget(self.scrollArea_3)

        self.tabWidget.addTab(self.tab, "")
        self.tokens_tab = QWidget()
        self.tokens_tab.setObjectName(u"tokens_tab")
        self.horizontalLayout_6 = QHBoxLayout(self.tokens_tab)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.button_print_token = QPushButton(self.tokens_tab)
        self.button_print_token.setObjectName(u"button_print_token")
        self.button_print_token.setMinimumSize(QSize(500, 100))
        self.button_print_token.setMaximumSize(QSize(600, 16777215))

        self.gridLayout_5.addWidget(self.button_print_token, 1, 0, 1, 1)

        self.token_display = QLabel(self.tokens_tab)
        self.token_display.setObjectName(u"token_display")
        self.token_display.setMinimumSize(QSize(500, 0))
        self.token_display.setMaximumSize(QSize(600, 16777215))

        self.gridLayout_5.addWidget(self.token_display, 0, 0, 1, 1)


        self.horizontalLayout_6.addLayout(self.gridLayout_5)

        self.scrollArea_2 = QScrollArea(self.tokens_tab)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea_2.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1320, 1045))
        self.horizontalLayout_5 = QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.token_grid = QGridLayout()
        self.token_grid.setObjectName(u"token_grid")
        self.label_4 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_4.setObjectName(u"label_4")

        self.token_grid.addWidget(self.label_4, 0, 4, 1, 1)

        self.label_8 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_8.setObjectName(u"label_8")

        self.token_grid.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_9 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_9.setObjectName(u"label_9")

        self.token_grid.addWidget(self.label_9, 1, 6, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents_2)
        self.label.setObjectName(u"label")

        self.token_grid.addWidget(self.label, 0, 6, 1, 1)

        self.label_7 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_7.setObjectName(u"label_7")

        self.token_grid.addWidget(self.label_7, 0, 1, 1, 1)

        self.label_10 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_10.setObjectName(u"label_10")

        self.token_grid.addWidget(self.label_10, 2, 6, 1, 1)

        self.label_6 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_6.setObjectName(u"label_6")

        self.token_grid.addWidget(self.label_6, 0, 2, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_5.setObjectName(u"label_5")

        self.token_grid.addWidget(self.label_5, 0, 3, 1, 1)

        self.label_2 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_2.setObjectName(u"label_2")

        self.token_grid.addWidget(self.label_2, 0, 5, 1, 1)

        self.label_11 = QLabel(self.scrollAreaWidgetContents_2)
        self.label_11.setObjectName(u"label_11")

        self.token_grid.addWidget(self.label_11, 3, 6, 1, 1)


        self.horizontalLayout_5.addLayout(self.token_grid)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout_6.addWidget(self.scrollArea_2)

        self.tabWidget.addTab(self.tokens_tab, "")
        self.tokens_tab_2 = QWidget()
        self.tokens_tab_2.setObjectName(u"tokens_tab_2")
        self.horizontalLayout_3 = QHBoxLayout(self.tokens_tab_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.button_print_token_2 = QPushButton(self.tokens_tab_2)
        self.button_print_token_2.setObjectName(u"button_print_token_2")
        self.button_print_token_2.setMinimumSize(QSize(500, 100))
        self.button_print_token_2.setMaximumSize(QSize(600, 16777215))

        self.gridLayout_4.addWidget(self.button_print_token_2, 1, 0, 1, 1)

        self.token_display_2 = QLabel(self.tokens_tab_2)
        self.token_display_2.setObjectName(u"token_display_2")
        self.token_display_2.setMinimumSize(QSize(500, 0))
        self.token_display_2.setMaximumSize(QSize(600, 16777215))

        self.gridLayout_4.addWidget(self.token_display_2, 0, 0, 1, 1)


        self.horizontalLayout_3.addLayout(self.gridLayout_4)

        self.scrollArea = QScrollArea(self.tokens_tab_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1320, 1045))
        self.horizontalLayout_4 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.token_grid_2 = QGridLayout()
        self.token_grid_2.setObjectName(u"token_grid_2")

        self.horizontalLayout_4.addLayout(self.token_grid_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_3.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tokens_tab_2, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1964, 22))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
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
        self.button_print_card.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.button_15.setText(QCoreApplication.translate("MainWindow", u"15", None))
        self.button_0.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.button_4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.cmc_label.setText(QCoreApplication.translate("MainWindow", u"CMC: 0", None))
        self.button_16.setText(QCoreApplication.translate("MainWindow", u"16", None))
        self.button_9.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.button_10.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.button_13.setText(QCoreApplication.translate("MainWindow", u"13", None))
        self.label_3.setText("")
        self.card_display.setText("")
        self.check_un.setText(QCoreApplication.translate("MainWindow", u"  Enable Un-Cards", None))
        self.check_noncreature.setText(QCoreApplication.translate("MainWindow", u"  Enable non-creature \n"
"  cards", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.momir_tab), QCoreApplication.translate("MainWindow", u"  Momir  ", None))
        self.button_print_history.setText(QCoreApplication.translate("MainWindow", u" Print", None))
        self.history_display.setText("")
        self.label_12.setText("")
        self.label_13.setText("")
        self.label_14.setText("")
        self.label_15.setText("")
        self.label_16.setText("")
        self.label_17.setText("")
        self.label_18.setText("")
        self.label_19.setText("")
        self.label_20.setText("")
        self.label_21.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"  History  ", None))
        self.button_print_token.setText(QCoreApplication.translate("MainWindow", u" Print", None))
        self.token_display.setText("")
        self.label_4.setText("")
        self.label_8.setText("")
        self.label_9.setText("")
        self.label.setText("")
        self.label_7.setText("")
        self.label_10.setText("")
        self.label_6.setText("")
        self.label_5.setText("")
        self.label_2.setText("")
        self.label_11.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tokens_tab), QCoreApplication.translate("MainWindow", u"  Tokens  ", None))
        self.button_print_token_2.setText(QCoreApplication.translate("MainWindow", u" Print", None))
        self.token_display_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tokens_tab_2), QCoreApplication.translate("MainWindow", u"  All Tokens  ", None))
    # retranslateUi

