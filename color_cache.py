import argparse
import pathlib
import sys
import json
from photomosaic import avg_color
from PIL import Image
from datetime import datetime


def main():
    """The main method"""

    parser = argparse.ArgumentParser(
        description="""Generate a cache file with image names and the
                       average color of the image. Store in a JSON file
                       in the 'img_cache' folder."""
    )
    parser.add_argument(
        "folder",
        nargs="?",
        help="the image cache folder to process",
        default="img_cache",
        type=pathlib.Path,
    )
    parser.add_argument(
        "-i",
        "--imagecache",
        help="Name of the image cache JSON file",
        type=pathlib.Path,
        default="cache.json",
    )
    # Size of the thumbnails (they are square)
    # parser.add_argument(
    #     "-s", "--size", help="Size of the (square) thumbnails.", type=int, default=300
    # )

    args = parser.parse_args()

    # check if image exists, exit if not
    folder = args.folder
    path = pathlib.Path(folder)
    if not path.exists():
        print(f"File does not exist: {folder}")
        sys.exit(-1)

    # check if image cache JSON file exists
    cache = args.imagecache
    cache_path = pathlib.Path(cache)
    if not cache_path.exists():
        print(f"Image cache file does not exist, starting a new one: {cache_path}")
        cache_dict = dict()
        cache_obj = {"store": cache_dict}
    else:
        print(f"Loading cache from file: {cache_path}")
        with open(cache_path, "r") as f_in:
            cache_obj = json.load(f_in)
        cache_dict = cache_obj["store"]

    # process any images not yet in the cache dictionary
    # read images in the folder
    source_images = sorted(path.glob("*.jpg"))
    print(f"Found {len(source_images)} images in folder {path}")
    processed_images = 0
    for src_img in source_images:
        img_path = pathlib.Path(src_img)
        img_name = img_path.name
        if img_name not in cache_dict:
            # image does not yet exist in cache
            print(f"Image {img_name} not found in cache, processing.")
            processed_images += 1
            # get average color of the image
            im = Image.open(img_path)
            RGB_avg = avg_color(im)
            # store time the image was processed
            processed_datetime = datetime.now().isoformat()
            cache_dict[img_name] = {"RGB_avg": RGB_avg, "processed": processed_datetime}
        else:
            # TODO: check if the image in the folder is newer than the processed
            # image
            pass

    # all images processed, store the data in the json file
    # overwrite the json file?
    print(
        f"Cache completed, processed {processed_images} files."
        + f" Total files in cache {len(cache_dict)}"
    )
    # write file back if any changes were done
    if processed_images > 0:
        print(f"Storing cache in: {cache_path}")
        with open(cache_path, "w") as f_out:
            json.dump(cache_obj, f_out)
    else:
        print("No changes processed - cache file not updated on disk.")


if __name__ == "__main__":
    main()
