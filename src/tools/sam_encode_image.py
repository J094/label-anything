# -*- coding: utf-8 -*-
# J094
# 2023.05.19
import os
import sys
sys.path.append(os.path.realpath("."))

import os
import argparse
import cv2
import torch
import time
import numpy as np

from segment_anything import sam_model_registry
from src.sam.predictor_custom import SamPredictorCustom


parser = argparse.ArgumentParser(
    description=(
        "Runs automatic mask generation on an input image or directory of images, "
        "and outputs masks as either PNGs or COCO-style RLEs. Requires open-cv, "
        "as well as pycocotools if saving in RLE format."
    )
)

parser.add_argument(
    "--input",
    type=str,
    default="data/image/exp.jpg",
    # required=True,
    help="Path to either a single input image or folder of images.",
)

parser.add_argument(
    "--output",
    type=str,
    default="data/embedding/",
    # required=True,
    help=(
        "Path to the directory where image embeddings will be output."
    ),
)

parser.add_argument(
    "--model-type",
    type=str,
    default="vit_h",
    # required=True,
    help="The type of model to load, in ['default', 'vit_h', 'vit_l', 'vit_b']",
)

parser.add_argument(
    "--checkpoint",
    type=str,
    default="ckpt/vit_h_image_encoder.pth",
    # required=True,
    help="The path to the SAM checkpoint to use for image encoding.",
)

parser.add_argument("--device", type=str, default="cuda", help="The device to run generation on.")

def main(args: argparse.Namespace) -> None:
    print("Loading model...")
    sam = sam_model_registry[args.model_type]()
    with open(args.checkpoint, "rb") as f:
        state_dict = torch.load(f)
    sam.image_encoder.load_state_dict(state_dict)
    _ = sam.to(device=args.device)
    
    predictor = SamPredictorCustom(sam)
    
    if not os.path.isdir(args.input):
        targets = [args.input]
    else:
        targets = [
            f for f in os.listdir(args.input) if not os.path.isdir(os.path.join(args.input, f))
        ]
        targets = [os.path.join(args.input, f) for f in targets]

    os.makedirs(args.output, exist_ok=True)

    for t in targets:
        print(f"Processing '{t}'...")
        image = cv2.imread(t)
        if image is None:
            print(f"Could not load '{t}' as an image, skipping...")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        start_time = time.perf_counter()
        predictor.set_image(image)
        image_embedding = predictor.get_image_embedding().detach().cpu().numpy()
        process_time = time.perf_counter() - start_time
        print("Encoding time: ", process_time, "s")

        base = os.path.basename(t)
        base = os.path.splitext(base)[0]
        save_base = os.path.join(args.output, base)
        
        np.save(save_base + ".npy", image_embedding)
    print("Done!")
    
    
if __name__ == "__main__":
    args = parser.parse_args()
    main(args)