# -*- coding: utf-8 -*-
# J094
# 2023.05.19
import os
import sys
sys.path.append(os.path.realpath("."))

import os
import argparse
import torch
import time
import numpy as np
import matplotlib.pyplot as plt

from segment_anything import sam_model_registry
from src.sam.predictor_custom import SamPredictorCustom

parser = argparse.ArgumentParser(
    description=(
        "Runs automatic mask generation on an input_embedding image or directory of images, "
        "and outputs masks as either PNGs or COCO-style RLEs. Requires open-cv, "
        "as well as pycocotools if saving in RLE format."
    )
)

parser.add_argument(
    "--input-image",
    type=str,
    default="data/image/500",
    # required=True,
    help="Path to either a single input_embedding image embedding or folder of image embeddings.",
)

parser.add_argument(
    "--input-embedding",
    type=str,
    default="data/embedding/500",
    # required=True,
    help="Path to either a single input_embedding image embedding or folder of image embeddings.",
)

parser.add_argument(
    "--output",
    type=str,
    default="result/500",
    # required=True,
    help=(
        "Path to the directory where masks will be output."
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
    "--checkpoint-prompt",
    type=str,
    default="ckpt/vit_h_prompt_encoder.pth",
    # required=True,
    help="The path to the SAM checkpoint to use for prompt encoding.",
)

parser.add_argument(
    "--checkpoint-mask",
    type=str,
    default="ckpt/vit_h_mask_decoder.pth",
    # required=True,
    help="The path to the SAM checkpoint to use for mask decoding.",
)

parser.add_argument("--device", type=str, default="cuda", help="The device to run generation on.")

def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))  

def main(args: argparse.Namespace) -> None:
    print("Loading model...")
    sam = sam_model_registry[args.model_type]()
    with open(args.checkpoint_prompt, "rb") as f:
        state_dict_prompt = torch.load(f)
    sam.prompt_encoder.load_state_dict(state_dict_prompt)
    with open(args.checkpoint_mask, "rb") as f:
        state_dict_mask = torch.load(f)
    sam.mask_decoder.load_state_dict(state_dict_mask)
    _ = sam.to(device=args.device)
    
    predictor = SamPredictorCustom(sam)
    
    if not os.path.isdir(args.input_embedding):
        targets = [args.input_embedding]
    else:
        targets = [
            f for f in os.listdir(args.input_embedding) if not os.path.isdir(os.path.join(args.input_embedding, f))
        ]
        targets = [os.path.join(args.input_embedding, f) for f in targets]

    os.makedirs(args.output, exist_ok=True)

    for t in targets:
        print(f"Processing '{t}'...")

        base = os.path.basename(t)
        base = os.path.splitext(base)[0]
        save_base = os.path.join(args.output, base)

        image = plt.imread(args.input_image + "/" + base + ".jpg")
        if image is None:
            print(f"Could not load '{t}' as an image, skipping...")
            continue

        image_embedding = np.load(t)
        if image_embedding is None:
            print(f"Could not load '{t}' as an image embedding, skipping...")
            continue
        image_embedding = torch.from_numpy(image_embedding).to(device=args.device)

        predictor.features = image_embedding
        
        start_time = time.perf_counter()
        predictor.set_image_decode_only(image)
        process_time = time.perf_counter() - start_time
        print("Set image time: ", process_time, "s")

        points = list()
        plt.figure(figsize=(15,10))
        plt.imshow(image)
        point = plt.ginput(n=1, show_clicks=True)
        plt.close()
        print("Prompt point is: ", point)
        points.append(point[0])
        plt.figure(figsize=(15,10))
        plt.imshow(image)
        point = plt.ginput(n=1, show_clicks=True)
        plt.close()
        print("Prompt point is: ", point)
        points.append(point[0])
        plt.figure(figsize=(15,10))
        plt.imshow(image)
        point = plt.ginput(n=1, show_clicks=True)
        plt.close()
        print("Prompt point is: ", point)
        points.append(point[0])
        input_point = np.array(points)
        input_label = np.array([1] * len(points))
        # input_label = np.array([1] + [0] * (len(points) - 1))
        plt.figure(figsize=(15,10))
        plt.imshow(image)
        point_1 = plt.ginput(n=1, show_clicks=True)
        plt.close()
        print("Prompt box point 1 is: ", point_1)
        plt.figure(figsize=(15,10))
        plt.imshow(image)
        point_2 = plt.ginput(n=1, show_clicks=True)
        plt.close()
        print("Prompt box point 2 is: ", point_2)
        box = [point_1[0][0], point_1[0][1], point_2[0][0], point_2[0][1]]
        input_box = np.array(box)
        
        start_time = time.perf_counter()
        masks, scores, logits = predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            # point_coords=None,
            # point_labels=None,
            box=input_box[None, :],
            multimask_output=True,
        )
        process_time = time.perf_counter() - start_time
        print("Decoding time: ", process_time, "s")
        

        for i, (mask, score) in enumerate(zip(masks, scores)):
            plt.figure(figsize=(15,10))
            plt.imshow(image)
            show_mask(mask, plt.gca())
            show_points(input_point, input_label, plt.gca())
            show_box(input_box, plt.gca())
            plt.title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
            plt.show()
    print("Done!")
    
    
if __name__ == "__main__":
    args = parser.parse_args()
    main(args)