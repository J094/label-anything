# -*- coding: utf-8 -*-
# J094
# 2023.05.12
import os
import sys
sys.path.append(os.path.realpath("."))

from src.widgets.objects.prompt_object import PromptObject


class PromptSAM(PromptObject):
    def __init__(self, canvas_scene=None):
        super(PromptSAM, self).__init__(canvas_scene)
        self.draw_points = []
        self.draw_rects = []