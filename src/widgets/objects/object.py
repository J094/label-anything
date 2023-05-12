# -*- coding: utf-8 -*-
# J094
# 2023.05.12
import os
import sys
sys.path.append(os.path.realpath("."))

from enum import Enum

from PySide6.QtGui import QColor


class Object(object):
    
    # 4 types to draw
    class ObjectType(Enum):
        POINTS = 0
        RECTANGLE = 1
        POLYGON = 2
        LINES = 3
        
    class PointType(Enum):
        ROUND = 0
        SQUARE = 1
    
    default_line_color = QColor(0, 255, 0, 128)
    default_fill_color = QColor(0, 255, 0, 128)
    default_select_line_color = QColor(255, 255, 255)
    default_select_fill_color = QColor(0, 255, 0, 155)
    default_point_fill_color = QColor(0, 255, 0, 255)
    default_hpoint_fill_color = QColor(255, 255, 255, 255)
    scale_factor = 1.0
    
    def __init__(self):
        # QGraphicsPointItem
        self.points = []