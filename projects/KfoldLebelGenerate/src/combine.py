import glob2
import json
import os
import shutil
import sys

sys.path.append("../../../modules")
from modules.trclab import config

OUTPUT_DIR = os.path.join(config.LOGS_DIR, "k-fold")

A_LABEL_PATH = "E:/PCP-NEW/Graduation-Project/logs/k-fold/A/via_region_data.json"
B_LABEL_PATH = "E:/PCP-NEW/Graduation-Project/logs/k-fold/B/via_region_data.json"
C_LABEL_PATH = "E:/PCP-NEW/Graduation-Project/logs/k-fold/C/via_region_data.json"
D_LABEL_PATH = "E:/PCP-NEW/Graduation-Project/logs/k-fold/D/via_region_data.json"
E_LABEL_PATH = "E:/PCP-NEW/Graduation-Project/logs/k-fold/E/via_region_data.json"

A_IMAGE_DIR = "E:/PCP-NEW/Graduation-Project/logs/k-fold/A"
B_IMAGE_DIR = "E:/PCP-NEW/Graduation-Project/logs/k-fold/B"
C_IMAGE_DIR = "E:/PCP-NEW/Graduation-Project/logs/k-fold/C"
D_IMAGE_DIR = "E:/PCP-NEW/Graduation-Project/logs/k-fold/D"
E_IMAGE_DIR = "E:/PCP-NEW/Graduation-Project/logs/k-fold/E"

DATASET_PATH = [
    A_IMAGE_DIR,
    B_IMAGE_DIR,
    C_IMAGE_DIR,
    D_IMAGE_DIR,
    E_IMAGE_DIR
]

DATASET_IMAGE_DIR_PATH = [
    list(),
    list(),
    list(),
    list(),
    list()
]

DATASET_IMAGE_MAPS = [
    [1, 2, 3, 4],
    [0, 2, 3, 4],
    [0, 1, 3, 4],
    [0, 1, 2, 4],
    [0, 1, 2, 3]
]

COPY_DICT = dict()

LABEL_PATH_DICT = {
    "BCDE": A_LABEL_PATH,
    "ACDE": B_LABEL_PATH,
    "ABDE": C_LABEL_PATH,
    "ABCE": D_LABEL_PATH,
    "ABCD": E_LABEL_PATH
}


def readimagename():
    for idx, path in enumerate(DATASET_PATH):
        DATASET_IMAGE_DIR_PATH[idx] = glob2.glob(os.path.join(path, "*.png"), recursive=True)

    for arrayidx, DataSetDirMaps in enumerate(DATASET_IMAGE_MAPS):
        dirname = ""
        for idx in DataSetDirMaps:
            dirname += chr(ord('A') + idx)

        temp = os.path.join(OUTPUT_DIR, dirname)
        if os.path.exists(temp):
            if not os.path.isdir(temp):
                os.remove(temp)
                os.mkdir(temp)
        else:
            os.mkdir(temp)

        for idx in DataSetDirMaps:
            for oldfilename in DATASET_IMAGE_DIR_PATH[idx]:
                newfilename = os.path.join(OUTPUT_DIR, dirname, os.path.basename(oldfilename))
                COPY_DICT[newfilename] = oldfilename
            # oldname
        # print(arrayidx, DataSetDirMaps, name)


def copyImage():
    for key in COPY_DICT:
        new_name = key
        old_name = COPY_DICT[key]
        shutil.copy(old_name, new_name)


def make_Json():
    for idx, key in enumerate(LABEL_PATH_DICT):
        print("Start process: ", idx)
        label_filename = LABEL_PATH_DICT[key]
        output_path = os.path.join(OUTPUT_DIR, key, os.path.basename(label_filename))
        result_json_data = dict()
        for dataset_list_idx in DATASET_IMAGE_MAPS[idx]:
            old_json_filename = os.path.join(DATASET_PATH[dataset_list_idx], os.path.basename(label_filename))
            with open(old_json_filename, "r") as json_stream:
                result_json_data.update(json.load(json_stream))

        print("Merge Successful!")

        with open(output_path, "w+") as file_stream:
            print("Export Json data!")
            json.dump(result_json_data, file_stream)


def main():
    readimagename()
    copyImage()
    # make_Json()


if __name__ == '__main__':
    main()
