import json
import os
import sys

# Import doc.config
sys.path.append("../../../modules")
# from docs import config
from modules.trclab import config


# noinspection PyUnresolvedReferences
def main():
    image_dir = config.DATASET_DA_CT_R_5o
    print(image_dir)
    files = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]

    with open(os.path.join(config.LABEL_MRCNN_DIR, "normal_R5.json"), 'r') as json_file:
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
    main()
