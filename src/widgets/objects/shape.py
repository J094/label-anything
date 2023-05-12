# -*- coding: utf-8 -*-
# J094
# 2023.05.10

from enum import Enum

from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import (
    QColor, QPixmap, QPainter, QPen, QBrush, QPainterPath
)


DEFAULT_LINE_COLOR = QColor(0, 255, 0, 128)
DEFAULT_FILL_COLOR = QColor(0, 255, 0, 128)
DEFAULT_SELECT_LINE_COLOR = QColor(255, 255, 255)
DEFAULT_SELECT_FILL_COLOR = QColor(0, 255, 0, 155)
DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 255)
DEFAULT_HVERTEX_FILL_COLOR = QColor(255, 255, 255, 255)

class Shape(QGraphicsPixmapItem):
    
    class ShapeType(Enum):
        POINTS = 0
        RECTANGLE = 1
        POLYGON = 2
        LINES = 3
        
    class PointType(Enum):
        ROUND = 0
        SQUARE = 1
        
    class HightlightMode(Enum):
        NEAR_VERTEX = 0
        MOVE_VERTEX = 1

    line_color = DEFAULT_LINE_COLOR
    fill_color = DEFAULT_FILL_COLOR
    select_line_color = DEFAULT_SELECT_LINE_COLOR
    select_fill_color = DEFAULT_SELECT_FILL_COLOR
    vertex_fill_color = DEFAULT_VERTEX_FILL_COLOR
    hvertex_fill_color = DEFAULT_HVERTEX_FILL_COLOR
        
    def __init__(self, parent=None, scene_rect=None, shape_type=None):
        super(Shape, self).__init__(parent)

        self.scene_rect = scene_rect
        self.shape_type = shape_type
        self.points = []
        self.points_flag = []
        self.point_type = Shape.PointType.ROUND
        self.point_size = 4
        self.vertex_color = None
        self.highlight_index = None
        self.highlight_mode = None
        self.highlight_settings = {
            Shape.HightlightMode.NEAR_VERTEX: (2, Shape.PointType.ROUND),
            Shape.HightlightMode.MOVE_VERTEX: (1.5, Shape.PointType.SQUARE),
        }
        self.fill_shape = False
        self.selected = False
        self.closed = False
        
    def add_point(self, point, point_flag=True):
        # At least 3 points
        if len(self.points) >= 3 and point == self.points[0]:
            self.closed = True
        self.points.append(point)
        self.points_flag.append(point_flag)
        
    def highlight_clear(self):
        self.highlight_index = None
        self.highlight_mode = None
        
    def highlight_vertex(self, i, mode):
        self.highlight_index = i
        self.highlight_mode = mode
        
    def get_rect_from_points(self, point_1, point_2):
        x_1, y_1 = point_1.x(), point_1.y()
        x_2, y_2 = point_2.x(), point_2.y()
        return QRectF(x_1, y_1, x_2 - x_1, y_2 - y_1)
        
    def draw_vertex(self, path, i):
        d = self.point_size
        shape = self.point_type
        point = self.points[i]
        if self.highlight_index == i:
            size, shape = self.highlight_settings[self.highlight_mode]
            d *= size
        if self.highlight_index is not None:
            self.vertex_color = self.hvertex_fill_color
        else:
            self.vertex_color = self.vertex_fill_color
        # Negative points are red
        if not self.points_flag[i]:
            self.vertex_color = Qt.GlobalColor.red
        if shape == Shape.PointType.ROUND:
            path.addEllipse(point, d / 2.0, d / 2.0)
        elif shape == Shape.PointType.SQUARE:
            path.addRect(point.x() - d / 2.0, point.y() - d / 2.0, d, d)
    
    def update_pixmap(self):
        shape_pixmap = QPixmap(self.scene_rect.width(), self.scene_rect.height())
        shape_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter()
        painter.begin(shape_pixmap)
        
        # Paint in pixmap
        if len(self.points) > 0:
            color = self.select_line_color if self.selected else self.line_color
            pen = QPen(color)
            pen.setWidth(max(1, int(round(2.0))))
            painter.setPen(pen)
            
            line_path = QPainterPath()
            vertex_path = QPainterPath()
            
            if self.shape_type == Shape.ShapeType.POINTS:
                for i, p in enumerate(self.points):
                    self.draw_vertex(vertex_path, i)
            elif self.shape_type == Shape.ShapeType.RECTANGLE:
                assert len(self.points) in [1, 2]
                if len(self.points) == 2:
                    rectangle = self.get_rect_from_points(*self.points)
                    line_path.addRect(rectangle)
                for i in range(len(self.points)):
                    self.draw_vertex(vertex_path, i)
            elif self.shape_type == Shape.ShapeType.POLYGON:
                line_path.moveTo(self.points[0])
                for i, p in enumerate(self.points):
                    line_path.lineTo(p)
                    self.draw_vertex(vertex_path, i)
                if self.closed:
                    line_path.lineTo(self.points[0])
            elif self.shape_type == Shape.ShapeType.LINES:
                line_path.moveTo(self.points[0])
                for i, p in enumerate(self.points):
                    line_path.lineTo(p)
                    self.draw_vertex(vertex_path, i)

            painter.drawPath(line_path)
            painter.drawPath(vertex_path)
            painter.fillPath(vertex_path, self.vertex_color)
            
            if self.fill_shape:
                color = self.select_fill_color if self.selected else self.fill_color
                painter.fillPath(line_path, color)
        
        painter.end()
        self.setPixmap(shape_pixmap)