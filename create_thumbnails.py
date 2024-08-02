import argparse
import pathlib
import sys
from photomosaic import create_thumbnail


def main():
    """The main method"""

    parser = argparse.ArgumentParser(
        description="""Generate square thumbnails of all JPG files
                                     int the provided folder."""
    )
    parser.add_argument(
        "folder",
        nargs="?",
        help="the image folder to process",
        default="/mnt/d/folders/Pictures/2019/2019-09-07 USA 2019",
        type=pathlib.Path,
    )
    # Size of the thumbnails (they are square)
    parser.add_argument(
        "-s", "--size", help="Size of the (square) thumbnails.", type=int, default=300
    )

    args = parser.parse_args()

    # check if image exists, exit if not
    folder = args.folder
    path = pathlib.Path(folder)
    if not path.exists():
        print(f"File does not exist: {folder}")
        sys.exit(-1)

    size = args.size

    # read images in the folder
    source_images = sorted(path.glob("*.jpg"))
    print(f"Found {len(source_images)} images in folder {path}")

    folder = "img_cache"
    for src_img in source_images:
        create_thumbnail(pathlib.Path(src_img), size, folder)


if __name__ == "__main__":
    main()
