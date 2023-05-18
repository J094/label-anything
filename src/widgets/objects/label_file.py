# -*- coding: utf-8 -*-
# J094
# 2023.05.18
import os
import sys
sys.path.append(os.path.realpath("."))

import src.utils.image as utils_image

import json
import base64


class LabelFile(object):
    def __init__(self, file_path=None):
        self.objects = []
        self.image_path = None
        self.image_data = None
        self.image_size = None
        if (file_path is not None
            and os.path.exists(file_path)):
            self.load(file_path)
        self.file_path = file_path
        
    def load(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        self.objects = [
            {
                "label_name": object["label_name"],
                "group_id": object["group_id"],
                "object_type": object["object_type"],
                "points": object["points"],
            }
            for object in data["objects"]
        ]
        self.image_path = data["image_path"]
        if data["image_data"] is not None:
            self.image_data = base64.b64decode(data["image_data"])
        else:
            self.image_data = utils_image.load_image_data(
                os.path.join(os.path.dirname(file_path), self.image_path),
            )
        self.image_size = data["image_size"]
            
    def save(self):
        image_b64 = base64.b64encode(self.image_data).decode("utf-8")
        data = {
            "objects": self.objects,
            "image_path": self.image_path,
            "image_size": self.image_size,
            "image_data": image_b64,
        }
        with open(self.file_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
            
        