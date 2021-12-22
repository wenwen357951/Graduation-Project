import skimage.io

from argparser import args
import os
import glob
import settings
import sys
import json

#######################
#   匯入 Mask R-CNN  #
####################
# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append("../../../")
from modules.mrcnn import model as model_lib, visualize
from modules.trclab import config as docs


def splash():
    output_folder = os.path.join(args.logs, CONFIG.NAME)
    docs.create_folder_if_not_exists(output_folder)
    json_data = dict()
    for image_path in sorted(glob.glob(os.path.join(args.images, "*.jpg"))):
        image = skimage.io.imread(image_path)
        r = MODEL.detect([image], verbose=settings.DEBUG_MODE)[0]
        bbox = r["rois"]
        masks = r["masks"]
        class_ids = r["class_ids"]
        scores = r["scores"]

        file_basename = os.path.basename(image_path)
        visualize.display_instances(
            image, bbox, masks, class_ids,
            settings.CLASS_LIST_WITH_BG, scores,
            output_filepath=os.path.join(output_folder, file_basename))

        json_data[file_basename] = {}
        json_data[file_basename]["scores"] = {}
        json_data[file_basename]["classes"] = {}

        for idx, score in enumerate(scores):
            json_data[file_basename]["scores"][idx] = str(score)
            json_data[file_basename]["classes"][idx] = settings.CLASS_LIST_WITH_BG[class_ids[idx]]

        with open(os.path.join(output_folder, "model_acc.json"), "w+", encoding="utf-8") as json_file:
            json.dump(json_data, json_file)


if __name__ == '__main__':
    print("運行環境參數配置: {}".format(args))
    print("----------")
    print("可辨識名稱:", args.name)
    print("輸入資料集:", args.images)
    print("輸入權重檔案:", args.weights)
    print("日誌資料夾:", args.logs)

    #######################
    #   推理模型配置       #
    ####################
    print("載入訓練模型配置: ")
    print("  - 推理配置 (Inference)")
    CONFIG = settings.InferenceConfig()
    CONFIG.NAME = args.name
    # # 顯示配置檔案
    print("顯示配置設定")
    CONFIG.display()

    #######################
    #   創建推理模型       #
    ####################
    MODEL = model_lib.MaskRCNN(
        mode="inference",
        config=CONFIG,
        model_dir=args.weights
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

    splash()
