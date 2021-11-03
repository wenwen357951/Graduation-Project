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
    print("Start process " + dataset_dir, end='')
    image_dir = dataset_dir
    files = glob2.glob(os.path.join(image_dir, "*.jpg"), recursive=True)

    with open(os.path.join(dataset_dir, json_basename), 'r') as json_file:
        json_data = json.load(json_file)
        all_good = True
        for key in json_data:
            image_name = key.split(".jpg")[0] + ".jpg"
            image_path = os.path.join(dataset_dir, image_name)
            image_size = int(key.split(".jpg")[1])
            try:
                if not os.path.exists(image_path):
                    all_good = False
                    raise FileNotFoundError

                if str(os.path.getsize(image_path)) == image_size:
                    all_good = False
                    raise KeyError

            except FileNotFoundError:
                print("Key:", key, "File Not Found! \n", image_path)

            except KeyError:
                print("Size Error: ", image_name, "Actual:", os.path.getsize(image_name))

        if all_good:
            print("\rAll Pass!!")


if __name__ == '__main__':
    KFOLD_DIR = os.path.join(config.LOGS_DIR, "k-fold")

    ALL_DIR = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "BCDE",
        "ACDE",
        "ABDE",
        "ABCE",
        "ABCD"
    ]

    for item in ALL_DIR:
        verify(os.path.join(KFOLD_DIR, item), "via_region_data.json")

    print("done.")
