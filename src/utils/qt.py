# -*- coding: utf-8 -*-
# J094
# 2023.05.16
import os
import sys
sys.path.append(os.path.realpath("."))

import math

from PySide6.QtCore import QPointF


def distance_points(point_1, point_2):
    point_delta = point_1 - point_2
    return math.sqrt(point_delta.x()**2 + point_delta.y()**2)


if __name__ == "__main__":
    distance = distance_points(QPointF(0, 0), QPointF(2, 2))
    print(distance)