# -*- coding: utf-8 -*-
# J094
# 2023.05.10
import os
import sys
sys.path.append(os.path.realpath("."))

from src.widgets.file_list.file_list import FileList
from src.widgets.label_list.label_list import LabelList
from src.widgets.label_dialog.label_dialog import LabelDialog
from src.widgets.canvas.canvas import Canvas, CanvasScene
from src.widgets.objects.draw_object import DrawObject
from src.widgets.objects.label_file import LabelFile
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from src.widgets.main_window.ui_form import Ui_MainWindow

import imgviz
from enum import Enum

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel,
)
from PySide6.QtGui import QImageReader, QImage, QColor


LABEL_COLORMAP = imgviz.label_colormap()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui()
        
        self.image_dir = None
        self.image_path = None
        self.image_paths = []
        self.output_dir = None
        self.output_path = None
        self.output_paths = []
        self.label_names = []
        self.canvas_objects = []
        self.label_file = None
        # Key: label_name
        # Value: r, g, b
        self.color_map = {}
        # True: changes not saved
        # False: all changes saved
        self.dirty = False
        
        self.action_startup = [
            self.ui.menu_Open_Recent,
            self.ui.action_Next_Image,
            self.ui.action_Prev_Image,
            self.ui.action_Save,
            self.ui.action_Save_As,
            self.ui.action_Close,
            self.ui.action_Delete_File,
            self.ui.action_Zoom_In,
            self.ui.action_Zoom_Out,
            self.ui.action_Original_Size,
        ]
        self.action_startup_checked = [
            self.ui.action_Save_With_Image,
            self.ui.action_Manual_Mode,
            self.ui.action_Fit_Window,
            self.ui.action_Show_Objects,
        ]
        self.action_startup_unchecked = [
            self.ui.action_Auto_Save,
            self.ui.action_Create_Points,
            self.ui.action_Create_Rectangle,
            self.ui.action_Create_Polygon,
            self.ui.action_Create_Lines,
            self.ui.action_Edit_Object,
            self.ui.action_SAM_Mode,
        ]

        self.setup_action_startup(False)
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
        
        self.dialog_label_dialog = LabelDialog(self)
        
    def setup_slot(self):
        self.ui.action_Open.triggered.connect(self.slot_open)
        self.ui.action_Open_Dir.triggered.connect(self.slot_open_dir)
        self.ui.action_Change_Output_Dir.triggered.connect(self.slot_change_output_dir)
        self.ui.action_Next_Image.triggered.connect(self.slot_next_image)
        self.ui.action_Prev_Image.triggered.connect(self.slot_prev_image)
        self.ui.action_Save.triggered.connect(self.slot_save)
        self.ui.action_Close.triggered.connect(self.slot_close)
        self.ui.action_Create_Points.triggered.connect(self.slot_create_points)
        self.ui.action_Create_Rectangle.triggered.connect(self.slot_create_rectangle)
        self.ui.action_Create_Polygon.triggered.connect(self.slot_create_polygon)
        self.ui.action_Create_Lines.triggered.connect(self.slot_create_lines)
        self.ui.action_Edit_Object.triggered.connect(self.slot_edit_object)
        self.ui.action_Manual_Mode.triggered.connect(self.slot_manual_mode)
        self.ui.action_SAM_Mode.triggered.connect(self.slot_sam_mode)
        self.ui.action_Zoom_In.triggered.connect(self.slot_zoom_in)
        self.ui.action_Zoom_Out.triggered.connect(self.slot_zoom_out)
        self.ui.action_Original_Size.triggered.connect(self.slot_original_size)
        self.ui.action_Fit_Window.triggered.connect(self.slot_fit_window)
        
    def setup_action_startup(self, status):
        for action in self.action_startup:
            action.setEnabled(status)
        for action in self.action_startup_checked:
            action.setEnabled(status)
            action.setChecked(True)
        for action in self.action_startup_unchecked:
            action.setEnabled(status)
            action.setChecked(False)
        
    def reset_status(self):
        pass
        
    def load_file(self):
        if self.image_path in self.image_paths:
            index = self.image_paths.index(self.image_path)
            self.widget_file_list.ui.listWidget_Files.setCurrentRow(index)
            self.widget_file_list.ui.label_Current.setText(
                '{}'.format(index+1)
            )
            self.widget_file_list.update()
        else:
            self.widget_file_list.ui.listWidget_Files.clear()
        
        self.label_file = LabelFile(self.output_path)
        if self.label_file.image_data is not None:
            self.graphicsScene_canvas_scene.load_image(image_data=self.label_file.image_data)
        else:
            self.graphicsScene_canvas_scene.load_image(image_path=self.image_path)
        self.label_names.clear()
        self.graphicsScene_canvas_scene.load_objects(self.label_file.objects)
        self.canvas_objects = self.graphicsScene_canvas_scene.canvas_objects
        self.widget_label_list.update_list()
        self.dialog_label_dialog.update_list()
        self.dialog_label_dialog.clear_text()

        self.setWindowTitle(f"Label-Anything: {self.image_path}")
        
    def save_file(self):
        self.label_file.image_size = [self.graphicsScene_canvas_scene.scene_rect.width(),
                                      self.graphicsScene_canvas_scene.scene_rect.height()]
        self.label_file.image_data = self.graphicsScene_canvas_scene.image_data
        self.label_file.image_path = os.path.relpath(
            self.output_path,
            os.path.dirname(self.image_path),
        )
        self.label_file.file_path = self.output_path
        self.label_file.objects.clear()
        for canvas_object in self.canvas_objects:
            draw_object_type = canvas_object.draw_object_type
            if draw_object_type == DrawObject.DrawObjectType.POINTS:
                object_type = "points"
            elif draw_object_type == DrawObject.DrawObjectType.RECTANGLE:
                object_type = "rectangle"
            elif draw_object_type == DrawObject.DrawObjectType.POLYGON:
                object_type = "polygon"
            elif draw_object_type == DrawObject.DrawObjectType.LINES:
                object_type = "lines"
            label_name = canvas_object.label_name
            group_id = canvas_object.group_id
            points = []
            for q_point in canvas_object.points:
                point = [q_point.x(), q_point.y()]
                points.append(point)
            object = {
                "label_name": label_name,
                "group_id": group_id,
                "object_type": object_type,
                "points": points,
            }
            self.label_file.objects.append(object)
        self.label_file.save()
        
    def load_dir(self):
        if self.image_dir is None: return
        output_dir = self.output_dir if self.output_dir is not None else self.image_dir
        suffixes = tuple(['{}'.format(fmt.data().decode('ascii').lower()) 
                          for fmt in QImageReader.supportedImageFormats()])
        image_names = os.listdir(self.image_dir)
        image_names = sorted(image_names)
        self.image_paths.clear()
        self.output_paths.clear()
        for image_name in image_names:
            if image_name.lower().endswith(suffixes):
                image_path = os.path.join(self.image_dir, image_name)
                self.image_paths.append(image_path)
                image_base = os.path.splitext(image_name)[0]
                output_name = image_base + ".json"
                output_path = os.path.join(output_dir, output_name)
                # print(output_path)
                self.output_paths.append(output_path)

        self.widget_file_list.update_list()
        
        if len(self.image_paths) > 0:
            self.image_path = self.image_paths[0]
            self.output_path = self.output_paths[0]
            self.load_file()
    
    def update_canvas_object(self, canvas_object):
        r, g, b = LABEL_COLORMAP[(self.label_names.index(canvas_object.label_name) + 1) %
                                  len(LABEL_COLORMAP)]
        self.color_map[canvas_object.label_name] = [r, g, b]
        canvas_object.line_color = QColor(r, g, b)
        canvas_object.point_color = QColor(r, g, b)
        canvas_object.point_size_base = DrawObject.default_point_size_base
        canvas_object.update_items()
        
    def add_label(self, canvas_object):
        label_name = canvas_object.label_name
        if label_name not in self.label_names:
            self.label_names.append(label_name)
        self.update_canvas_object(canvas_object)
            
    def new_label(self):
        ok = self.dialog_label_dialog.exec()
        if not ok:
            return False
        label_name = self.dialog_label_dialog.ui.lineEdit_Label_Name.text()
        group_id = self.dialog_label_dialog.ui.lineEdit_Group_ID.text()

        if label_name not in self.label_names:
            self.label_names.append(label_name)

        self.canvas_objects = self.graphicsScene_canvas_scene.canvas_objects
        canvas_object = self.canvas_objects[-1]
        canvas_object.label_name = label_name
        canvas_object.group_id = group_id
        
        self.update_canvas_object(canvas_object)
        self.widget_label_list.update_list()
        self.dialog_label_dialog.update_list()
        return True
        
    def change_canvas_status(self, status_mode=None, label_mode=None, object_type=None):
        if status_mode is not None:
            self.graphicsScene_canvas_scene.status_mode = status_mode
            self.graphicsScene_canvas_scene.reset_objects()
        if label_mode is not None:
            self.graphicsScene_canvas_scene.label_mode = label_mode
            self.graphicsScene_canvas_scene.reset_objects()
        if object_type is not None:
            self.graphicsScene_canvas_scene.draw_object_type = object_type
            if self.graphicsScene_canvas_scene.label_mode == Canvas.LabelMode.MANUAL:
                self.graphicsScene_canvas_scene.reset_objects()
        
    def slot_open(self):
        path = os.path.dirname(self.image_path) if self.image_path else "."
        formats = [
            "*.{}".format(fmt.data().decode())
            for fmt in QImageReader.supportedImageFormats()
        ]
        filters = "Image Files ({})".format(
            " ".join(formats)
        )
        image_dialog = QFileDialog(self)
        image_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        image_dialog.setNameFilter(filters)
        image_dialog.setWindowTitle("Choose Image File")
        image_dialog.setWindowFilePath(path)
        if image_dialog.exec():
            image_path = image_dialog.selectedFiles()[0]
            if image_path is not None:
                self.image_path = image_path
                image_base = os.path.splitext(image_path)[0]
                self.output_path = image_base + ".json"
                print("Choose Image File:", self.image_path)
                self.load_file()
        self.setup_action_startup(True)
    
    def slot_open_dir(self):
        path = os.path.dirname(self.image_dir) if self.image_dir else "."
        image_dir = QFileDialog.getExistingDirectory(
            self,
            "Choose Image Directory",
            path,
        )
        if image_dir is not None:
            self.image_dir = image_dir
            print("Choose Image Directory:", self.image_dir)
            self.load_dir()
        self.setup_action_startup(True)
            
    def slot_change_output_dir(self):
        path = os.path.dirname(self.output_dir) if self.output_dir else "."
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Choose Output Directory",
            path,
        )
        if output_dir is not None:
            self.output_dir = output_dir
            print("Choose Output Directory:", self.output_dir)
            self.load_dir()
            
    def slot_save(self):
        self.save_file()
        self.widget_file_list.update_list()
            
    def slot_next_image(self):
        index = self.widget_file_list.ui.listWidget_Files.currentRow()
        if index + 1 < len(self.image_paths):
            index = index + 1
        else:
            return
        self.image_path = self.image_paths[index]
        self.output_path = self.output_paths[index]
        self.load_file()
        
    def slot_prev_image(self):
        index = self.widget_file_list.ui.listWidget_Files.currentRow()
        if index - 1 >= 0:
            index = index - 1
        else:
            return
        self.image_path = self.image_paths[index]
        self.output_path = self.output_paths[index]
        self.load_file()
    
    def slot_close(self):
        self.setup_action_startup(False)
        
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
        
    def slot_create_points(self):
        self.ui.action_Create_Points.setEnabled(False)
        self.ui.action_Create_Points.setChecked(True)
        self.ui.action_Create_Rectangle.setEnabled(True)
        self.ui.action_Create_Rectangle.setChecked(False)
        self.ui.action_Create_Polygon.setEnabled(True)
        self.ui.action_Create_Polygon.setChecked(False)
        self.ui.action_Create_Lines.setEnabled(True)
        self.ui.action_Create_Lines.setChecked(False)
        self.ui.action_Edit_Object.setEnabled(True)
        self.ui.action_Edit_Object.setChecked(False)
        self.change_canvas_status(status_mode=Canvas.StatusMode.CREATE, 
                                  object_type=DrawObject.DrawObjectType.POINTS)
        
    def slot_create_rectangle(self):
        self.ui.action_Create_Points.setEnabled(True)
        self.ui.action_Create_Points.setChecked(False)
        self.ui.action_Create_Rectangle.setEnabled(False)
        self.ui.action_Create_Rectangle.setChecked(True)
        self.ui.action_Create_Polygon.setEnabled(True)
        self.ui.action_Create_Polygon.setChecked(False)
        self.ui.action_Create_Lines.setEnabled(True)
        self.ui.action_Create_Lines.setChecked(False)
        self.ui.action_Edit_Object.setEnabled(True)
        self.ui.action_Edit_Object.setChecked(False)
        self.change_canvas_status(status_mode=Canvas.StatusMode.CREATE, 
                                  object_type=DrawObject.DrawObjectType.RECTANGLE)
        
    def slot_create_polygon(self):
        self.ui.action_Create_Points.setEnabled(True)
        self.ui.action_Create_Points.setChecked(False)
        self.ui.action_Create_Rectangle.setEnabled(True)
        self.ui.action_Create_Rectangle.setChecked(False)
        self.ui.action_Create_Polygon.setEnabled(False)
        self.ui.action_Create_Polygon.setChecked(True)
        self.ui.action_Create_Lines.setEnabled(True)
        self.ui.action_Create_Lines.setChecked(False)
        self.ui.action_Edit_Object.setEnabled(True)
        self.ui.action_Edit_Object.setChecked(False)
        self.change_canvas_status(status_mode=Canvas.StatusMode.CREATE, 
                                  object_type=DrawObject.DrawObjectType.POLYGON)
        
    def slot_create_lines(self):
        self.ui.action_Create_Points.setEnabled(True)
        self.ui.action_Create_Points.setChecked(False)
        self.ui.action_Create_Rectangle.setEnabled(True)
        self.ui.action_Create_Rectangle.setChecked(False)
        self.ui.action_Create_Polygon.setEnabled(True)
        self.ui.action_Create_Polygon.setChecked(False)
        self.ui.action_Create_Lines.setEnabled(False)
        self.ui.action_Create_Lines.setChecked(True)
        self.ui.action_Edit_Object.setEnabled(True)
        self.ui.action_Edit_Object.setChecked(False)
        self.change_canvas_status(status_mode=Canvas.StatusMode.CREATE, 
                                  object_type=DrawObject.DrawObjectType.LINES)
        
    def slot_edit_object(self):
        self.ui.action_Create_Points.setEnabled(True)
        self.ui.action_Create_Points.setChecked(False)
        self.ui.action_Create_Rectangle.setEnabled(True)
        self.ui.action_Create_Rectangle.setChecked(False)
        self.ui.action_Create_Polygon.setEnabled(True)
        self.ui.action_Create_Polygon.setChecked(False)
        self.ui.action_Create_Lines.setEnabled(True)
        self.ui.action_Create_Lines.setChecked(False)
        self.ui.action_Edit_Object.setEnabled(False)
        self.ui.action_Edit_Object.setChecked(True)
        self.change_canvas_status(status_mode=Canvas.StatusMode.EDIT)
        
    def slot_manual_mode(self):
        self.ui.action_Create_Points.setEnabled(True)
        self.ui.action_Create_Points.setChecked(False)
        self.ui.action_Create_Rectangle.setEnabled(True)
        self.ui.action_Create_Rectangle.setChecked(False)
        self.ui.action_Create_Polygon.setEnabled(True)
        self.ui.action_Create_Polygon.setChecked(False)
        self.ui.action_Create_Lines.setEnabled(True)
        self.ui.action_Create_Lines.setChecked(False)
        self.ui.action_Edit_Object.setEnabled(True)
        self.ui.action_Edit_Object.setChecked(False)
        self.ui.action_Manual_Mode.setChecked(True)
        self.ui.action_Manual_Mode.setEnabled(False)
        self.ui.action_SAM_Mode.setChecked(False)
        self.ui.action_SAM_Mode.setEnabled(True)
        self.change_canvas_status(label_mode=Canvas.LabelMode.MANUAL)
        
    def slot_sam_mode(self):
        self.ui.action_Create_Points.setEnabled(True)
        self.ui.action_Create_Points.setChecked(False)
        self.ui.action_Create_Rectangle.setEnabled(True)
        self.ui.action_Create_Rectangle.setChecked(False)
        self.ui.action_Create_Polygon.setEnabled(True)
        self.ui.action_Create_Polygon.setChecked(False)
        self.ui.action_Create_Lines.setEnabled(True)
        self.ui.action_Create_Lines.setChecked(False)
        self.ui.action_Edit_Object.setEnabled(True)
        self.ui.action_Edit_Object.setChecked(False)
        self.ui.action_Manual_Mode.setChecked(False)
        self.ui.action_Manual_Mode.setEnabled(True)
        self.ui.action_SAM_Mode.setChecked(True)
        self.ui.action_SAM_Mode.setEnabled(False)
        self.change_canvas_status(label_mode=Canvas.LabelMode.SAM)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
