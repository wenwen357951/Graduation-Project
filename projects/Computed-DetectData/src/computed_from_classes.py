import glob
import os
from argparser import args
import numpy as np
import sys
import json
import settings

np.seterr(divide='ignore', invalid='ignore')

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
            self.intersections.append(section["intersection"])  # TP
            self.gt_difference.append(section["gt_difference"])  # FN
            self.pr_difference.append(section["pr_difference"])  # FP

        self.intersections = np.array(self.intersections)
        self.gt_difference = np.array(self.gt_difference)
        self.pr_difference = np.array(self.pr_difference)

    def get_pr_tp_area(self):
        result = [0] * len(settings.CLASS_LIST_WITH_BG)
        for idx, (gt, pr) in enumerate(zip(self.gt_classes, self.pr_classes)):
            if gt == pr:
                result[gt] += self.pr_difference[idx] + self.intersections[idx]

        return result


def computed_from_classes(json_folder):
    json_files = glob.glob(os.path.join(json_folder, "*.json"))

    total_gt = np.array([0] * len(settings.CLASS_LIST_WITH_BG))
    total_pr = np.array([0] * len(settings.CLASS_LIST_WITH_BG))
    for json_file in json_files:
        with open(json_file, "r", encoding="utf-8") as json_stream:
            json_data = json.load(json_stream)

        for image_name in json_data:
            if image_name == "gt_total_area":
                continue

            img_detect_data = ImageDetectData(json_data[image_name])
            total_pr += np.array(img_detect_data.get_pr_tp_area())

        total_gt += np.array(json_data["gt_total_area"])

    result = "classes,gt_area,pr_area\n"
    for idx, name in enumerate(settings.CLASS_LIST_WITH_BG):
        result += "{},{},{}\n" \
            .format(name, total_gt[idx], total_pr[idx])

    return result


def computed_iou(json_folder):
    from_classes = dict()
    for idx in range(len(settings.CLASS_LIST_WITH_BG)):
        from_classes[str(idx)] = {}
        from_classes[str(idx)]["intersection"] = []
        from_classes[str(idx)]["pr_difference"] = []
        from_classes[str(idx)]["gt_difference"] = []

    for json_file in glob.glob(os.path.join(json_folder, "*.json")):
        with open(json_file, "r", encoding="utf-8") as json_stream:
            json_data = json.load(json_stream)

        for key in json_data:
            if key == "gt_total_area":
                continue

            for area_idx in json_data[key]:
                pr_id = json_data[key][area_idx]["gt_class_id"]
                gt_id = json_data[key][area_idx]["pr_class_id"]
                if pr_id != gt_id:
                    continue

                from_classes[str(gt_id)]["intersection"].append(json_data[key][area_idx]["intersection"])
                from_classes[str(gt_id)]["pr_difference"].append(json_data[key][area_idx]["pr_difference"])
                from_classes[str(gt_id)]["gt_difference"].append(json_data[key][area_idx]["gt_difference"])

    iou_list = [0] * len(settings.CLASS_LIST_WITH_BG)
    dice = [0] * len(settings.CLASS_LIST_WITH_BG)
    recall = [0] * len(settings.CLASS_LIST_WITH_BG)
    precision = [0] * len(settings.CLASS_LIST_WITH_BG)
    for idx in from_classes:
        tp = np.sum(from_classes[idx]["intersection"])
        fp = np.sum(from_classes[idx]["pr_difference"])
        fn = np.sum(from_classes[idx]["gt_difference"])

        iou_list[int(idx)] = tp / (tp + fp + fn)
        dice[int(idx)] = (2 * tp) / ((tp + fn) + (tp + fp))
        recall[int(idx)] = tp / (tp + fn)
        precision[int(idx)] = tp / (tp + fp)

    iou_l = np.nan_to_num(iou_list)
    dice_l = np.nan_to_num(dice)
    recall_l = np.nan_to_num(recall)
    precision_l = np.nan_to_num(precision)
    result = "class,iou,dice,recall,precision\n"
    for idx, name in enumerate(settings.CLASS_LIST_WITH_BG):
        result += "{},{},{},{},{}\n".format(name, iou_l[idx], dice_l[idx], recall_l[idx], precision_l[idx])

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

    output_csv = computed_iou(args.jsondir)
    with open(os.path.join(args.logs, os.path.basename(args.jsondir) + "_iou.csv"), "w+", encoding="utf-8") as csv_file:
        csv_file.write(output_csv)
