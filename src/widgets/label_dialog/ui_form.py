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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_LabelDialog(object):
    def setupUi(self, LabelDialog):
        if not LabelDialog.objectName():
            LabelDialog.setObjectName(u"LabelDialog")
        LabelDialog.resize(266, 266)
        self.verticalLayout = QVBoxLayout(LabelDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_Label_Name = QLineEdit(LabelDialog)
        self.lineEdit_Label_Name.setObjectName(u"lineEdit_Label_Name")
        self.lineEdit_Label_Name.setMinimumSize(QSize(170, 0))

        self.horizontalLayout.addWidget(self.lineEdit_Label_Name)

        self.lineEdit_Group_ID = QLineEdit(LabelDialog)
        self.lineEdit_Group_ID.setObjectName(u"lineEdit_Group_ID")
        self.lineEdit_Group_ID.setMinimumSize(QSize(70, 0))

        self.horizontalLayout.addWidget(self.lineEdit_Group_ID)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_Cancel = QPushButton(LabelDialog)
        self.pushButton_Cancel.setObjectName(u"pushButton_Cancel")

        self.horizontalLayout_2.addWidget(self.pushButton_Cancel)

        self.pushButton_OK = QPushButton(LabelDialog)
        self.pushButton_OK.setObjectName(u"pushButton_OK")

        self.horizontalLayout_2.addWidget(self.pushButton_OK)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listWidget_Label_Name = QListWidget(LabelDialog)
        self.listWidget_Label_Name.setObjectName(u"listWidget_Label_Name")

        self.verticalLayout.addWidget(self.listWidget_Label_Name)


        self.retranslateUi(LabelDialog)

        QMetaObject.connectSlotsByName(LabelDialog)
    # setupUi

    def retranslateUi(self, LabelDialog):
        LabelDialog.setWindowTitle(QCoreApplication.translate("LabelDialog", u"Label-Anything", None))
        self.lineEdit_Label_Name.setPlaceholderText(QCoreApplication.translate("LabelDialog", u"Enter Object Label", None))
        self.lineEdit_Group_ID.setPlaceholderText(QCoreApplication.translate("LabelDialog", u"Group ID", None))
        self.pushButton_Cancel.setText(QCoreApplication.translate("LabelDialog", u"&Cancel", None))
        self.pushButton_OK.setText(QCoreApplication.translate("LabelDialog", u"&OK", None))
    # retranslateUi

