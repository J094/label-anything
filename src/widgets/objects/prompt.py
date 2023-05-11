# -*- coding: utf-8 -*-
# J094
# 2023.05.10

from enum import Enum

from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtGui import QColor, QPixmap, QPainter


class Prompt(QGraphicsPixmapItem):
    
    DEFAULT_MASK_COLOR = QColor(30, 144, 255, 128)
    DEFAULT_SELECT_MASK_COLOR = QColor(30, 144, 255, 155)
    
    def __init__(self, parent=None, scene_rect=None):
        super(Prompt, self).__init__(parent)
        
        self.scene_rect = scene_rect
        self.shapes = []
        
    def update_pixmap(self):
        prompt_pixmap = QPixmap(self.scene_rect.width(), self.scene_rect.height())
        prompt_pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter()
        painter.begin(prompt_pixmap)
        painter.end()
        self.setPixmap(prompt_pixmap)