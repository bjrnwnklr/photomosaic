from PIL import Image, ImageOps
import argparse
import pathlib
import sys


def rotate_image(im):
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
    rotation = im.getexif()[274]
    if rotation == 3:
        angle = 180
    elif rotation == 6:
        angle = 270
    elif rotation == 8:
        angle = 90
    else:
        angle = 0
    return im.rotate(angle=angle, expand=True)


def crop_image(im: Image.Image, size):
    """Crop an image to the specified size.
    Cropping is done by cropping the middle of the image by fitting the crop
    box into the middle of the image"""
    # calculate top left of middle section of image
    top = int((im.size[0] - size[0]) / 2)
    left = int((im.size[1] - size[1]) / 2)

    return im.crop((top, left, top + size[0], left + size[1]))


def create_thumbnail(im_path: pathlib.Path, size, folder):
    """Generate a thumbnail with dimensions size and store in folder"""
    # load the image from the provided path
    im = Image.open(im_path)
    # rotate the image if required
    im = rotate_image(im)
    thumb = ImageOps.cover(im, size)
    thumb = crop_image(thumb, size)
    img_name = f"{folder}/thump_{im_path.stem}{im_path.suffix}"
    print(f"Saving thumbnail {img_name}")
    thumb.save(img_name)


def main():
    """The main method"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder",
        nargs="?",
        help="the image folder to process",
        default="/mnt/d/folders/Pictures/2019/2019-09-07 USA 2019",
        type=pathlib.Path,
    )
    # TODO: add option to resize by entering width and height arguments (or just one?)
    size = (300, 300)

    args = parser.parse_args()

    # check if image exists, exit if not
    folder = args.folder
    path = pathlib.Path(folder)
    if not path.exists():
        print(f"File does not exist: {folder}")
        sys.exit(-1)

    # read images in the folder
    source_images = sorted(path.glob("*.jpg"))
    print(f"Found {len(source_images)} images in folder {path}")

    folder = "img_cache"
    for src_img in source_images:
        create_thumbnail(pathlib.Path(src_img), size, folder)


if __name__ == "__main__":
    main()
