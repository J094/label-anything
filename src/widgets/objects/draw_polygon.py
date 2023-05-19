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


class DrawPolygon(DrawObject):
    def __init__(self, canvas_scene=None):
        super(DrawPolygon, self).__init__(canvas_scene)
        self.draw_object_type = DrawObject.DrawObjectType.POLYGON
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
        self.polygon_item = None
        self.line_color = DrawObject.default_line_color
        self.point_color = DrawObject.default_point_color
        self.fill_color = DrawObject.default_fill_color
        
    def add_point(self, point):
        # Close this polygon
        if (len(self.points) >= 3
            and point.x() == self.points[0].x()
            and point.y() == self.points[0].y()):
            self.close()
            return
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
        if self.closed:
            if self.polygon_item is None:
                self.polygon_item = QGraphicsPolygonItem()
                self.canvas_scene.addItem(self.polygon_item)
            polygon_pen = QPen(self.line_color)
            polygon_pen.setWidthF(self.line_width)
            polygon_brush = QBrush(self.fill_color)
            self.polygon_item.setPolygon(self.points)
            self.polygon_item.setPen(polygon_pen)
            self.polygon_item.setBrush(polygon_brush)
            for line_item in self.line_items:
                if line_item in self.canvas_scene.items():
                    self.canvas_scene.removeItem(line_item)
            if self.last_point_item in self.canvas_scene.items():
                self.canvas_scene.removeItem(self.last_point_item)
            if self.last_line_item in self.canvas_scene.items():
                self.canvas_scene.removeItem(self.last_line_item)
        else:
            line_pen = QPen(self.line_color)
            line_pen.setWidthF(self.line_width)
            for i in range(len(self.points) - 1):
                point_1 = self.points[i]
                point_2 = self.points[i + 1]
                self.line_items[i].setLine(point_1.x(), point_1.y(),
                                        point_2.x(), point_2.y())
                self.line_items[i].setPen(line_pen)
            self.last_point_item.setRect(self.last_point.x()-self.point_size/2,
                                        self.last_point.y()-self.point_size/2,
                                        self.point_size,
                                        self.point_size)
            self.last_point_item.setPen(point_pen)
            self.last_point_item.setBrush(point_brush)
            last_point_1 = self.points[-1]
            last_point_2 = self.last_point
            if (last_point_1.x() == last_point_2.x()
                and last_point_1.y() == last_point_2.y()):
                self.last_line_item.setVisible(False)
            else:
                self.last_line_item.setLine(last_point_1.x(), last_point_1.y(),
                                            last_point_2.x(), last_point_2.y())
                self.last_line_item.setVisible(True)
            self.last_line_item.setPen(line_pen)
            
    def unclose(self):
        for line_item in self.line_items:
            self.canvas_scene.addItem(line_item)
        self.canvas_scene.addItem(self.last_point_item)
        self.canvas_scene.addItem(self.last_line_item)
        self.canvas_scene.removeItem(self.polygon_item)
        self.polygon_item = None
        return super().unclose()
        
    def clear(self):
        for point_item in self.point_items:
            if point_item in self.canvas_scene.items():
                self.canvas_scene.removeItem(point_item)
        for line_item in self.line_items:
            if line_item in self.canvas_scene.items():
                self.canvas_scene.removeItem(line_item)
        if self.last_point_item in self.canvas_scene.items():
            self.canvas_scene.removeItem(self.last_point_item)
        if self.last_line_item in self.canvas_scene.items():
            self.canvas_scene.removeItem(self.last_line_item)