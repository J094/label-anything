# -*- coding: utf-8 -*-
# J094
# 2023.05.15
import os
import sys
sys.path.append(os.path.realpath("."))

from src.widgets.objects.draw_object import DrawObject

from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem
from PySide6.QtGui import QColor, QPen, QBrush


class DrawRectangle(DrawObject):
    def __init__(self, canvas_scene=None):
        super(DrawRectangle, self).__init__(canvas_scene)
        self.draw_object_type = DrawObject.DrawObjectType.RECTANGLE
        self.points = [None, None]
        # QGraphicsEllipseItem or QGraphicsRectItem
        self.point_items = [None, None]
        # QGraphicsRectItem
        self.rect_item = None
        self.line_color = DrawObject.default_line_color
        self.point_color = DrawObject.default_point_color
        
    def add_point(self, point):
        self.update_point_size()
        self.update_line_width()
        point_item = QGraphicsEllipseItem()
        self.canvas_scene.addItem(point_item)
        if self.points[0] is None:
            self.points = [point, point]
            self.point_items = [point_item, point_item]
            rect_item = QGraphicsRectItem()
            self.canvas_scene.addItem(rect_item)
            self.rect_item = rect_item
        else:
            self.closed = True
            self.points[1] = point
            self.point_items[1] = point_item
            
    def get_rect(self, point_1, point_2):
        x_1, y_1 = point_1.x(), point_1.y()
        x_2, y_2 = point_2.x(), point_2.y()
        return QRectF(x_1, y_1, x_2 - x_1, y_2 - y_1)
    
    def update_items(self):
        self.update_point_size()
        self.update_line_width()
        point_pen = QPen(self.line_color)
        point_brush = QBrush(self.point_color)
        for (i, point) in enumerate(self.points):
            self.point_items[i].setRect(point.x()-self.point_size/2,
                                        point.y()-self.point_size/2,
                                        self.point_size,
                                        self.point_size)
            point_pen.setWidthF(self.line_width)
            self.point_items[i].setPen(point_pen)
            self.point_items[i].setBrush(point_brush)
        rect_pen = QPen(self.line_color)
        self.rect_item.setRect(self.get_rect(
            self.points[0],
            self.points[1],
        ))
        self.rect_item.setPen(rect_pen)