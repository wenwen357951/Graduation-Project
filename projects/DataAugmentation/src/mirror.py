import sys
import os
import glob
from PIL import Image, ImageOps

ROOT_DIR = os.path.abspath("../../../")
sys.path.append(ROOT_DIR)

from mydocs import config

image_dir = config.ASSETS_ALIGNMENT_CT_RESIZE_DIR
files = glob.glob(os.path.join(image_dir, "*.jpg"), recursive=True)


def main():
    for file in files:
        im = Image.open(file)
        im_flip = ImageOps.mirror(im)
        im_flip.save(os.path.join(config.LOGS_DIR, "MirrorCtResize (1000 x 570)/{}".format(os.path.basename(file))), quality=100)


if __name__ == '__main__':
    main()
