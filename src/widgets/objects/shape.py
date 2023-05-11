# -*- coding: utf-8 -*-
# J094
# 2023.05.10

from enum import Enum

from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QColor, QPixmap, QPainter


class Shape(QGraphicsPixmapItem):
    
    class ShapeType(Enum):
        POINTS = 0
        RECTANGLE = 1
        POLYGON = 2
        LINES = 3
        
    class PointType(Enum):
        ROUND = 0
        SQUARE = 1
        
    DEFAULT_LINE_COLOR = QColor(0, 255, 0, 128)
    DEFAULT_FILL_COLOR = QColor(0, 255, 0, 128)
    DEFAULT_SELECT_LINE_COLOR = QColor(255, 255, 255)
    DEFAULT_SELECT_FILL_COLOR = QColor(0, 255, 0, 155)
    DEFAULT_VERTEX_FILL_COLOR = QColor(0, 255, 0, 255)
    DEFAULT_HVERTEX_FILL_COLOR = QColor(255, 255, 255, 255)
    
    def __init__(self, parent=None, scene_rect=None, shape_type=None, is_tmp=False):
        super(Shape, self).__init__(parent)

        self.scene_rect = scene_rect
        self.shape_type = shape_type
        self.is_tmp = is_tmp
        self.points = []
        self.points_flag = []
        self.point_type = None
        self.closed = False
        
    def add_point(self, point, point_flag=True):
        self.points.append(point)
        self.points_flag.append(point_flag)
    
    def update_pixmap(self):
        shape_pixmap = QPixmap(self.scene_rect.width(), self.scene_rect.height())
        shape_pixmap.fill(QColor(255, 0, 0, 125))
        painter = QPainter()
        painter.begin(shape_pixmap)
        painter.end()
        self.setPixmap(shape_pixmap)