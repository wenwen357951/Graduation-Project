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
    files_basename = [os.path.basename(filename) for filename in files]
    parent_dir = os.path.abspath(os.path.join(files[0], os.pardir))

    with open(os.path.join(dataset_dir, json_basename), 'r') as json_file:
        json_data = json.load(json_file)
        all_good = True
        for key in json_data:
            image_name = key.split(".jpg")[0] + ".jpg"
            image_size = int(key.split(".jpg")[1])

        try:
            if files_basename.index(image_name) < 0:
                all_good = False
                print("Index Error")

            if os.path.getsize(os.path.join(parent_dir, image_name)) != image_size:
                all_good = False
                print("Size Error!")

        except KeyError:
            all_good = False
            print("Key Missing: " + key)

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
