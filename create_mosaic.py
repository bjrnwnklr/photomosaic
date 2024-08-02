from PIL import Image
import argparse
import pathlib
import sys
from photomosaic import pixelate


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

    # print image information
    im = Image.open(im_name)
    print(im.format, im.size, im.mode)

    # pixelate the image
    pixelated_im = pixelate(im, size)

    # save new image
    tmp_name = f"tmp/{path.stem}_pixelated_{size}{path.suffix}"
    print(f"Saving new image: {tmp_name}")
    pixelated_im.save(tmp_name)


if __name__ == "__main__":
    main()
