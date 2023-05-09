# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_FileList(object):
    def setupUi(self, FileList):
        if not FileList.objectName():
            FileList.setObjectName(u"FileList")
        FileList.resize(300, 400)
        self.verticalLayout = QVBoxLayout(FileList)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_file_search = QLineEdit(FileList)
        self.lineEdit_file_search.setObjectName(u"lineEdit_file_search")
        self.lineEdit_file_search.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.lineEdit_file_search)

        self.label_current = QLabel(FileList)
        self.label_current.setObjectName(u"label_current")
        self.label_current.setMinimumSize(QSize(30, 0))
        self.label_current.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_current)

        self.label_separator = QLabel(FileList)
        self.label_separator.setObjectName(u"label_separator")
        self.label_separator.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_separator)

        self.label_total = QLabel(FileList)
        self.label_total.setObjectName(u"label_total")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_total.sizePolicy().hasHeightForWidth())
        self.label_total.setSizePolicy(sizePolicy)
        self.label_total.setMinimumSize(QSize(30, 0))
        self.label_total.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_total)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget_files = QListWidget(FileList)
        self.listWidget_files.setObjectName(u"listWidget_files")

        self.verticalLayout.addWidget(self.listWidget_files)


        self.retranslateUi(FileList)

        QMetaObject.connectSlotsByName(FileList)
    # setupUi

    def retranslateUi(self, FileList):
        FileList.setWindowTitle(QCoreApplication.translate("FileList", u"FileList", None))
        self.label_current.setText("")
        self.label_separator.setText(QCoreApplication.translate("FileList", u"/", None))
        self.label_total.setText("")
    # retranslateUi

