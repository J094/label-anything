# -*- coding: utf-8 -*-
# J094
# 2023.05.12
import os
import sys
sys.path.append(os.path.realpath("."))

from enum import Enum

from PySide6.QtGui import QColor


class DrawObject(object):
    
    # 4 types to draw
    class DrawObjectType(Enum):
        POINTS = 0
        RECTANGLE = 1
        POLYGON = 2
        LINES = 3
    
    default_line_color = QColor(0, 255, 0, 128)
    default_fill_color = QColor(0, 255, 0, 128)
    default_point_color = QColor(0, 255, 0, 255)
    default_selected_line_color = QColor(255, 255, 255, 255)
    default_selected_fill_color = QColor(0, 255, 0, 155)
    default_selected_point_color = QColor(255, 255, 255, 255)
    default_point_size_base = 8.0
    default_line_width_base = 2.0
    scale_factor = 1.0
    
    def __init__(self, canvas_scene=None):
        self.canvas_scene = canvas_scene

        self.label_name = None
        self.group_id = None
        self.draw_object_type = None
        self.point_size_base = DrawObject.default_point_size_base
        self.point_size = None
        self.line_width_base = DrawObject.default_line_width_base
        self.line_width = None
        self.closed = False
    
    def add_point(self, point):
        pass
    
    def update_items(self):
        pass
    
    def update_point_size(self):
        self.point_size = max(3.0, self.point_size_base / DrawObject.scale_factor)
        # print("point size:", self.point_size)

    def update_line_width(self):
        self.line_width = max(1.0, self.line_width_base / DrawObject.scale_factor)
        # print("line width", self.line_width)