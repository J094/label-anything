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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(500, 250)
        self.verticalLayout = QVBoxLayout(About)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_About = QLabel(About)
        self.label_About.setObjectName(u"label_About")
        font = QFont()
        font.setPointSize(11)
        self.label_About.setFont(font)

        self.verticalLayout.addWidget(self.label_About)

        self.label_Title = QLabel(About)
        self.label_Title.setObjectName(u"label_Title")
        self.label_Title.setMinimumSize(QSize(0, 150))
        font1 = QFont()
        font1.setPointSize(20)
        font1.setBold(False)
        font1.setItalic(True)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.label_Title.setFont(font1)
        self.label_Title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_Title)

        self.label_Author = QLabel(About)
        self.label_Author.setObjectName(u"label_Author")
        self.label_Author.setFont(font)
        self.label_Author.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_Author)

        self.label_E_Mail = QLabel(About)
        self.label_E_Mail.setObjectName(u"label_E_Mail")
        self.label_E_Mail.setFont(font)
        self.label_E_Mail.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_E_Mail)


        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(QCoreApplication.translate("About", u"About", None))
        self.label_About.setText(QCoreApplication.translate("About", u"About:", None))
        self.label_Title.setText(QCoreApplication.translate("About", u"Label-Anything", None))
        self.label_Author.setText(QCoreApplication.translate("About", u"Author: J094", None))
        self.label_E_Mail.setText(QCoreApplication.translate("About", u"E-Mail: jun.guo.chn@outlook.com", None))
    # retranslateUi

