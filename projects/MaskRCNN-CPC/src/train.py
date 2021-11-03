import os
from datetime import datetime
from argparser import args
import settings
import sys

#######################
#   匯入 Mask R-CNN  #
####################
# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append("../../../modules")
from modules.trclab import config
from mrcnn import model as model_lib, utils

from dataset import CPCDataset


def train(model):
    dataset_train = CPCDataset()


def color_splash(image, mask):
    pass


if __name__ == '__main__':
    # Record the start time
    START_TIME = datetime.now()
    print("程序開始運行: {}".format(START_TIME))
    print("運行環境參數配置: {}".format(args))

    if args.command == "train":
        assert args.dataset, "訓練時需要參數 '--dataset'"
    elif args.command == "detect":
        assert args.image or args.video, "偵測時需要提供資料來源參數 '--image' or '--video'"

    print("----------")
    print("權重檔案:", args.weights)
    print("輸入資料集:", args.dataset)
    print("日誌資料夾:", args.logs)

    #######################
    #   訓練模型配置       #
    ####################
    print("載入訓練模型配置: ")
    if args.command == "train":
        print("  - 訓練配置 (Training)")
        config = settings.TrainingConfig()
    else:
        print("  - 推論配置 (Inference)")
        config = settings.InferenceConfig()

    # # 顯示配置檔案
    print("顯示配置設定")
    config.display()

    #######################
    #   創建訓練模型       #
    ####################
    if args.command == "train":
        MODEL = model_lib.MaskRCNN(
            mode="training",
            config=config,
            model_dir=args.logs
        )
    else:
        MODEL = model_lib.MaskRCNN(
            mode="inference",
            config=config,
            model_dir=args.logs
        )

    #######################
    #   載入權重檔案       #
    ####################

    # 選擇需加載的權重檔案
    if args.weights.lower() == "coco":
        weights_path = settings.COCO_WEIGHTS_PATH
        # 如果找不到檔案，就下載權重檔案
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)

    elif args.weights.lower() == "last":
        # 找到上一次訓練的權重檔案
        weights_path = MODEL.find_last()
    elif args.weights.lower() == "imagenet":
        weights_path = MODEL.get_imagenet_weights()
    else:
        weights_path = args.weights

    # 載入權重檔案
    print("Loading weights ", weights_path)
    if args.weights.lower() == "coco":
        MODEL.load_weights(
            weights_path,
            by_name=True,
            exclude=[
                "mrcnn_class_logits",
                "mrcnn_bbox_fc",
                "mrcnn_bbox",
                "mrcnn_mask"
            ]
        )
    else:
        MODEL.load_weights(
            weights_path,
            by_name=True
        )

    # 進行訓練或是偵測辨識
    if args.command == "train":
        train(MODEL)
    elif args.command == "detect":
        detect_and_color_splash(
            MODEL,
            image_path=args.image,
            video_path=args.video
        )
    else:
        print("'{}' 無法識別"
              "請使用 'train' 或是 'detect'".format(args.command))
