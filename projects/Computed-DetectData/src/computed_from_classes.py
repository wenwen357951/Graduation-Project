import glob
import os
from argparser import args
import numpy as np
import sys
import json
import settings

#######################
#   匯入 TRCLAB LIB  #
####################
sys.path.append("../../../")


class ImageDetectData:
    def __init__(self, json_section):
        self.detect_num = len(json_section)
        self.iou_list = []
        self.gt_classes = []
        self.pr_classes = []
        self.intersections = []
        self.gt_difference = []
        self.pr_difference = []
        for idx in range(self.detect_num):
            section = json_section[str(idx)]
            self.iou_list.append(float(section["iou"]))
            self.gt_classes.append(section["gt_class_id"])
            self.pr_classes.append(section["pr_class_id"])
            self.intersections.append(section["intersection"])
            self.gt_difference.append(section["gt_difference"])
            self.pr_difference.append(section["pr_difference"])

    def calc_classes_total_area(self):
        result = dict()
        result["gt"] = [0] * len(settings.CLASS_LIST_WITH_BG)
        result["pr"] = [0] * len(settings.CLASS_LIST_WITH_BG)
        for idx, (gt, pr) in enumerate(zip(self.gt_classes, self.pr_classes)):
            class_id = gt
            result["gt"][class_id] += self.gt_difference[idx] + self.intersections[idx]
            if gt == pr:
                result["pr"][class_id] += self.pr_difference[idx] + self.intersections[idx]

        return result


def computed_from_classes(json_folder):
    json_files = glob.glob(os.path.join(json_folder, "*.json"))

    total_gt = np.array([0] * len(settings.CLASS_LIST_WITH_BG))
    total_pr = total_gt.copy()
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as json_stream:
            json_data = json.load(json_stream)

        area_list = []
        for image_name in json_data:
            area_list.append(ImageDetectData(json_data[image_name]).calc_classes_total_area())

        for area in area_list:
            total_gt += np.array(area["gt"])
            total_pr += np.array(area["pr"])

    result = "classes,gt_area,pr_area\n"
    for idx, name in enumerate(settings.CLASS_LIST_WITH_BG):
        result += "{},{},{}\n".format(name, total_gt[idx], total_pr[idx])

    return result


if __name__ == '__main__':
    print("運行環境參數配置: {}".format(args))
    print("----------")
    print("JSON檔案的路徑:", args.jsondir)
    print("日誌資料夾:", args.logs)

    assert os.path.exists(args.jsondir), FileNotFoundError("JSON folder not found!")

    output_csv = computed_from_classes(args.jsondir)

    with open(os.path.join(args.logs, os.path.basename(args.jsondir) + ".csv"), "w+", encoding="utf-8") as csv_file:
        csv_file.write(output_csv)
