# -*- coding: utf-8 -*-
# J094
# 2023.05.10
import os
import sys

import PySide6.QtGui
sys.path.append(os.path.realpath("."))

from src.widgets.objects.shape import Shape
from src.widgets.objects.prompt import Prompt

import math
import numpy as np
from enum import Enum
from PIL import Image, ImageQt

from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem,
    QApplication,
)
from PySide6.QtGui import QPainter


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
        
    def reset_status(self):
        pass
        
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
            # Do not effect scrollbar
            return super().wheelEvent(event)


class CanvasScene(QGraphicsScene):
    def __init__(self, parent=None, main_window=None):
        super(CanvasScene, self).__init__(parent)
        self.main_window = main_window

        self.scene_rect = None
        self.image_data = None
        self.shape_item = None
        self.shape_items = []
        self.prompt_item = None
        self.prompt_items = []
        self.tmp_shape_item = None
        self.guide_line_x = None
        self.guide_line_y = None
        self.draw_mode = Canvas.DrawMode.MANUAL
        self.status_mode = Canvas.StatusMode.CREATE
        self.shape_type = Shape.ShapeType.RECTANGLE
        # Snap last point with first point when draw POLYGON
        self.snapping = True
        # Snap threshold is 5 pixels
        self.close_eplison = 5
        
    def load_image(self, image_path):
        self.clear()
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
        
    def reset_shape_item(self):
        if self.shape_item in self.items():
            self.shape_item.highlight_clear()
            self.shape_item.update_pixmap()
            self.removeItem(self.shape_item)
        if self.tmp_shape_item in self.items():
            self.shape_item.highlight_clear()
            self.shape_item.update_pixmap()
            self.removeItem(self.tmp_shape_item)
        self.shape_item = None
        self.tmp_shape_item = None
        
    def can_close_shape(self):
        if (self.status_mode == Canvas.StatusMode.CREATE
            and self.shape_item is not None
            and len(self.shape_item.points) >= 3):
            # At least 3 points
            return True
        else:
            return False
        
    def close_enough(self, point_1, point_2):
        point_delta = point_1 - point_2
        distance = math.sqrt(
            point_delta.x() * point_delta.x() + point_delta.y() * point_delta.y()
        )
        return distance < self.close_eplison
        
    def finish_draw_manual(self):
        self.shape_items.append(self.shape_item)
        self.reset_shape_item()
        pass
    
    def finish_draw_sam(self):
        pass
    
    def update(self):
        #TODO: Add items here
        # Saved shape items
        for shape_item in self.shape_items:
            if (shape_item is not None
                and shape_item not in self.items()):
                self.addItem(shape_item)
        # Current shape item
        if (self.shape_item is not None
            and self.shape_item not in self.items()):
            self.addItem(self.shape_item)
        # Current temperary shape item
        if (self.tmp_shape_item is not None
            and self.tmp_shape_item not in self.items()):
            self.addItem(self.tmp_shape_item)
        
        super().update()
        
    def mousePressEvent(self, event):
        scene_pos = event.scenePos()
        if scene_pos.x() < 0: scene_pos.setX(0)
        if scene_pos.x() > self.width(): scene_pos.setX(self.width())
        if scene_pos.y() < 0: scene_pos.setY(0)
        if scene_pos.y() > self.height(): scene_pos.setY(self.height())
        
        if event.button() == Qt.MouseButton.LeftButton:
            if self.status_mode == Canvas.StatusMode.CREATE:
                if self.draw_mode == Canvas.DrawMode.MANUAL:
                    if self.shape_item is None:
                        # Create a new shape
                        self.shape_item = Shape(scene_rect=self.scene_rect, 
                                                shape_type=self.shape_type)
                        self.shape_item.add_point(point=scene_pos)
                        self.shape_item.update_pixmap()
                        self.tmp_shape_item = Shape(scene_rect=self.scene_rect, 
                                              shape_type=self.shape_type)
                        self.tmp_shape_item.add_point(point=scene_pos)
                        self.tmp_shape_item.add_point(point=scene_pos)
                        self.tmp_shape_item.update_pixmap()
                        if (self.shape_type == Shape.ShapeType.POINTS
                            and event.modifiers() == Qt.KeyboardModifier.ControlModifier):
                            self.finish_draw_manual()
                        self.update()
                    else:
                        # Add points to shape item
                        if self.shape_type == Shape.ShapeType.POINTS:
                            self.shape_item.add_point(self.tmp_shape_item.points[1])
                            self.shape_item.update_pixmap()
                            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                                self.finish_draw_manual()
                        elif self.shape_type == Shape.ShapeType.RECTANGLE:
                            assert len(self.shape_item.points) == 1
                            self.shape_item.add_point(self.tmp_shape_item.points[1])
                            self.shape_item.update_pixmap()
                            self.finish_draw_manual()
                        elif self.shape_type == Shape.ShapeType.POLYGON:
                            self.shape_item.add_point(self.tmp_shape_item.points[1])
                            self.shape_item.update_pixmap()
                            self.tmp_shape_item.points[0] = self.shape_item.points[-1]
                            self.tmp_shape_item.update_pixmap()
                            if self.shape_item.closed:
                                self.shape_item.points.pop()
                                self.finish_draw_manual()
                        elif self.shape_type == Shape.ShapeType.LINES:
                            self.shape_item.add_point(self.tmp_shape_item.points[1])
                            self.shape_item.update_pixmap()
                            self.tmp_shape_item.points[0] = self.shape_item.points[-1]
                            self.tmp_shape_item.update_pixmap()
                            if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                                self.finish_draw_manual()
                        self.update()
                elif self.draw_mode == Canvas.DrawMode.SAM:
                    #TODO: SAM mode
                    if self.shape_item is None:
                        # Create a new shape
                        pass
                    else:
                        # Add points to shape item
                        pass
            elif self.status_mode == Canvas.StatusMode.EDIT:
                #TODO: EDIT mode
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
        if self.status_mode == Canvas.StatusMode.CREATE and inside_scene:
            QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
        else:
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)

        if self.guide_line_x is not None and self.guide_line_x in self.items():
            self.removeItem(self.guide_line_x)
            self.guide_line_x = None
        if self.guide_line_y is not None and self.guide_line_y in self.items():
            self.removeItem(self.guide_line_y)
            self.guide_line_y = None
        if self.shape_type == Shape.ShapeType.RECTANGLE:
            self.guide_line_x = QGraphicsLineItem(0, scene_pos.y(), self.width(), scene_pos.y())
            self.guide_line_x.setZValue(1)
            self.addItem(self.guide_line_x)
            self.guide_line_y = QGraphicsLineItem(scene_pos.x(), 0, scene_pos.x(), self.height())
            self.guide_line_y.setZValue(1)
            self.addItem(self.guide_line_y)
        
        if self.image_data is not None:
            self.main_window.statusBar().showMessage("Current Pose: ({}, {})".format(
                int(scene_pos.x()),
                int(scene_pos.y()),
            ))
            
        if (self.shape_item is not None and self.tmp_shape_item is not None):
            if (self.snapping
                and self.shape_type == Shape.ShapeType.POLYGON
                and self.can_close_shape()
                and self.close_enough(scene_pos, self.shape_item.points[0])):
                scene_pos = self.shape_item.points[0]
                self.shape_item.highlight_vertex(0, Shape.HightlightMode.NEAR_VERTEX)
                self.tmp_shape_item.highlight_vertex(1, Shape.HightlightMode.NEAR_VERTEX)
            else:
                self.shape_item.highlight_clear()
                self.tmp_shape_item.highlight_clear()
            
            if self.shape_type == Shape.ShapeType.POINTS:
                self.tmp_shape_item.points[0] = scene_pos
                self.tmp_shape_item.points[1] = scene_pos
            else:
                # RECTANGLE, POLYGON, LINES
                self.tmp_shape_item.points[0] = self.shape_item.points[-1]
                self.tmp_shape_item.points[1] = scene_pos
            self.shape_item.update_pixmap()
            self.tmp_shape_item.update_pixmap()

        self.update()
        return super().mouseMoveEvent(event)

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        key = event.key()
        if self.status_mode == Canvas.StatusMode.CREATE:
            if (key == Qt.Key.Key_Escape 
                and self.shape_item is not None
                and self.tmp_shape_item is not None):
                self.reset_shape_item()
                self.update()
        pass