from PIL import Image
import argparse
import pathlib
import sys
from photomosaic import img_to_squares, patch_image_from_files, find_color_neighbor
import json
from tqdm import tqdm


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
        help="Name of the image cache JSON file (located in the img_cache folder)",
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

    # check if image cache folder exists
    folder = args.folder
    folder_path = pathlib.Path(folder)
    if not folder_path.exists():
        print(f"Image cache folder does not exist: {folder_path}")
        sys.exit(1)

    # check if image cache JSON file exists
    cache = args.imagecache
    cache_path = folder_path / pathlib.Path(cache)
    if not cache_path.exists():
        print(f"Image cache file does not exist: {cache_path}")
        sys.exit(1)
    else:
        print(f"Loading cache from file: {cache_path}")
        with open(cache_path, "r") as f_in:
            cache_obj = json.load(f_in)
        cache_dict = cache_obj["store"]

    # print image information
    im = Image.open(im_name)
    print(im.format, im.size, im.mode)

    # split the image into squares
    squares = img_to_squares(im, size)

    # Generate an updated list of squares with the thumbnails as squares.
    # process each square, get average color, retrieve nearest thumbnail from cache
    print(f"Collecting thumbnails and finding nearest color matches from {cache}")
    thumb_squares = []
    for row in tqdm(squares):
        new_row = []
        for sq in row:
            # retrieve nearest image name with the closest color from cache
            neighbor = find_color_neighbor(sq, cache_dict)
            # construct path of thumbnail to load
            thumb_path = pathlib.Path(f"{folder}/{neighbor}")
            if not thumb_path.exists():
                print(f"Thumbnail does not exit in image cache: {thumb_path}")
                sys.exit(1)
            new_row.append(thumb_path)
        thumb_squares.append(new_row)

    print(f"Thumbnails collected: {len(thumb_squares) * len(thumb_squares[0])}")

    # generate new image from thumbnails
    mosaic_im = patch_image_from_files(thumb_squares)

    # save new image
    mosaic_name = f"output/{path.stem}_mosaic_{size}{path.suffix}"
    print(f"Saving new image: {mosaic_name}")
    mosaic_im.save(mosaic_name)


if __name__ == "__main__":
    main()
