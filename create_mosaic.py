from PIL import Image
import argparse
import pathlib
import sys
from photomosaic import img_to_squares, patch_image, avg_color
import json
import math
import random


def color_distance(a_RGB: tuple[int, int, int], b_RGB: tuple[int, int, int]) -> int:
    """Return an integer value of the pythagorean distance of the two RGB tuples
    from each other."""
    dist = 0
    for a, b in zip(a_RGB, b_RGB):
        dist += (a - b) ** 2
    return math.sqrt(dist)


def find_color_neighbor(im: Image.Image, cache_dict: dict) -> str:
    """Find the nearest image from the image cache that is close to the average
    RGB of the provided image."""
    src_avg_RGB = avg_color(im)
    print(f"Searching for color match for average color {src_avg_RGB}")
    # TODO: find a smarter way of searching through the cache
    min_dist = 1_000
    # set a default random image from the cache in case nothing is found
    min_thumb = random.choice(cache_dict)
    threshold = 10
    for k, v in cache_dict.items():
        dist = color_distance(src_avg_RGB, v["RGB_avg"])
        if dist < min_dist:
            min_dist = dist
            min_thumb = k
        # stop searching if we found a close enough match
        if min_dist <= threshold:
            print(f"Found a close enough match: {min_dist}, {min_thumb}")
            break

    print("Found neighbor: {min_dist}, {min_thumb}")
    return min_thumb


def main():
    """The main method"""

    parser = argparse.ArgumentParser(
        description="Create a photomosaic of a given image."
    )
    # path of the image
    parser.add_argument(
        "image",
        nargs="?",
        help="the image to convert",
        default="cat.jpg",
        type=pathlib.Path,
    )
    # image cache folder
    parser.add_argument(
        "folder",
        nargs="?",
        help="the image cache folder to process",
        default="img_cache",
        type=pathlib.Path,
    )
    # name of the image cache JSON file
    parser.add_argument(
        "-i",
        "--imagecache",
        help="Name of the image cache JSON file",
        type=pathlib.Path,
        default="cache.json",
    )
    # option to to specify the size of the pixels to generate in the pixelated image
    parser.add_argument("-s", "--size", help="Size of the pixels", default=50, type=int)

    args = parser.parse_args()

    # check if image exists, exit if not
    im_name = args.image
    path = pathlib.Path(im_name)
    if not path.exists():
        print(f"File does not exist: {im_name}")
        sys.exit(-1)

    size = args.size

    # check if image cache JSON file exists
    cache = args.imagecache
    cache_path = pathlib.Path(cache)
    if not cache_path.exists():
        print(f"Image cache file does not exist: {cache_path}")
        sys.exit(1)
    else:
        print(f"Loading cache from file: {cache_path}")
        with open(cache_path, "r") as f_in:
            cache_obj = json.load(f_in)
        cache_dict = cache_obj["store"]

    # check if image cache folder exists
    folder = args.folder
    folder_path = pathlib.Path(folder)
    if not folder_path.exists():
        print(f"Image cache folder does not exist: {folder_path}")
        sys.exit(1)

    # print image information
    im = Image.open(im_name)
    print(im.format, im.size, im.mode)

    # split the image into squares
    squares = img_to_squares(im, size)

    # Generate an updated list of squares with the thumbnails as squares.
    # process each square, get average color, retrieve nearest thumbnail from cache
    for row in squares:
        new_row = []
        for sq in row:
            # retrieve nearest image name with the closest color from cache
            neighbor = find_color_neighbor(sq, cache_dict)
            neighbor_im = Image.load()

    # save new image
    # tmp_name = f"tmp/{path.stem}_pixelated_{size}{path.suffix}"
    # print(f"Saving new image: {tmp_name}")
    # pixelated_im.save(tmp_name)


if __name__ == "__main__":
    main()
