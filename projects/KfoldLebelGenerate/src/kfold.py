import json
import os
import pathlib
import shutil
import sys

sys.path.append("../../../modules")
from modules.trclab import config

OUTPUT_DIR = os.path.join(config.LOGS_DIR, "k-fold")
LABEL_DICT = {
    "normal": {
        "0": {
            "label_filepath": config.LABEL_MRCNN,
            "dataset_path": config.DATASET_ALIGNMENT_CT_RESIZE,
            "template_name": "normal_{}.{}"
        },
        "l5": {
            "label_filepath": config.LABEL_MRCNN_L5,
            "dataset_path": config.DATASET_DA_CT_L_5o,
            "template_name": "normal_l5_{}.{}"
        },
        "l10": {
            "label_filepath": config.LABEL_MRCNN_L10,
            "dataset_path": config.DATASET_DA_CT_L_10o,
            "template_name": "normal_l10_{}.{}"
        },
        "r5": {
            "label_filepath": config.LABEL_MRCNN_R5,
            "dataset_path": config.DATASET_DA_CT_R_5o,
            "template_name": "normal_r5_{}.{}"
        },
        "r10": {
            "label_filepath": config.LABEL_MRCNN_R10,
            "dataset_path": config.DATASET_DA_CT_R_10o,
            "template_name": "normal_r10_{}.{}"
        },
    },
    "mirror": {
        "0": {
            "label_filepath": config.LABEL_MRCNN_M,
            "dataset_path": config.DATASET_DA_M_CT_RS,
            "template_name": "mirror_{}.{}"
        },
        "l5": {
            "label_filepath": config.LABEL_MRCNN_M_L5,
            "dataset_path": config.DATASET_DA_M_CT_L_5o,
            "template_name": "mirror_l5_{}.{}"
        },
        "l10": {
            "label_filepath": config.LABEL_MRCNN_M_L10,
            "dataset_path": config.DATASET_DA_M_CT_L_10o,
            "template_name": "mirror_l10_{}.{}"
        },
        "r5": {
            "label_filepath": config.LABEL_MRCNN_M_R5,
            "dataset_path": config.DATASET_DA_M_CT_R_5o,
            "template_name": "mirror_r5_{}.{}"
        },
        "r10": {
            "label_filepath": config.LABEL_MRCNN_M_R10,
            "dataset_path": config.DATASET_DA_M_CT_R_10o,
            "template_name": "mirror_r10_{}.{}"
        }
    }
}


class KFold:
    def __init__(self, output_dir, fold_arr=None):
        # 創造存放資料夾
        if fold_arr is None:
            fold_arr = ["A", "B", "C", "D", "E"]

        print("Fold code: {}".format(fold_arr))

        if output_dir is None:
            output_dir = config.LOGS_DIR

        print("Output pathname: {}".format(output_dir))

        self.output_dir = output_dir
        self.fold_arr = fold_arr
        self.index = 0
        self.dict_array = []
        self.copy_dict = dict()
        self.__check_dir()

        print("Initial Dict Array")
        for idx in range(len(fold_arr)):
            self.dict_array.append(dict())

    def next(self, data, old_filename, new_basename):
        self.dict_array[self.index].update(data)
        self.copy_dict[os.path.join(self.output_dir, self.fold_arr[self.index], new_basename)] = old_filename
        self.__increase()

    def __check_dir(self):
        print("Check output dir")
        for idx in self.fold_arr:
            check_path = os.path.join(self.output_dir, idx)
            need_create = False
            if os.path.exists(check_path):
                if os.path.isfile(check_path):
                    os.remove(check_path)
                    need_create = True
            else:
                need_create = True

            if need_create:
                print("Generate dir path: {}".format(check_path))
                pathlib.Path(check_path).mkdir(parents=True, exist_ok=True)
        print("Checked Success!")

    def __increase(self) -> int:
        prev_index = self.index
        self.index += 1
        if self.index >= len(self.fold_arr):
            self.index = 0

        return prev_index

    def export_json(self):
        print("Start export all json data")
        for idx in range(len(self.fold_arr)):
            json_filename = os.path.join(self.output_dir, self.fold_arr[idx], "via_region_data.json")
            print("Process id: {}, filename: {}".format(idx, json_filename))
            with open(json_filename, "w+") as json_file:
                json.dump(self.dict_array[idx], json_file)
        print("Export success!")

    def copy_images(self):
        print("Start copy image")
        for new in self.copy_dict:
            new_path = os.path.abspath(new)
            old_path = os.path.abspath(self.copy_dict[new_path])
            print("Processing:")
            print("    - old: {}".format(old_path))
            print("    - new: {}".format(new_path))
            shutil.copy(old_path, new_path)
        print("image success!")


def main():
    print("K-Fold Grouping")
    k_fold = KFold(OUTPUT_DIR)
    extension = ".jpg"
    print("Set the extension name: .jpg")

    print("Start Grouping")
    for image_type in LABEL_DICT:
        for index in LABEL_DICT[image_type]:
            target = LABEL_DICT[image_type][index]
            print(type(target))
            print(target)
            label_filepath, dataset_path, template_name = target["label_filepath"], target["dataset_path"], target[
                "template_name"]
            print("Grouping:")
            print("    - label: {}".format(label_filepath))
            print("    - dataset: {}".format(dataset_path))
            print("    - template: {}".format(template_name))
            with open(label_filepath, "r") as json_file:
                old_json_data = json.load(json_file)
                for old_key in old_json_data:
                    old_key_split = old_key.split(".")
                    old_filename = os.path.join(dataset_path, old_key_split[0] + extension)
                    new_key = template_name.format(old_key_split[0], old_key_split[1])
                    new_basename = new_key[:new_key.find(extension) + len(extension)]
                    new_json_data = dict()
                    new_json_data[new_key] = old_json_data[old_key]
                    k_fold.next(new_json_data, old_filename, new_basename)

            print("Grouping Done! --> Next...")

    k_fold.export_json()
    k_fold.copy_images()
    print("All Done!!")


if __name__ == '__main__':
    main()
