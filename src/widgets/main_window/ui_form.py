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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QToolBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        self.action_Open_Dir = QAction(MainWindow)
        self.action_Open_Dir.setObjectName(u"action_Open_Dir")
        self.action_Setup_Assist = QAction(MainWindow)
        self.action_Setup_Assist.setObjectName(u"action_Setup_Assist")
        self.action_Next_Image = QAction(MainWindow)
        self.action_Next_Image.setObjectName(u"action_Next_Image")
        self.action_Next_Image.setEnabled(False)
        self.action_Prev_Image = QAction(MainWindow)
        self.action_Prev_Image.setObjectName(u"action_Prev_Image")
        self.action_Prev_Image.setEnabled(False)
        self.action_Save = QAction(MainWindow)
        self.action_Save.setObjectName(u"action_Save")
        self.action_Save.setEnabled(False)
        self.action_Save_As = QAction(MainWindow)
        self.action_Save_As.setObjectName(u"action_Save_As")
        self.action_Save_As.setEnabled(False)
        self.action_Auto_Save = QAction(MainWindow)
        self.action_Auto_Save.setObjectName(u"action_Auto_Save")
        self.action_Auto_Save.setCheckable(True)
        self.action_Auto_Save.setEnabled(False)
        self.action_Change_Output_Dir = QAction(MainWindow)
        self.action_Change_Output_Dir.setObjectName(u"action_Change_Output_Dir")
        self.action_Save_With_Image = QAction(MainWindow)
        self.action_Save_With_Image.setObjectName(u"action_Save_With_Image")
        self.action_Save_With_Image.setCheckable(True)
        self.action_Save_With_Image.setChecked(True)
        self.action_Save_With_Image.setEnabled(False)
        self.action_Close = QAction(MainWindow)
        self.action_Close.setObjectName(u"action_Close")
        self.action_Close.setEnabled(False)
        self.action_Delete_File = QAction(MainWindow)
        self.action_Delete_File.setObjectName(u"action_Delete_File")
        self.action_Delete_File.setEnabled(False)
        self.action_Open = QAction(MainWindow)
        self.action_Open.setObjectName(u"action_Open")
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        self.action_Create_Points = QAction(MainWindow)
        self.action_Create_Points.setObjectName(u"action_Create_Points")
        self.action_Create_Points.setCheckable(True)
        self.action_Create_Points.setEnabled(False)
        self.action_Create_Rectangle = QAction(MainWindow)
        self.action_Create_Rectangle.setObjectName(u"action_Create_Rectangle")
        self.action_Create_Rectangle.setCheckable(True)
        self.action_Create_Rectangle.setEnabled(False)
        self.action_Create_Polygon = QAction(MainWindow)
        self.action_Create_Polygon.setObjectName(u"action_Create_Polygon")
        self.action_Create_Polygon.setCheckable(True)
        self.action_Create_Polygon.setEnabled(False)
        self.action_Edit_Object = QAction(MainWindow)
        self.action_Edit_Object.setObjectName(u"action_Edit_Object")
        self.action_Edit_Object.setCheckable(True)
        self.action_Edit_Object.setEnabled(False)
        self.action_Undo = QAction(MainWindow)
        self.action_Undo.setObjectName(u"action_Undo")
        self.action_Undo.setEnabled(False)
        self.action_Redo = QAction(MainWindow)
        self.action_Redo.setObjectName(u"action_Redo")
        self.action_Redo.setEnabled(False)
        self.action_Manual_Mode = QAction(MainWindow)
        self.action_Manual_Mode.setObjectName(u"action_Manual_Mode")
        self.action_Manual_Mode.setCheckable(True)
        self.action_Manual_Mode.setChecked(True)
        self.action_Manual_Mode.setEnabled(False)
        self.action_SAM_Mode = QAction(MainWindow)
        self.action_SAM_Mode.setObjectName(u"action_SAM_Mode")
        self.action_SAM_Mode.setCheckable(True)
        self.action_SAM_Mode.setEnabled(False)
        self.action_Tutorial = QAction(MainWindow)
        self.action_Tutorial.setObjectName(u"action_Tutorial")
        self.action_About = QAction(MainWindow)
        self.action_About.setObjectName(u"action_About")
        self.action_File_List = QAction(MainWindow)
        self.action_File_List.setObjectName(u"action_File_List")
        self.action_File_List.setCheckable(True)
        self.action_File_List.setChecked(True)
        self.action_Label_List = QAction(MainWindow)
        self.action_Label_List.setObjectName(u"action_Label_List")
        self.action_Label_List.setCheckable(True)
        self.action_Label_List.setChecked(True)
        self.action_Show_Objects = QAction(MainWindow)
        self.action_Show_Objects.setObjectName(u"action_Show_Objects")
        self.action_Show_Objects.setCheckable(True)
        self.action_Show_Objects.setChecked(True)
        self.action_Show_Objects.setEnabled(False)
        self.action_Zoom_In = QAction(MainWindow)
        self.action_Zoom_In.setObjectName(u"action_Zoom_In")
        self.action_Zoom_In.setEnabled(False)
        self.action_Zoom_Out = QAction(MainWindow)
        self.action_Zoom_Out.setObjectName(u"action_Zoom_Out")
        self.action_Zoom_Out.setEnabled(False)
        self.action_Original_Size = QAction(MainWindow)
        self.action_Original_Size.setObjectName(u"action_Original_Size")
        self.action_Original_Size.setEnabled(False)
        self.action_Fit_Window = QAction(MainWindow)
        self.action_Fit_Window.setObjectName(u"action_Fit_Window")
        self.action_Fit_Window.setCheckable(True)
        self.action_Fit_Window.setChecked(True)
        self.action_Fit_Window.setEnabled(False)
        self.action_Finish_Prompt = QAction(MainWindow)
        self.action_Finish_Prompt.setObjectName(u"action_Finish_Prompt")
        self.action_Finish_Prompt.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1280, 22))
        self.menu_FIle = QMenu(self.menuBar)
        self.menu_FIle.setObjectName(u"menu_FIle")
        self.menu_Open_Recent = QMenu(self.menu_FIle)
        self.menu_Open_Recent.setObjectName(u"menu_Open_Recent")
        self.menu_Open_Recent.setEnabled(False)
        self.menu_Edit = QMenu(self.menuBar)
        self.menu_Edit.setObjectName(u"menu_Edit")
        self.menu_View = QMenu(self.menuBar)
        self.menu_View.setObjectName(u"menu_View")
        self.menu_Tools = QMenu(self.menuBar)
        self.menu_Tools.setObjectName(u"menu_Tools")
        self.menu_Help = QMenu(self.menuBar)
        self.menu_Help.setObjectName(u"menu_Help")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.dockWidget_File = QDockWidget(MainWindow)
        self.dockWidget_File.setObjectName(u"dockWidget_File")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.dockWidget_File.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_File)
        self.dockWidget_Label = QDockWidget(MainWindow)
        self.dockWidget_Label.setObjectName(u"dockWidget_Label")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.dockWidget_Label.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_Label)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setAllowedAreas(Qt.AllToolBarAreas)
        MainWindow.addToolBar(Qt.LeftToolBarArea, self.toolBar)

        self.menuBar.addAction(self.menu_FIle.menuAction())
        self.menuBar.addAction(self.menu_Edit.menuAction())
        self.menuBar.addAction(self.menu_View.menuAction())
        self.menuBar.addAction(self.menu_Tools.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())
        self.menu_FIle.addAction(self.action_Open)
        self.menu_FIle.addAction(self.action_Open_Dir)
        self.menu_FIle.addAction(self.menu_Open_Recent.menuAction())
        self.menu_FIle.addSeparator()
        self.menu_FIle.addAction(self.action_Setup_Assist)
        self.menu_FIle.addSeparator()
        self.menu_FIle.addAction(self.action_Next_Image)
        self.menu_FIle.addAction(self.action_Prev_Image)
        self.menu_FIle.addSeparator()
        self.menu_FIle.addAction(self.action_Save)
        self.menu_FIle.addAction(self.action_Save_As)
        self.menu_FIle.addAction(self.action_Auto_Save)
        self.menu_FIle.addSeparator()
        self.menu_FIle.addAction(self.action_Change_Output_Dir)
        self.menu_FIle.addAction(self.action_Save_With_Image)
        self.menu_FIle.addSeparator()
        self.menu_FIle.addAction(self.action_Close)
        self.menu_FIle.addAction(self.action_Delete_File)
        self.menu_FIle.addSeparator()
        self.menu_FIle.addAction(self.action_Quit)
        self.menu_Edit.addAction(self.action_Create_Points)
        self.menu_Edit.addAction(self.action_Create_Rectangle)
        self.menu_Edit.addAction(self.action_Create_Polygon)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Edit_Object)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Finish_Prompt)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Undo)
        self.menu_Edit.addAction(self.action_Redo)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_Manual_Mode)
        self.menu_Edit.addAction(self.action_SAM_Mode)
        self.menu_View.addAction(self.action_File_List)
        self.menu_View.addAction(self.action_Label_List)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.action_Show_Objects)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.action_Zoom_In)
        self.menu_View.addAction(self.action_Zoom_Out)
        self.menu_View.addAction(self.action_Original_Size)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.action_Fit_Window)
        self.menu_Help.addAction(self.action_Tutorial)
        self.menu_Help.addAction(self.action_About)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Setup_Assist)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Next_Image)
        self.toolBar.addAction(self.action_Prev_Image)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Save)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Create_Points)
        self.toolBar.addAction(self.action_Create_Rectangle)
        self.toolBar.addAction(self.action_Create_Polygon)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Edit_Object)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Finish_Prompt)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Manual_Mode)
        self.toolBar.addAction(self.action_SAM_Mode)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Fit_Window)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Label-Anything", None))
        self.action_Open_Dir.setText(QCoreApplication.translate("MainWindow", u"Open &Dir", None))
        self.action_Setup_Assist.setText(QCoreApplication.translate("MainWindow", u"Setup &Assist", None))
        self.action_Next_Image.setText(QCoreApplication.translate("MainWindow", u"&Next Image", None))
        self.action_Prev_Image.setText(QCoreApplication.translate("MainWindow", u"&Prev Image", None))
        self.action_Save.setText(QCoreApplication.translate("MainWindow", u"&Save", None))
        self.action_Save_As.setText(QCoreApplication.translate("MainWindow", u"&Save As", None))
        self.action_Auto_Save.setText(QCoreApplication.translate("MainWindow", u"&Auto Save", None))
        self.action_Change_Output_Dir.setText(QCoreApplication.translate("MainWindow", u"&Change Output Dir", None))
        self.action_Save_With_Image.setText(QCoreApplication.translate("MainWindow", u"Save &With Image", None))
        self.action_Close.setText(QCoreApplication.translate("MainWindow", u"&Close", None))
        self.action_Delete_File.setText(QCoreApplication.translate("MainWindow", u"&Delete File", None))
        self.action_Open.setText(QCoreApplication.translate("MainWindow", u"&Open", None))
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"&Quit", None))
        self.action_Create_Points.setText(QCoreApplication.translate("MainWindow", u"Create &Points", None))
        self.action_Create_Rectangle.setText(QCoreApplication.translate("MainWindow", u"Create &Rectangle", None))
        self.action_Create_Polygon.setText(QCoreApplication.translate("MainWindow", u"Create &Polygon", None))
        self.action_Edit_Object.setText(QCoreApplication.translate("MainWindow", u"&Edit Object", None))
        self.action_Undo.setText(QCoreApplication.translate("MainWindow", u"&Undo", None))
        self.action_Redo.setText(QCoreApplication.translate("MainWindow", u"&Redo", None))
        self.action_Manual_Mode.setText(QCoreApplication.translate("MainWindow", u"&Manual Mode", None))
        self.action_SAM_Mode.setText(QCoreApplication.translate("MainWindow", u"&SAM Mode", None))
        self.action_Tutorial.setText(QCoreApplication.translate("MainWindow", u"&Tutorial", None))
        self.action_About.setText(QCoreApplication.translate("MainWindow", u"&About", None))
        self.action_File_List.setText(QCoreApplication.translate("MainWindow", u"&File List", None))
        self.action_Label_List.setText(QCoreApplication.translate("MainWindow", u"&Label List", None))
        self.action_Show_Objects.setText(QCoreApplication.translate("MainWindow", u"&Show Objects", None))
#if QT_CONFIG(tooltip)
        self.action_Show_Objects.setToolTip(QCoreApplication.translate("MainWindow", u"Show Objects", None))
#endif // QT_CONFIG(tooltip)
        self.action_Zoom_In.setText(QCoreApplication.translate("MainWindow", u"Zoom &In", None))
        self.action_Zoom_Out.setText(QCoreApplication.translate("MainWindow", u"&Zoom Out", None))
        self.action_Original_Size.setText(QCoreApplication.translate("MainWindow", u"&Original Size", None))
        self.action_Fit_Window.setText(QCoreApplication.translate("MainWindow", u"Fit Window", None))
        self.action_Finish_Prompt.setText(QCoreApplication.translate("MainWindow", u"&Finish Prompt", None))
        self.menu_FIle.setTitle(QCoreApplication.translate("MainWindow", u"&FIle", None))
        self.menu_Open_Recent.setTitle(QCoreApplication.translate("MainWindow", u"Open &Recent", None))
        self.menu_Edit.setTitle(QCoreApplication.translate("MainWindow", u"&Edit", None))
        self.menu_View.setTitle(QCoreApplication.translate("MainWindow", u"&View", None))
        self.menu_Tools.setTitle(QCoreApplication.translate("MainWindow", u"&Tools", None))
        self.menu_Help.setTitle(QCoreApplication.translate("MainWindow", u"&Help", None))
        self.dockWidget_File.setWindowTitle(QCoreApplication.translate("MainWindow", u"File List", None))
        self.dockWidget_Label.setWindowTitle(QCoreApplication.translate("MainWindow", u"Label List", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

