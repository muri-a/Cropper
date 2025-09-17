# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

from views.pages_view import PagesView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(990, 652)
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.spoiler_cb = QCheckBox(self.centralwidget)
        self.spoiler_cb.setObjectName(u"spoiler_cb")

        self.verticalLayout.addWidget(self.spoiler_cb)

        self.jpg_quality_layout = QHBoxLayout()
        self.jpg_quality_layout.setObjectName(u"jpg_quality_layout")
        self.jpg_quality_label = QLabel(self.centralwidget)
        self.jpg_quality_label.setObjectName(u"jpg_quality_label")

        self.jpg_quality_layout.addWidget(self.jpg_quality_label)

        self.jpg_quality_box = QSpinBox(self.centralwidget)
        self.jpg_quality_box.setObjectName(u"jpg_quality_box")
        self.jpg_quality_box.setMaximum(100)
        self.jpg_quality_box.setStepType(QAbstractSpinBox.StepType.DefaultStepType)
        self.jpg_quality_box.setValue(95)

        self.jpg_quality_layout.addWidget(self.jpg_quality_box)


        self.verticalLayout.addLayout(self.jpg_quality_layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pages_list_view = PagesView(self.centralwidget)
        self.pages_list_view.setObjectName(u"pages_list_view")

        self.verticalLayout_2.addWidget(self.pages_list_view)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.saving_label = QLabel(self.centralwidget)
        self.saving_label.setObjectName(u"saving_label")

        self.horizontalLayout.addWidget(self.saving_label)

        self.save_button = QPushButton(self.centralwidget)
        self.save_button.setObjectName(u"save_button")
        self.save_button.setEnabled(False)

        self.horizontalLayout.addWidget(self.save_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 990, 30))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_exit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cropper", None))
        self.action_open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.action_open.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.action_exit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.spoiler_cb.setText(QCoreApplication.translate("MainWindow", u"Spoiler mode", None))
        self.jpg_quality_label.setText(QCoreApplication.translate("MainWindow", u"Jpg quality", None))
        self.saving_label.setText(QCoreApplication.translate("MainWindow", u"saving...", None))
        self.save_button.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

