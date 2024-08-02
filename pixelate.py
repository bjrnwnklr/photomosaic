from PIL import Image
import argparse
import pathlib
import sys
from photomosaic import img_to_squares, generate_avg_color_image, patch_image


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

    # cut into squares
    print("Generating squares from original image")
    squares = img_to_squares(im, size)
    # generate a new image with the dimensions of the squares
    print("Generating avg color squares from original squares")
    new_squares = generate_avg_color_image(squares)
    print(f"New avg square, first square: {new_squares[0][0].size}")

    # patch the new image together
    print("Patching new image together from avg color squares")
    new_im = patch_image(new_squares)
    # save new image
    print("Saving new image")
    tmp_name = "tmp/tmp.jpg"
    new_im.save(tmp_name)


if __name__ == "__main__":
    main()
