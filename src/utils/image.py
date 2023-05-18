# -*- coding: utf-8 -*-
# J094
# 2023.05.18
import os
import sys
sys.path.append(os.path.realpath("."))

import io
from PIL import Image


def load_image_data(image_path):
    try:
        image_pil = Image.open(image_path)
    except IOError:
        print(f"ERROR: Failed openning image file: {image_path}")
        return None
    
    with io.BytesIO() as f:
        ext = os.path.splitext(image_path)[1].lower()
        if ext == ".png":
            format = "PNG"
        elif ext in [".jpg", ".jpeg"]:
            format = "JPEG"
        else:
            print(f"ERROR: Unsupported image format: {ext}")
            return None
        image_pil.save(f, format=format)
        f.seek(0)
        return f.read()