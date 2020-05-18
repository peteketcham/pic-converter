#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

import argparse
import PIL
from PIL import Image
from pathlib import Path


def resize_all(path, output_path, max_dimension):
    p = Path(path)
    for item in p.rglob("*"):
        try:
            image = Image.open(item)
        except (PIL.UnidentifiedImageError, PermissionError, IsADirectoryError):
            continue
        # if max_dimension >= max(image.size):
        #     continue
        # ratio = max_dimension / max(image.size)
        # new_image_size = tuple([int(x * ratio) for x in image.size])
        new_image_size = dimensions(image.size, max_dimension)
        if new_image_size is None:
            continue
        print(item, image.size, new_image_size)
        image = image.resize(new_image_size)
        new_file = Path(output_path).joinpath(*item.parts)
        # create folder if it doesn't exist
        new_file.parent.mkdir(parents=True, exist_ok=True)
        image.save(new_file)


def dimensions(image_size, dimension_tup):
    """
    dimension_tup[0] == size
    dimension_tup[1] == width
    dimension_tup[2] == height
    """
    if not any(dimension_tup):
        return image_size
    if dimension_tup[1] and dimension_tup[2]:
        # max width and max height
        ratio = min(dimension_tup[1] / image_size[0],
                    dimension_tup[2] / image_size[1])
    elif dimension_tup[1]:
        # max width
        if dimension_tup[1] < image_size[0]:
            ratio = dimension_tup[1] / image_size[0]
        else:
            return None
    elif dimension_tup[2]:
        # max height
        if dimension_tup[2] < image_size[1]:
            ratio = dimension_tup[2] / image_size[1]
        else:
            return None
    else:
        # max dimension
        ratio = dimension_tup[0] / max(image_size)
        if ratio > 1:
            return None
    return tuple([int(x * ratio) for x in image_size])


def main():
    parser = argparse.ArgumentParser(description='Process images to size to a maximum.')
    parser.add_argument('path', type=str, help='an integer for the accumulator')
    parser.add_argument("--size", action="store", help="maximum dimension", type=int)
    parser.add_argument("--width", action="store", help="maximum width", type=int)
    parser.add_argument("--height", action="store", help="maximum height", type=int)

    args = parser.parse_args()
    if args.size is None and args.width is None and args.height is None:
        parser.error("at least one of --size, --width, or --height are required")

    resize_all(args.path, "_optimized", (args.size, args.width, args.height))


if __name__ == "__main__":
    main()
