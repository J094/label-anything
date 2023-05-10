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
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 5)
        self.lineEdit_File_Search = QLineEdit(FileList)
        self.lineEdit_File_Search.setObjectName(u"lineEdit_File_Search")
        self.lineEdit_File_Search.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.lineEdit_File_Search)

        self.label_Current = QLabel(FileList)
        self.label_Current.setObjectName(u"label_Current")
        self.label_Current.setMinimumSize(QSize(30, 0))
        self.label_Current.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_Current)

        self.label_Separator = QLabel(FileList)
        self.label_Separator.setObjectName(u"label_Separator")
        self.label_Separator.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_Separator)

        self.label_Total = QLabel(FileList)
        self.label_Total.setObjectName(u"label_Total")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Total.sizePolicy().hasHeightForWidth())
        self.label_Total.setSizePolicy(sizePolicy)
        self.label_Total.setMinimumSize(QSize(30, 0))
        self.label_Total.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_Total)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget_Files = QListWidget(FileList)
        self.listWidget_Files.setObjectName(u"listWidget_Files")

        self.verticalLayout.addWidget(self.listWidget_Files)


        self.retranslateUi(FileList)

        QMetaObject.connectSlotsByName(FileList)
    # setupUi

    def retranslateUi(self, FileList):
        FileList.setWindowTitle(QCoreApplication.translate("FileList", u"FileList", None))
        self.lineEdit_File_Search.setPlaceholderText(QCoreApplication.translate("FileList", u"Search Filename", None))
        self.label_Current.setText("")
        self.label_Separator.setText(QCoreApplication.translate("FileList", u"/", None))
        self.label_Total.setText("")
    # retranslateUi

