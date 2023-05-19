# -*- coding: utf-8 -*-
# J094
# 2023.05.15
import os
import sys
sys.path.append(os.path.realpath("."))

from src.widgets.objects.draw_object import DrawObject

from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QColor, QPen, QBrush


class DrawPoints(DrawObject):
    def __init__(self, canvas_scene=None):
        super(DrawPoints, self).__init__(canvas_scene)
        self.draw_object_type = DrawObject.DrawObjectType.POINTS
        self.points = []
        # QGraphicsEllipseItem or QGraphicsRectItem
        self.point_items = []
        self.line_color = DrawObject.default_line_color
        self.point_color = DrawObject.default_point_color
        
    def add_point(self, point):
        point_item = QGraphicsEllipseItem()
        self.canvas_scene.addItem(point_item)
        self.points.append(point)
        self.point_items.append(point_item)
    
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
    
    def unclose(self):
        self.points.pop()
        self.point_items.pop()
        return super().unclose()
    
    def clear(self):
        for point_item in self.point_items:
            if point_item in self.canvas_scene.items():
                self.canvas_scene.removeItem(point_item)