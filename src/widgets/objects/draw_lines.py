# -*- coding: utf-8 -*-
# J094
# 2023.05.16
import os
import sys
sys.path.append(os.path.realpath("."))

from src.widgets.objects.draw_object import DrawObject

from PySide6.QtCore import QLineF
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPolygonItem
from PySide6.QtGui import QColor, QPen, QBrush


class DrawLines(DrawObject):
    def __init__(self, canvas_scene=None):
        super(DrawLines, self).__init__(canvas_scene)
        self.draw_object_type = DrawObject.DrawObjectType.LINES
        self.points = []
        # Only used in drawing item
        self.last_point = None
        # QGraphicsEllipseItem or QGraphicsRectItem
        self.point_items = []
        # QGraphicsEllipseItem
        # Only used in drawing item
        self.last_point_item = None
        # QGraphicsLineItem
        # Only used in drawing item
        self.line_items = []
        # Only used in drawing item
        self.last_line_item = None
        self.line_color = DrawObject.default_line_color
        self.point_color = DrawObject.default_point_color
        
    def add_point(self, point):
        point_item = QGraphicsEllipseItem()
        self.canvas_scene.addItem(point_item)
        self.points.append(point)
        self.point_items.append(point_item)
        if len(self.points) >= 2:
            line_item = QGraphicsLineItem()
            self.canvas_scene.addItem(line_item)
            self.line_items.append(line_item)
        if self.last_point_item is None:
            last_point_item = QGraphicsEllipseItem()
            self.canvas_scene.addItem(last_point_item)
            self.last_point = point
            self.last_point_item = last_point_item
        if self.last_line_item is None:
            last_line_item = QGraphicsLineItem()
            self.canvas_scene.addItem(last_line_item)
            self.last_line_item = last_line_item
    
    def update_items(self):
        self.update_point_size()
        self.update_line_width()
        point_pen = QPen(self.line_color)
        point_pen.setWidthF(self.line_width)
        point_brush = QBrush(self.point_color)
        for (i, point) in enumerate(self.points):
            self.point_items[i].setRect(point.x()-self.point_size/2,
                                        point.y()-self.point_size/2,
                                        self.point_size,
                                        self.point_size)
            self.point_items[i].setPen(point_pen)
            self.point_items[i].setBrush(point_brush)
        line_pen = QPen(self.line_color)
        line_pen.setWidthF(self.line_width)
        for i in range(len(self.points) - 1):
            point_1 = self.points[i]
            point_2 = self.points[i + 1]
            self.line_items[i].setLine(point_1.x(), point_1.y(),
                                    point_2.x(), point_2.y())
            self.line_items[i].setPen(line_pen)
        if self.closed:
            self.canvas_scene.removeItem(self.last_point_item)
            self.last_point_item = None
            self.canvas_scene.removeItem(self.last_line_item)
            self.last_line_item = None
        else:
            self.last_point_item.setRect(self.last_point.x()-self.point_size/2,
                                        self.last_point.y()-self.point_size/2,
                                        self.point_size,
                                        self.point_size)
            self.last_point_item.setPen(point_pen)
            self.last_point_item.setBrush(point_brush)
            last_point_1 = self.points[-1]
            last_point_2 = self.last_point
            self.last_line_item.setLine(last_point_1.x(), last_point_1.y(),
                                        last_point_2.x(), last_point_2.y())
            self.last_line_item.setPen(line_pen)