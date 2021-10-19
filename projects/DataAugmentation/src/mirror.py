import os
import sys

from PIL import Image, ImageOps
from glob2 import glob

ROOT_DIR = os.path.abspath("../../../")
sys.path.append(ROOT_DIR)
from docs import config

image_dir = config.ASSETS_ALIGNMENT_CT_RESIZE_DIR
files = glob(os.path.join(image_dir, "*.jpg"), recursive=True)


def main():
    output_dir = os.path.join(config.LOGS_DIR, "MirrorCtResize (1000 x 570)")
    if not os.path.exists(output_dir):
        print("Output Dir isn't exists")
        os.mkdir(config.LOGS_DIR)
        os.mkdir(output_dir)

    for file in files:
        print(os.path.basename(file))
        im = Image.open(file)
        im_flip = ImageOps.mirror(im)
        im_flip.save(os.path.join(config.LOGS_DIR, "MirrorCtResize (1000 x 570)/{}".format(os.path.basename(file))),
                     quality=100)


if __name__ == '__main__':
    main()
