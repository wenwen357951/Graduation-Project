import json
import os
import sys

import glob2

# Import doc.config
sys.path.append("../../../modules")
# from docs import config
from modules.trclab import config


# noinspection PyUnresolvedReferences
def verify(dataset_dir, json_basename):
    image_dir = dataset_dir
    files = glob2.glob(os.path.join(image_dir, "*.jpg"), recursive=True)

    with open(os.path.join(dataset_dir, json_basename), 'r') as json_file:
        json_data = json.load(json_file)
        if json_data is None:
            return

        all_good = True

        try:
            for item in files:
                filename = "{}{}".format(os.path.basename(item), os.path.getsize(item))
                _ = json_data[filename]

        except KeyError:
            all_good = False
            print("Key Missing: " + filename)

        finally:
            if all_good:
                print("All Pass!!")


if __name__ == '__main__':
    KFOLD_DIR = os.path.join(config.LOGS_DIR, "k-fold")

    ALL_DIR = [
        "BCDE",
        "ACDE",
        "ABDE",
        "ABCE",
        "ABCD"
    ]

    for item in ALL_DIR:
        verify(os.path.join(KFOLD_DIR, item), "via_region_data.json")
