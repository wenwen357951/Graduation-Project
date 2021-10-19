import glob
import os
import sys

from PIL import Image

ROOT_DIR = os.path.abspath("../../../")
sys.path.append(ROOT_DIR)

from docs import config

# image_dir = config.ASSETS_ALIGNMENT_CT_RESIZE_DIR
image_dir = '/logs/MirrorCtResize (1000 x 570)'
files = glob.glob(os.path.join(image_dir, "*.jpg"), recursive=True)


def main():
    for file in files:
        im = Image.open(file)
        im_rotate = im.rotate(5)
        im_rotate.save(os.path.join(config.LOGS_DIR, "MirrorCtTurnLeft5Degree (1000 x 570)/{}".format(os.path.basename(file))), quality=100)


if __name__ == '__main__':
    main()
