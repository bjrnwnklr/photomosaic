from PIL import Image
import argparse
import pathlib
import sys


def img_to_squares(im: Image.Image, sq_size=50):
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
        squares.append(row)

    return squares


def generate_color_block(
    width: int, height: int, color: tuple[int, int, int]
) -> Image.Image:
    """Generate a new image with width x height and the color provided."""
    im = Image.new("RGB", (width, height), color=color)
    return im


def avg_color(im: Image.Image) -> tuple[int]:
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


def generate_avg_color_image(
    squares: list[list[Image.Image]],
) -> list[list[Image.Image]]:
    """Generate a new two dimensional list of squares, each square with the average color
    of the original list of squares."""
    new_squares = []
    for row in squares:
        new_row = []
        for sq in row:
            new_row.append(generate_color_block(sq.size[0], sq.size[1], avg_color(sq)))
        new_squares.append(new_row)

    return new_squares


def patch_image(squares: list[list[Image.Image]]) -> Image.Image:
    """Generate a new image from the provided two dimensional list of squares.

    Assumption is that each square has the same size."""
    # assume each image in the row has the same height, and each
    # image in a column has the same height. Use the first image of
    width = len(squares[0]) * squares[0][0].size[0]
    height = len(squares) * squares[0][0].size[1]
    print(f"Calculated size of new image: {width} x {height}")

    # create new image
    im = Image.new("RGB", (width, height))
    print(f"New image dimensions: {im.size}")
    # patch the image together
    print("Patching new image together from squares")
    height = 0
    for row in squares:
        width = 0
        for sq in row:
            im.paste(sq, (width, height))
            width += sq.size[0]
        height += sq.size[1]

    return im


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
    length = 50
    print("Generating squares from original image")
    squares = img_to_squares(im, length)
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
