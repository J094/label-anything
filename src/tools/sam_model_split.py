# -*- coding: utf-8 -*-
# J094
# 2023.05.19
import os
import sys
sys.path.append(os.path.realpath("."))

import torch
import argparse

from segment_anything import sam_model_registry

parser = argparse.ArgumentParser()

parser.add_argument(
    "--model-type",
    type=str,
    required=True,
    help="The type of model to load, in ['default', 'vit_h', 'vit_l', 'vit_b']",
)

parser.add_argument(
    "--checkpoint",
    type=str,
    required=True,
    help="The path to the SAM checkpoint to use for mask generation.",
)

parser.add_argument(
    "--output",
    type=str,
    required=True,
    help="Path to the directory where ckpt will be output.",
)

def main(args: argparse.Namespace) -> None:
    print("Loading model...")
    sam = sam_model_registry[args.model_type](checkpoint=args.checkpoint)
    print("Saving model...")
    torch.save(sam.image_encoder.state_dict(), args.output + "/" + args.model_type + "_image_encoder.pth")
    torch.save(sam.prompt_encoder.state_dict(), args.output + "/" + args.model_type + "_prompt_encoder.pth")
    torch.save(sam.mask_decoder.state_dict(), args.output + "/" + args.model_type + "_mask_decoder.pth")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)