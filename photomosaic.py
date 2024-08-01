from PIL import Image
import argparse
import pathlib


def img_to_squares(im: Image, sq_size=50):
    """Divide the input image into squares. The squares parameter defines the size in pixels of the squares
    e.g. 100 = break image into squares of 100x100 size."""
    # get size of the image
    width, height = im.size
    # calculate how many squares in the image, cut off the last remaining one on the right and bottom
    row_squares = height // sq_size
    col_squares = width // sq_size
    print(f"Image has {col_squares} * {row_squares} squares of size {sq_size}")

    # break into squares using the Image.crop function
    squares = []
    for r in range(row_squares):
        row = []
        for c in range(col_squares):
            square = im.crop(
                (c * sq_size, r * sq_size, (c + 1) * sq_size, (r + 1) * sq_size)
            )
            row.append(square)
            color = avg_color(square)
            print(f"Square [{r}, {c}]: {square.size}. Avg color: {color}")
        squares.append(row)


def avg_color(im: Image) -> tuple[int]:
    """Calculate the average color (in an RGB tuple) of a p
    provided image.

    Args:
        im (Image): Input image

    Returns:
        tuple[int]: RGB color tuple
    """
    # get the individual pixels by color band
    R = list(im.getdata(0))
    R_avg = int(sum(R) / len(R))
    G = list(im.getdata(1))
    G_avg = int(sum(G) / len(G))
    B = list(im.getdata(2))
    B_avg = int(sum(B) / len(B))

    return (R_avg, G_avg, B_avg)


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
