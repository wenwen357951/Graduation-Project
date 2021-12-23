import os
import sys

from PIL import Image, ImageOps
from glob2 import glob

ROOT_DIR = os.path.abspath("../../../")
sys.path.append(ROOT_DIR)
from modules.trclab import config

# image import from config path
image_dir = config.ASSETS_VHP_SEG_DIR
# find every image in dir
files = glob(os.path.join(image_dir, "*.bmp"), recursive=True)


def main():
    # setting output dir
    output_dir = os.path.join(config.LOGS_DIR, "SEG Mirror (1000 X 570)")
    # expect problame
    if not os.path.exists(output_dir):
        print("Output Dir isn't exists")
        os.mkdir(config.LOGS_DIR)
        os.mkdir(output_dir)

    # out put file give it a loop to process mirror
    for file in files:
        print(os.path.basename(file))
        im = Image.open(file)
        im_flip = ImageOps.mirror(im)
        im_flip.save(os.path.join(config.LOGS_DIR, "SEG Mirror (1000 X 570)/{}".format(os.path.basename(file))),
                     quality=100)


if __name__ == '__main__':
    main()
