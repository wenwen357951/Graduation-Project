import glob
import os
import sys

from PIL import Image

ROOT_DIR = os.path.abspath("../../../")
sys.path.append(ROOT_DIR)

from modules.trclab import config
# image import from config path
image_dir = config.ASSETS_VHP_SEG_DIR
# image_dir = '/assets/data-augmentation/MirrorResize (1000 x 570)'

# find every image in dir
files = glob.glob(os.path.join(image_dir, "*.bmp"), recursive=True)


def main():
    # give it a loop to process every image
    for file in files:
        # load image
        im = Image.open(file)
        # roatate image
        im_rotate = im.rotate(10)
        # save image
        im_rotate.save(
            os.path.join(config.LOGS_DIR, "SEG Left 10Degree (1000 x 570)/{}".format(os.path.basename(file))),
            quality=100)


if __name__ == '__main__':
    main()
