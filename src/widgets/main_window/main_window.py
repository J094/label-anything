# -*- coding: utf-8 -*-
# J094
# 2023.05.10
import os
import sys
sys.path.append(os.path.realpath("."))

from src.widgets.file_list.file_list import FileList
from src.widgets.label_list.label_list import LabelList
from src.widgets.canvas import Canvas, CanvasScene
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from src.widgets.main_window.ui_form import Ui_MainWindow

from enum import Enum

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel,
)
from PySide6.QtGui import QImageReader, QImage


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui()
        
        self.file_dir = "data/image"
        self.file_path = None
        self.file_paths = []
        self.label_dir = None
        self.label_path = None
        self.label_paths = []

        # True: changes not saved
        # False: all changes saved
        self.dirty = False

        self.reset_status()
        self.setup_slot()
        
    def setup_ui(self):
        self.widget_file_list = FileList(main_window=self)
        self.ui.dockWidget_File.setWidget(self.widget_file_list)
        self.widget_label_list = LabelList(main_window=self)
        self.ui.dockWidget_Label.setWidget(self.widget_label_list)
        
        self.graphicsScene_canvas_scene = CanvasScene(main_window=self)
        self.graphicsView_canvas = Canvas()
        self.graphicsView_canvas.setScene(self.graphicsScene_canvas_scene)
        self.setCentralWidget(self.graphicsView_canvas)
        
    def setup_slot(self):
        self.ui.action_Open.triggered.connect(self.slot_open)
        self.ui.action_Open_Dir.triggered.connect(self.slot_open_dir)
        self.ui.action_Next_Image.triggered.connect(self.slot_next_image)
        self.ui.action_Prev_Image.triggered.connect(self.slot_prev_image)
        self.ui.action_Fit_Window.triggered.connect(self.slot_fit_window)
        self.ui.action_Zoom_In.triggered.connect(self.slot_zoom_in)
        self.ui.action_Zoom_Out.triggered.connect(self.slot_zoom_out)
        self.ui.action_Original_Size.triggered.connect(self.slot_original_size)
        
    def reset_status(self):
        pass
        
    def load_file(self):
        if self.file_path in self.file_paths:
            self.widget_file_list.ui.listWidget_Files.setCurrentRow(
                self.file_paths.index(self.file_path)
            )
            self.widget_file_list.ui.label_Current.setText(
                '{}'.format(self.file_paths.index(self.file_path)+1)
            )
            self.widget_file_list.update()

        self.graphicsScene_canvas_scene.load_image(self.file_path)
        
    def load_dir(self):
        suffixes = tuple(['{}'.format(fmt.data().decode('ascii').lower()) 
                          for fmt in QImageReader.supportedImageFormats()])
        file_names = os.listdir(self.file_dir)
        file_names = sorted(file_names)
        self.file_paths.clear()
        for file_name in file_names:
            if file_name.lower().endswith(suffixes):
                file_path = os.path.join(self.file_dir, file_name)
                self.file_paths.append(file_path)
        
        self.widget_file_list.update_list()
        
        if len(self.file_paths) > 0:
            self.file_path = self.file_paths[0]
            self.load_file()
        
    def slot_open(self):
        path = os.path.dirname(self.file_path) if self.file_path else "."
        formats = [
            "*.{}".format(fmt.data().decode())
            for fmt in QImageReader.supportedImageFormats()
        ]
        filters = "Image files ({})".format(
            " ".join(formats)
        )
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter(filters)
        file_dialog.setWindowTitle("Choose Image File")
        file_dialog.setWindowFilePath(path)
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            if file_path is not None:
                self.file_path = file_path
                print("Open:", self.file_path)
                self.load_file()
    
    def slot_open_dir(self):
        path = os.path.dirname(self.file_dir) if self.file_dir else "."
        file_dir = QFileDialog.getExistingDirectory(
            self,
            "Choose Image Directory",
            path,
        )
        if file_dir is not None:
            self.file_dir = file_dir
            print("Open:", self.file_dir)
            self.load_dir()
            
    def slot_next_image(self):
        index = self.widget_file_list.ui.listWidget_Files.currentRow()
        if index + 1 < len(self.file_paths):
            index = index + 1
        else:
            return
        self.file_path = self.file_paths[index]
        self.load_file()
        
    def slot_prev_image(self):
        index = self.widget_file_list.ui.listWidget_Files.currentRow()
        if index - 1 >= 0:
            index = index - 1
        else:
            return
        self.file_path = self.file_paths[index]
        self.load_file()
        
    def slot_fit_window(self):
        checked = self.ui.action_Fit_Window.isChecked()
        if checked:
            self.graphicsView_canvas.zoom_mode = Canvas.ZoomMode.FIT_WINDOW
            self.graphicsView_canvas.zoom_fit_window()
        else:
            self.graphicsView_canvas.zoom_mode = Canvas.ZoomMode.MANUAL
            self.graphicsView_canvas.zoom_original()
            
    def slot_zoom_in(self):
        self.ui.action_Fit_Window.setChecked(False)
        self.graphicsView_canvas.zoom_mode = Canvas.ZoomMode.MANUAL
        self.graphicsView_canvas.zoom_in()
        
    def slot_zoom_out(self):
        self.ui.action_Fit_Window.setChecked(False)
        self.graphicsView_canvas.zoom_mode = Canvas.ZoomMode.MANUAL
        self.graphicsView_canvas.zoom_out()
        
    def slot_original_size(self):
        self.ui.action_Fit_Window.setChecked(False)
        self.graphicsView_canvas.zoom_mode = Canvas.ZoomMode.MANUAL
        self.graphicsView_canvas.zoom_original()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
