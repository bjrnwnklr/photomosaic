from PIL import Image
import argparse
import pathlib


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


if __name__ == "__main__":
    main()
