import os
import sys

# Import doc.config
sys.path.append("../../../")
from modules.trclab import config


def main():
    image_dir = config.DATASET_DA_CT_L_5o
    files = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
    filename_hj = "{}{}".format(os.path.basename(files), os.path.getsize(files))
    print(filename_hj)


if __name__ == '__main__':
    main()
