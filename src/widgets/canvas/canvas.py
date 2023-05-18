# -*- coding: utf-8 -*-
# J094
# 2023.05.10
import os
import sys
sys.path.append(os.path.realpath("."))

import src.utils.qt as utils_qt
import src.utils.image as utils_image
from src.widgets.objects.guide_line import GuideLine
from src.widgets.objects.draw_object import DrawObject
from src.widgets.objects.draw_points import DrawPoints
from src.widgets.objects.draw_rectangle import DrawRectangle
from src.widgets.objects.draw_polygon import DrawPolygon
from src.widgets.objects.draw_lines import DrawLines
from src.widgets.objects.prompt_object import PromptObject

import time
import numpy as np
from enum import Enum

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, 
    QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsEllipseItem,
    QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsPathItem,
)
from PySide6.QtGui import (
    QPainter, QColor, QPen, QBrush, QPainterPath, QPixmap, QImage
)


class Canvas(QGraphicsView):
    
    class ZoomMode(Enum):
        MANUAL = 0
        FIT_WINDOW = 1

    class StatusMode(Enum):
        CREATE = 0
        EDIT = 1

    class LabelMode(Enum):
        MANUAL = 0
        SAM = 1
        YOLO = 2
    
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        self.zoom_mode = Canvas.ZoomMode.FIT_WINDOW
        self.zoom_factor = 1.2
        
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing, True)
        self.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontSavePainterState, True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
    def zoom_in(self):
        self.zoom(zoom_factor=self.zoom_factor)
    
    def zoom_out(self):
        self.zoom(zoom_factor=1/self.zoom_factor)
    
    def zoom_fit_window(self):
        # scene() returns CanvasScene
        # self.scene()
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        DrawObject.scale_factor = self.transform().m11()
        for canvas_object in self.scene().canvas_objects:
            canvas_object.update_items()
        if self.scene().draw_object is not None:
            self.scene().draw_object.update_items()
        
    
    def zoom_original(self):
        zoom_factor = 1/self.transform().m11()
        self.zoom(zoom_factor=zoom_factor)
    
    def zoom(self, zoom_factor, point=None):
        mouse_old = self.mapToScene(point.toPoint()) if point else None

        # Limit zoom ranges: 0.1 ~ 10
        scaled_width = self.transform().scale(
            zoom_factor, zoom_factor,
        ).mapRect(QRectF(0, 0, 1, 1)).width()
        if scaled_width > 10 or scaled_width < 0.1:
            return

        self.scale(zoom_factor, zoom_factor)
        if point is not None:
            mouse_now = self.mapToScene(point.toPoint())
            center_now = self.mapToScene(
                self.viewport().width() // 2, self.viewport().height() // 2,
            )
            center_new = mouse_old - mouse_now + center_now
            self.centerOn(center_new)
        
        DrawObject.scale_factor = DrawObject.scale_factor * zoom_factor
        for canvas_object in self.scene().canvas_objects:
            canvas_object.update_items()
        if self.scene().draw_object is not None:
            self.scene().draw_object.update_items()
    
    def resizeEvent(self, event):
        if self.zoom_mode == Canvas.ZoomMode.FIT_WINDOW:
            self.zoom_fit_window()
        return super().resizeEvent(event)
    
    def wheelEvent(self, event):
        angle = event.angleDelta()
        angle_y = angle.y()
        point = event.position()
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # parent() returns MainWindow
            # self.parent()
            self.parent().ui.action_Fit_Window.setChecked(False)
            self.zoom_mode = Canvas.ZoomMode.MANUAL
            if angle_y > 0:
                self.zoom(zoom_factor=self.zoom_factor, point=point)
            elif angle_y < 0:
                self.zoom(zoom_factor=1/self.zoom_factor, point=point)
        else:
            # Zoom should not effect scrollbar
            return super().wheelEvent(event)


class CanvasScene(QGraphicsScene):
    def __init__(self, parent=None, main_window=None):
        super(CanvasScene, self).__init__(parent)
        self.main_window = main_window
        self.scene_rect = None
        self.image_data = None
        self.guide_line_x = None
        self.guide_line_y = None
        self.canvas_objects = []
        self.draw_object = None
        self.draw_object_type = DrawObject.DrawObjectType.POLYGON
        self.prompt_object = None
        self.prompt_object_type = PromptObject.PromptObjectType.SAM
        self.label_mode = Canvas.LabelMode.MANUAL
        self.status_mode = None
        self.point_to_add = None
        self.snapping = True
        
    def load_image(self, image_path=None, image_data=None):
        self.clear()
        self.reset_status()
        # views() returns all views of this scene
        # self.views()
        if image_path is not None:
            self.image_data = utils_image.load_image_data(image_path)
        elif image_data is not None:
            self.image_data = image_data
        image = QImage.fromData(self.image_data)
        image_pixmap = QPixmap.fromImage(image)
        self.image_item = QGraphicsPixmapItem()
        self.image_item.setZValue(0)
        self.image_item.setPixmap(image_pixmap)
        self.addItem(self.image_item)
        # Fix scene size
        fix_width = image_pixmap.width()
        fix_height = image_pixmap.height()
        self.scene_rect = QRectF(0, 0, fix_width, fix_height)
        self.setSceneRect(self.scene_rect)
        # Fit window
        self.views()[0].zoom_mode = Canvas.ZoomMode.FIT_WINDOW
        self.views()[0].zoom_fit_window()
        self.status_mode = Canvas.StatusMode.CREATE
        
    def load_objects(self, objects):
        for object in objects:
            object_type = object["object_type"]
            if object_type == "points":
                canvas_object = DrawPoints(canvas_scene=self)
            elif object_type == "rectangle":
                canvas_object = DrawRectangle(canvas_scene=self)
            elif object_type == "polygon":
                canvas_object = DrawPolygon(canvas_scene=self)
            elif object_type == "lines":
                canvas_object = DrawLines(canvas_scene=self)
            canvas_object.label_name = object["label_name"]
            canvas_object.group_id = object["group_id"]
            for point in object["points"]:
                canvas_object.add_point(QPointF(*point))
            if canvas_object.draw_object_type == DrawObject.DrawObjectType.POLYGON:
                canvas_object.add_point(QPointF(*object["points"][0]))
            self.canvas_objects.append(canvas_object)
            self.main_window.add_label(canvas_object)
    
    def reset_objects(self):
        self.draw_object = None
        self.prompt_object = None
        
    def reset_status(self):
        self.guide_line_x = None
        self.guide_line_y = None
        self.canvas_objects = []
        self.reset_objects()
        
    def finish_draw_manual(self):
        self.canvas_objects.append(self.draw_object)
        self.main_window.new_label()
        self.reset_objects()
        # print(self.canvas_objects)
    
    def finish_draw_sam(self):
        pass
    
    def finish_draw_yolo(self):
        pass
        
    def mousePressEvent(self, event):
        # scene_pos = event.scenePos()
        # if scene_pos.x() < 0: scene_pos.setX(0)
        # if scene_pos.x() > self.width(): scene_pos.setX(self.width())
        # if scene_pos.y() < 0: scene_pos.setY(0)
        # if scene_pos.y() > self.height(): scene_pos.setY(self.height())
        
        if event.button() == Qt.MouseButton.LeftButton:
            #TODO: Left Click -> Draw Point
            if self.status_mode == Canvas.StatusMode.CREATE:
                #TODO: CREATE mode
                if self.label_mode == Canvas.LabelMode.MANUAL:
                    if self.draw_object is None:
                        if self.draw_object_type == DrawObject.DrawObjectType.POINTS:
                            self.draw_object = DrawPoints(canvas_scene=self)
                            self.draw_object.add_point(self.point_to_add)
                            self.draw_object.update_items()
                            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                                self.draw_object.closed = True
                                self.finish_draw_manual()
                        elif self.draw_object_type == DrawObject.DrawObjectType.RECTANGLE:
                            self.draw_object = DrawRectangle(canvas_scene=self)
                            self.draw_object.add_point(self.point_to_add)
                            self.draw_object.update_items()
                        elif self.draw_object_type == DrawObject.DrawObjectType.POLYGON:
                            self.draw_object = DrawPolygon(canvas_scene=self)
                            self.draw_object.add_point(self.point_to_add)
                            self.draw_object.update_items()
                        elif self.draw_object_type == DrawObject.DrawObjectType.LINES:
                            self.draw_object = DrawLines(canvas_scene=self)
                            self.draw_object.add_point(self.point_to_add)
                            self.draw_object.update_items()
                    else:
                        if self.draw_object_type == DrawObject.DrawObjectType.POINTS:
                            self.draw_object.add_point(self.point_to_add)
                            self.draw_object.update_items()
                            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                                self.draw_object.closed = True
                                self.finish_draw_manual()
                        elif self.draw_object_type == DrawObject.DrawObjectType.RECTANGLE:
                            self.draw_object.add_point(self.point_to_add)
                            self.draw_object.update_items()
                            if self.draw_object.closed:
                                self.finish_draw_manual()
                        elif self.draw_object_type == DrawObject.DrawObjectType.POLYGON:
                            self.draw_object.add_point(self.point_to_add)
                            self.draw_object.update_items()
                            if self.draw_object.closed:
                                self.finish_draw_manual()
                        elif self.draw_object_type == DrawObject.DrawObjectType.LINES:
                            self.draw_object.add_point(self.point_to_add)
                            self.draw_object.update_items()
                            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                                self.draw_object.closed = True
                                self.finish_draw_manual()
                elif self.label_mode == Canvas.LabelMode.SAM:
                    pass
                elif self.label_mode == Canvas.LabelMode.YOLO:
                    pass
            elif self.status_mode == Canvas.StatusMode.EDIT:
                #TODO: EDIT mode
                if self.label_mode == Canvas.LabelMode.MANUAL:
                    pass
                elif self.label_mode == Canvas.LabelMode.SAM:
                    pass
                elif self.label_mode == Canvas.LabelMode.YOLO:
                    pass
        elif (event.button() == Qt.MouseButton.RightButton
              and self.status_mode == Canvas.StatusMode.EDIT):
            #TODO: Right Click -> Open Menu
            pass
        self.update()
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        inside_scene = True
        scene_pos = event.scenePos()
        if scene_pos.x() < 0: 
            scene_pos.setX(0)
        if scene_pos.x() > self.width(): 
            scene_pos.setX(self.width())
        if scene_pos.y() < 0: 
            scene_pos.setY(0)
        if scene_pos.y() > self.height(): 
            scene_pos.setY(self.height())
        self.point_to_add = scene_pos

        if self.draw_object is not None:
            if self.draw_object_type == DrawObject.DrawObjectType.RECTANGLE:
                self.draw_object.points[1] = self.point_to_add
                self.draw_object.update_items()
            elif self.draw_object_type == DrawObject.DrawObjectType.POLYGON:
                if (self.snapping
                    and len(self.draw_object.points) >= 3):
                    point_1 = self.draw_object.points[0]
                    point_2 = self.point_to_add
                    distance = utils_qt.distance_points(point_1, point_2)
                    if distance <= 10:
                        self.point_to_add = point_1
                        self.draw_object.point_color = DrawObject.default_selected_point_color
                        self.draw_object.point_size_base = 2 * DrawObject.default_point_size_base
                    else:
                        self.draw_object.point_color = DrawObject.default_point_color
                        self.draw_object.point_size_base = DrawObject.default_point_size_base
                self.draw_object.last_point = self.point_to_add
                self.draw_object.update_items()
            elif self.draw_object_type == DrawObject.DrawObjectType.LINES:
                self.draw_object.last_point = self.point_to_add
                self.draw_object.update_items()

        # Cross shows only inside scene
        # start = time.perf_counter()
        if self.status_mode == Canvas.StatusMode.CREATE:
            self.views()[0].setCursor(Qt.CursorShape.CrossCursor)
        else:
            self.views()[0].setCursor(Qt.CursorShape.ArrowCursor)

        if self.draw_object_type == DrawObject.DrawObjectType.RECTANGLE:
            if self.guide_line_x is None:
                self.guide_line_x = GuideLine(0, self.point_to_add.y(), 
                                              self.width(), self.point_to_add.y())
                self.addItem(self.guide_line_x)
            else:
                self.guide_line_x.setLine(0, self.point_to_add.y(), 
                                          self.width(), self.point_to_add.y())
            if self.guide_line_y is None:
                self.guide_line_y = GuideLine(self.point_to_add.x(), 0, 
                                              self.point_to_add.x(), self.height())
                self.addItem(self.guide_line_y)
            else:
                self.guide_line_y.setLine(self.point_to_add.x(), 0, 
                                          self.point_to_add.x(), self.height())
        else: # POINTS, POLYGON, LINES
            if self.guide_line_x is not None:
                self.removeItem(self.guide_line_x)
                self.guide_line_x = None
            if self.guide_line_y is not None:
                self.removeItem(self.guide_line_y)
                self.guide_line_y = None
        # print(time.perf_counter() - start)

        if self.image_data is not None:
            self.main_window.statusBar().showMessage("Current Pose: ({}, {})".format(
                int(self.point_to_add.x()),
                int(self.point_to_add.y()),
            ))

        self.update()
        return super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        key = event.key()