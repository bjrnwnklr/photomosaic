from PIL import Image
import argparse
import pathlib


def img_to_squares(im, sq_size=50):
    """Divide the input image into squares. The squares parameter defines the size in pixels of the squares
    e.g. 100 = break image into squares of 100x100 size."""
    # get size of the image
    width, height = im.size
    # calculate how many squares in the image, cut off the last remaining one on the right and bottom
    row_squares = height // sq_size
    col_squares = width // sq_size
    print(f"Image has {col_squares} * {row_squares} squares of size {sq_size}")


def main():
    """The main method"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "image",
        nargs="?",
        help="the image to convert",
        default="cat.jpg",
        type=pathlib.Path,
    )
    # TODO: add option to resize by entering width and height arguments (or just one?)
    size = (120, 80)

    args = parser.parse_args()

    # check if image exists, exit if not
    im_name = args.image
    path = pathlib.Path(im_name)
    if not path.exists():
        print(f"File does not exist: {im_name}")
        sys.exit(-1)

    # print image information
    im = Image.open(im_name)
    print(im.format, im.size, im.mode)

    # cut into squares
    img_to_squares(im, 50)


if __name__ == "__main__":
    main()
