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
    
    def __init__(self, parent):
        super(Shape, self).__init__(parent)
        
        self.points = []
        self.shape_type = None
        self.point_type = None
        
    def update_pixmap(self):
        shape_pixmap = QPixmap()
        painter = QPainter()
        painter.begin(shape_pixmap)
        painter.end()
        self.setPixmap(shape_pixmap)