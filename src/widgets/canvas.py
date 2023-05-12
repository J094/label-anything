# -*- coding: utf-8 -*-
# J094
# 2023.05.10
import os
import sys
sys.path.append(os.path.realpath("."))

from src.widgets.objects.guide_line import GuideLine
from src.widgets.objects.object import Object

import time
import numpy as np
from enum import Enum
from PIL import Image, ImageQt

from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, 
    QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsEllipseItem,
    QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsPathItem
)
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath


class Canvas(QGraphicsView):
    
    class ZoomMode(Enum):
        MANUAL = 0
        FIT_WINDOW = 1

    class StatusMode(Enum):
        CREATE = 0
        EDIT = 1

    class DrawMode(Enum):
        MANUAL = 0
        SAM = 1
    
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        
        self.zoom_mode = Canvas.ZoomMode.FIT_WINDOW
        self.zoom_factor = 1.2
        
        self.setMouseTracking(True)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
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
    
    def zoom_original(self):
        zoom_facor = 1/self.transform().m11()
        self.zoom(zoom_factor=zoom_facor)
    
    def zoom(self, zoom_factor, point=None):
        mouse_old = self.mapToScene(point.toPoint()) if point else None

        # Limit zoom ranges: 0.1 ~ 10
        scaled_width = self.transform().scale(
            zoom_factor, zoom_factor,
        ).mapRect(QRectF(0, 0, 1, 1)).width()
        if scaled_width > 10 or scaled_width < 0.1:
            return

        self.scale(zoom_factor, zoom_factor)
        Object.scale_factor = Object.scale_factor * zoom_factor
        if point is not None:
            mouse_now = self.mapToScene(point.toPoint())
            center_now = self.mapToScene(
                self.viewport().width() // 2, self.viewport().height() // 2,
            )
            center_new = mouse_old - mouse_now + center_now
            self.centerOn(center_new)
    
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
        self.temp_line = None
        self.object = None
        self.objects = []
        self.draw_mode = Canvas.DrawMode.MANUAL
        self.status_mode = Canvas.StatusMode.CREATE
        self.object_type = Object.ObjectType.RECTANGLE
        
    def load_image(self, image_path):
        self.clear()
        self.reset_status()
        # views() returns all views of this scene
        # self.views()
        image_pil = Image.open(image_path)
        image_pixmap = ImageQt.toqpixmap(image_pil)
        self.image_data = np.array(image_pil)
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
        
    def reset_status(self):
        self.guide_line_x = None
        self.guide_line_y = None
        self.temp_line = None
        self.object = None
        self.objects = []
        
    def mousePressEvent(self, event):
        scene_pos = event.scenePos()
        if scene_pos.x() < 0: scene_pos.setX(0)
        if scene_pos.x() > self.width(): scene_pos.setX(self.width())
        if scene_pos.y() < 0: scene_pos.setY(0)
        if scene_pos.y() > self.height(): scene_pos.setY(self.height())
        
        if event.button() == Qt.MouseButton.LeftButton:
            #TODO: Left Click -> Draw Point
            if self.status_mode == Canvas.StatusMode.CREATE:
                #TODO: CREATE mode
                if self.draw_mode == Canvas.DrawMode.MANUAL:
                    point_size = max(3.0, 6.0 / Object.scale_factor)
                    line_width = max(1.0, 2.0 / Object.scale_factor)
                    # line_item = QGraphicsLineItem(0, 0, scene_pos.x(), scene_pos.y())
                    # line_item_pen = QPen(Qt.GlobalColor.green)
                    # line_item_pen.setWidthF(line_width)
                    # line_item.setPen(line_item_pen)
                    # self.addItem(line_item)
                    # rect_item = QGraphicsRectItem(0, 0, scene_pos.x(), scene_pos.y())
                    # rect_item_pen = QPen(Qt.GlobalColor.green)
                    # rect_item_pen.setWidthF(line_width)
                    # rect_item.setPen(rect_item_pen)
                    # self.addItem(rect_item)
                    # ellipse_item = QGraphicsEllipseItem(scene_pos.x()-point_size/2, 
                    #                                     scene_pos.y()-point_size/2, 
                    #                                     point_size, 
                    #                                     point_size)
                    # ellipse_item.setPen(QPen(Qt.GlobalColor.green))
                    # ellipse_item.setBrush(QBrush(Qt.GlobalColor.red))
                    # self.addItem(ellipse_item)
                    path_item = QGraphicsPathItem()
                    path_item_pen = QPen(Qt.GlobalColor.green)
                    path_item_pen.setWidthF(line_width)
                    path_item.setPen(path_item_pen)
                    path_item_brush = QBrush(Qt.GlobalColor.green)
                    path_item.setBrush(path_item_brush)
                    path_item_path = QPainterPath()
                    path_item_path.moveTo(0, 0)
                    path_item_path.lineTo(scene_pos.x(), scene_pos.y())
                    path_item_path.addEllipse(scene_pos.x()-point_size/2, 
                                              scene_pos.y()-point_size/2, 
                                              point_size, 
                                              point_size)
                    path_item.setPath(path_item_path)
                    self.addItem(path_item)
                    pass
                elif self.draw_mode == Canvas.DrawMode.SAM:
                    pass
            elif self.status_mode == Canvas.StatusMode.EDIT:
                #TODO: EDIT mode
                if self.draw_mode == Canvas.DrawMode.MANUAL:
                    pass
                elif self.draw_mode == Canvas.DrawMode.SAM:
                    pass
        elif (event.button() == Qt.MouseButton.RightButton
              and self.status_mode == Canvas.StatusMode.EDIT):
            #TODO: Right Click -> Open Menu
            pass
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        inside_scene = True
        scene_pos = event.scenePos()
        if scene_pos.x() < 0: 
            scene_pos.setX(0)
            inside_scene = False
        if scene_pos.x() > self.width(): 
            scene_pos.setX(self.width())
            inside_scene = False
        if scene_pos.y() < 0: 
            scene_pos.setY(0)
            inside_scene = False
        if scene_pos.y() > self.height(): 
            scene_pos.setY(self.height())
            inside_scene = False

        # Cross shows only inside scene
        # start = time.perf_counter()
        if self.status_mode == Canvas.StatusMode.CREATE and inside_scene:
            QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
        else:
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)

        if self.object_type == Object.ObjectType.RECTANGLE:
            if self.guide_line_x is None:
                self.guide_line_x = GuideLine(0, scene_pos.y(), self.width(), scene_pos.y())
                self.addItem(self.guide_line_x)
            else:
                self.guide_line_x.setLine(0, scene_pos.y(), self.width(), scene_pos.y())
            if self.guide_line_y is None:
                self.guide_line_y = GuideLine(scene_pos.x(), 0, scene_pos.x(), self.height())
                self.addItem(self.guide_line_y)
            else:
                self.guide_line_y.setLine(scene_pos.x(), 0, scene_pos.x(), self.height())
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
                int(scene_pos.x()),
                int(scene_pos.y()),
            ))

        return super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        key = event.key()