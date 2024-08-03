from PIL import Image, ImageOps
import pathlib
import math
import random


def img_to_squares(im: Image.Image, sq_size=50):
    """Divide the input image into squares. The squares parameter defines
    the size in pixels of the squares
    e.g. 100 = break image into squares of 100x100 size."""
    # get size of the image
    width, height = im.size
    # calculate how many squares in the image, cut off the last remaining one on
    # the right and bottom
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
    """Generate a new two dimensional list of squares, each square with
    the average color
    of the original list of squares."""
    new_squares = []
    for row in squares:
        new_row = []
        for sq in row:
            new_row.append(generate_color_block(sq.size[0], sq.size[1], avg_color(sq)))
        new_squares.append(new_row)

    return new_squares


def patch_image_from_images(squares: list[list[Image.Image]]) -> Image.Image:
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


def patch_image_from_files(squares: list[list[str]]) -> Image.Image:
    """Generate a new image from the provided two dimensional list of squares.
    Loads the images from the filenames provided.

    Assumption is that each square has the same size."""
    # load the first thumbnail to calculate the size
    sq0 = squares[0][0]
    with open(sq0, "rb") as thumb_f:
        sq0_im = Image.open(thumb_f)
        # assume each image in the row has the same height, and each
        # image in a column has the same height. Use the first image of
        width = len(squares[0]) * sq0_im.size[0]
        height = len(squares) * sq0_im.size[1]
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
            tmp_im = Image.open(sq)
            im.paste(tmp_im, (width, height))
            width += tmp_im.size[0]
        height += tmp_im.size[1]

    return im


def pixelate(im: Image.Image, size: int) -> Image.Image:
    """Convenience function: cut an image into squares of size and
    generate a new image with average color of the squares. Return
    the new image."""
    print("Generating squares from original image")
    squares = img_to_squares(im, size)
    # generate a new image with the dimensions of the squares
    print("Generating avg color squares from original squares")
    new_squares = generate_avg_color_image(squares)
    print(f"New avg square, first square: {new_squares[0][0].size}")

    # patch the new image together
    print("Patching new image together from avg color squares")
    new_im = patch_image_from_images(new_squares)

    return new_im


def pixelate_gif(
    im: Image.Image, start: int, end: int, steps: int
) -> list[Image.Image]:
    """Convenience function: Generate an animated GIF out of a sequence
    of pixelated images.
    Start: % of the original image to be used as one square (default: 100)
    end: % of the original image to be used as a square (default: 5)
    steps: number of steps between start and end %

    Example:
    start = 100, end = 20, steps = 4.
    Images generated with 100, 80, 60, 40, 20 % of the image size as pixel squares.
    """
    gif = []
    for pixel_size in range(start, end + 1, -1 * (start - end) // steps):
        # calculate size of the pixelation from largest side of the image
        size = max(im.size) // pixel_size
        print(f"Generating squares from original image, pixel size {size}")
        squares = img_to_squares(im, size)
        # generate a new image with the dimensions of the squares
        print("Generating avg color squares from original squares")
        new_squares = generate_avg_color_image(squares)
        print(f"New avg square, first square: {new_squares[0][0].size}")

        # patch the new image together
        print("Patching new image together from avg color squares")
        new_im = patch_image_from_images(new_squares)
        gif.append(new_im)

    return gif


def rotate_image(im: Image.Image) -> Image.Image:
    """Rotate an image according to the rotation stored in the images Exif data
    1 = Horizontal (normal)
    2 = Mirror horizontal
    3 = Rotate 180
    4 = Mirror vertical
    5 = Mirror horizontal and rotate 270 CW
    6 = Rotate 90 CW
    7 = Mirror horizontal and rotate 90 CW
    8 = Rotate 270 CW
    """
    # get rotation from EXIF
    exif = im.getexif()
    if 274 in exif:
        rotation = exif[274]
        if rotation == 3:
            angle = 180
        elif rotation == 6:
            angle = 270
        elif rotation == 8:
            angle = 90
        else:
            angle = 0
        return im.rotate(angle=angle, expand=True)
    else:
        # no rotation data found in exif information,
        # return the original image
        return im


def crop_image(im: Image.Image, size: int) -> Image.Image:
    """Crop an image to the specified size.
    Cropping is done by cropping the middle of the image by fitting the crop
    box into the middle of the image"""
    # calculate top left of middle section of image
    top = int((im.size[0] - size[0]) / 2)
    left = int((im.size[1] - size[1]) / 2)

    return im.crop((top, left, top + size[0], left + size[1]))


def create_thumbnail(im_path: pathlib.Path, size: int, folder: str):
    """Generate a thumbnail with dimensions size and store in folder"""
    # load the image from the provided path
    im = Image.open(im_path)
    # rotate the image if required
    im = rotate_image(im)
    # create the thumbnail. This will create an image with the smallest
    # size as provided size
    # e.g. size = 300, image is 4000 x 3000, new image will be 400 x 300
    thumb = ImageOps.cover(im, (size, size))
    # crop the image to the specified size in the middle of the provided image
    # new image will be 300 x 300, the previously longer side is cut to
    # 300 and centered in the previous 400 side (cut is from 50 to 350)
    thumb = crop_image(thumb, (size, size))
    # save in folder with 'thumb' prefix
    img_name = f"{folder}/thump_{im_path.stem}{im_path.suffix}"
    # print(f"Saving thumbnail {img_name}")
    thumb.save(img_name)


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
    # TODO: find a smarter way of searching through the cache
    min_dist = 1_000
    # set a default random image from the cache in case nothing is found
    min_thumb = random.choice(list(cache_dict.keys()))
    threshold = 4
    for k, v in cache_dict.items():
        dist = color_distance(src_avg_RGB, v["RGB_avg"])
        if dist < min_dist:
            min_dist = dist
            min_thumb = k
        # stop searching if we found a close enough match
        if min_dist <= threshold:
            break

    return min_thumb
