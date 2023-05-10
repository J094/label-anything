# -*- coding: utf-8 -*-
# J094
# 2023.05.10
import os
import sys

import PySide6.QtGui
sys.path.append(os.path.realpath("."))

from src.widgets.objects.shape import Shape
from src.widgets.objects.prompt import Prompt

import numpy as np
from enum import Enum
from PIL import Image, ImageQt

from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
)


class Canvas(QGraphicsView):
    
    class ZoomMode(Enum):
        MANUAL = 0
        FIT_WINDOW = 1

    class StatusMode(Enum):
        CREATE = 0
        EDIT = 1

    class DrawMode(Enum):
        MANUAL = 0
        SAM = 1
    
    def __init__(self, parent=None):
        super(Canvas, self).__init__(parent)
        
        self.zoom_mode = Canvas.ZoomMode.FIT_WINDOW
        self.factor = 1.2
        
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
    def reset_status(self):
        pass
        
    def zoom_in(self):
        self.zoom(self.factor)
    
    def zoom_out(self):
        self.zoom(1/self.factor)
    
    def zoom_fit_window(self):
        self.fitInView(0, 0, self.scene().width(), self.scene().height(), 
                       Qt.AspectRatioMode.KeepAspectRatio)
    
    def zoom(self, factor, point=None):
        mouse_old = self.mapToScene(point) if point is not None else None

        pix_widget = self.transform().scale(factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if pix_widget > 3 or pix_widget < 0.01:
            return

        self.scale(factor, factor)
        if point is not None:
            mouse_now = self.mapToScene(point)
            center_now = self.mapToScene(self.viewport().width() // 2, self.viewport().height() // 2)
            center_new = mouse_old - mouse_now + center_now
            self.centerOn(center_new)
    
    def paintEvent(self, event):
        if self.zoom_mode == Canvas.ZoomMode.FIT_WINDOW:
            self.zoom_fit_window()
        return super().paintEvent(event)

        

class CanvasScene(QGraphicsScene):
    def __init__(self, parent=None, main_window=None):
        super(CanvasScene, self).__init__(parent)
        self.main_window = main_window

        self.image_pil = None
        self.image_pixmap = None
        self.shape_item = None
        self.shape_items = []
        self.prompt_item = None
        self.prompt_items = []
        self.status_mode = None
        
    def load_image(self, image_path):
        self.clear()
        
        self.image_pil = Image.open(image_path)
        self.image_pixmap = ImageQt.toqpixmap(self.image_pil)
        
        self.image_item = QGraphicsPixmapItem()
        self.image_item.setZValue(0)
        self.image_item.setPixmap(self.image_pixmap)
        
        self.addItem(self.image_item)