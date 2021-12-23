import os.path

from argparser import args
import numpy as np
import sys
import json
import settings

#######################
#   匯入 Mask R-CNN  #
####################
# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append("../../../")
from modules.mrcnn import model as model_lib, visualize
from dataset import PeritonealDataset


def computed_overlap_set(gt_masks, pr_masks):
    # If either set of masks is empty return empty result
    if gt_masks.shape[-1] == 0 or pr_masks.shape[-1] == 0:
        return np.zeros((gt_masks.shape[-1], pr_masks.shape[-1]))
    # flatten masks and compute their areas
    gt_masks = np.reshape(gt_masks > .5, (-1, gt_masks.shape[-1])).astype(np.float32)
    pr_masks = np.reshape(pr_masks > .5, (-1, pr_masks.shape[-1])).astype(np.float32)

    gt_area = np.sum(gt_masks, axis=0)
    pr_area = np.sum(pr_masks, axis=0)

    # intersections and union
    intersections = np.dot(gt_masks.T, pr_masks)
    gt_difference = gt_area[:, None] - intersections
    pr_difference = pr_area[None, :] - intersections
    union = gt_area[:, None] + pr_area[None, :] - intersections
    return gt_difference, pr_difference, intersections, union


def computed_iou(dataset_path):
    dataset_val = PeritonealDataset()
    dataset_val.load_via(dataset_path, "val")
    dataset_val.prepare()

    json_data = dict()

    gt_classes_total_area = [0] * len(settings.CLASSES)
    for image_id in dataset_val.image_ids:
        image, image_meta, gt_class_ids, gt_bbox, gt_mask = model_lib.load_image_gt(dataset_val, CONFIG, image_id)
        gt_area = [np.sum(gt_mask[:, :, idx]) for idx in range(len(gt_class_ids))]

        for idx, area in zip(gt_class_ids, gt_area):
            gt_classes_total_area[int(idx)] += int(area)

        r = MODEL.detect([image], verbose=settings.DEBUG_MODE)[0]
        pr_masks = r["masks"]
        pr_class_ids = r["class_ids"]

        gt_diff_list, pr_diff_list, intersections, union = computed_overlap_set(gt_mask, pr_masks)
        overlaps = intersections / union

        intersection_idx = [np.argmax(intersection) for intersection in intersections]
        intersection_area = [np.max(intersection) for intersection in intersections]
        intersection_class_idx = [pr_class_ids[idx] for idx in intersection_idx]
        overlaps_iou = [np.max(overlap) for overlap in overlaps]

        gt_area = [gt_diff[intersection_idx[idx]] for idx, gt_diff in enumerate(gt_diff_list)]
        pr_area = [pr_diff[intersection_idx[idx]] for idx, pr_diff in enumerate(pr_diff_list)]

        image_name = dataset_val.image_info[image_id]["id"]
        json_data[image_name] = {}
        for idx, gt_class_id in enumerate(gt_class_ids):
            json_data[image_name][idx] = {}
            json_data[image_name][idx]["gt_class_id"] = int(gt_class_id)
            json_data[image_name][idx]["pr_class_id"] = int(intersection_class_idx[idx])
            json_data[image_name][idx]["iou"] = str(overlaps_iou[idx])
            json_data[image_name][idx]["intersection"] = int(intersection_area[idx])
            json_data[image_name][idx]["gt_difference"] = int(gt_area[idx])
            json_data[image_name][idx]["pr_difference"] = int(pr_area[idx])

    gt_classes_total_area.insert(0, 0)  # Insert Background
    json_data["gt_total_area"] = gt_classes_total_area
    with open(os.path.join(args.logs, args.name + ".json"), "w+", encoding="utf-8") as json_file:
        json.dump(json_data, json_file)


if __name__ == '__main__':
    print("運行環境參數配置: {}".format(args))
    print("----------")
    print("名稱:", args.name)
    print("資料集路徑:", args.dataset)
    print("權重檔案:", args.weights)
    print("日誌資料夾:", args.logs)

    #######################
    #   推理模型配置       #
    ####################
    print("載入訓練模型配置: ")
    print("  - 推理配置 (Inference)")
    settings.RECOGNIZABLE_NAME = args.name
    CONFIG = settings.InferenceConfig()
    CONFIG.NAME = settings.RECOGNIZABLE_NAME
    # # 顯示配置檔案
    print("顯示配置設定")
    CONFIG.display()

    #######################
    #   創建推理模型       #
    ####################
    MODEL = model_lib.MaskRCNN(
        mode="inference",
        config=CONFIG,
        model_dir=args.logs
    )

    #######################
    #   載入權重檔案       #
    ####################
    # 選擇需加載的權重檔案
    if args.weights.lower() == "last":
        # 找到上一次訓練的權重檔案
        WEIGHTS_PATH = MODEL.find_last()
    else:
        WEIGHTS_PATH = args.weights

    # 載入權重檔案
    print("載入權重檔案 ", WEIGHTS_PATH)
    MODEL.load_weights(
        WEIGHTS_PATH,
        by_name=True
    )

    # 進行訓練或是偵測辨識
    computed_iou(args.dataset)
