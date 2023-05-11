# -*- coding: utf-8 -*-
# J094
# 2023.05.10

from enum import Enum

from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QColor, QPixmap, QPainter


class Prompt(QGraphicsPixmapItem):
    
    DEFAULT_MASK_COLOR = QColor(30, 144, 255, 128)
    DEFAULT_SELECT_MASK_COLOR = QColor(30, 144, 255, 155)
    
    def __init__(self, parent=None):
        super(Prompt, self).__init__(parent)
        
        self.shapes = []
        self.prompt_pixmap = None
        
    def update_pixmap(self):
        # shape_pixmap = QPixmap()
        # painter = QPainter()
        # painter.begin(shape_pixmap)
        # painter.end()
        # self.setPixmap(shape_pixmap)
        pass