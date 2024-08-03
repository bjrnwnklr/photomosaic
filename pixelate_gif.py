from PIL import Image
import argparse
import pathlib
import sys
from photomosaic import pixelate_gif


def main():
    """The main method"""

    parser = argparse.ArgumentParser(description="Pixelate a given image into a GIF.")
    # path of the image
    parser.add_argument(
        "image",
        nargs="?",
        help="the image to convert",
        default="cat.jpg",
        type=pathlib.Path,
    )
    # option to to specify the size of the pixels to generate in the pixelated image
    parser.add_argument(
        "-s",
        "--start",
        help="Starting size of the pixels (i.e. largest value). Default: 500",
        default=500,
        type=int,
    )
    parser.add_argument(
        "-e",
        "--end",
        help="End size of the pixels (i.e. smallest value). Default: 5",
        default=5,
        type=int,
    )
    parser.add_argument(
        "-n",
        "--number-of-steps",
        help="Number of steps between start and end pixel size. Default: 10",
        default=10,
        type=int,
    )

    args = parser.parse_args()

    # check if image exists, exit if not
    im_name = args.image
    path = pathlib.Path(im_name)
    if not path.exists():
        print(f"File does not exist: {im_name}")
        sys.exit(-1)

    start = args.start
    end = args.end
    steps = args.number_of_steps

    # print image information
    im = Image.open(im_name)
    print(im.format, im.size, im.mode)

    # pixelate the image
    pixelated_im = pixelate_gif(im, start, end, steps)

    # save gif
    tmp_name = f"output/{path.stem}_pixelated_{start}_{end}_{steps}.gif"
    print(f"Saving new image: {tmp_name}")
    pixelated_im[0].save(
        tmp_name,
        save_all=True,
        append_images=pixelated_im[1:],
        optimize=False,
        duration=1000,
        loop=0,
    )


if __name__ == "__main__":
    main()
