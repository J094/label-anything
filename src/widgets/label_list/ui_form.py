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
from PySide6.QtWidgets import (QApplication, QListWidget, QListWidgetItem, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_LabelList(object):
    def setupUi(self, LabelList):
        if not LabelList.objectName():
            LabelList.setObjectName(u"LabelList")
        LabelList.resize(300, 400)
        self.verticalLayout = QVBoxLayout(LabelList)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget_Labels = QListWidget(LabelList)
        self.listWidget_Labels.setObjectName(u"listWidget_Labels")

        self.verticalLayout.addWidget(self.listWidget_Labels)


        self.retranslateUi(LabelList)

        QMetaObject.connectSlotsByName(LabelList)
    # setupUi

    def retranslateUi(self, LabelList):
        LabelList.setWindowTitle(QCoreApplication.translate("LabelList", u"LabelList", None))
    # retranslateUi

