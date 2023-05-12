# -*- coding: utf-8 -*-
# J094
# 2023.05.12
import os
import sys
sys.path.append(os.path.realpath("."))

from PySide6.QtWidgets import QGraphicsLineItem


class GuideLine(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super(GuideLine, self).__init__(x1, y1, x2, y2)
        self.setZValue(1)