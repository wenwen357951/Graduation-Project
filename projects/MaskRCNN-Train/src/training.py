from argparser import args
from datetime import datetime
import os
import sys
import settings

#######################
#   匯入 Mask R-CNN  #
####################
# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append("../../../")
from modules.mrcnn import model as model_lib, utils
from dataset import PeritonealDataset


def train(dataset_path):
    dataset_train = PeritonealDataset()
    dataset_train.load_via(dataset_path, "train")
    dataset_train.prepare()

    dataset_val = PeritonealDataset()
    dataset_val.load_via(dataset_path, "val")
    dataset_val.prepare()

    print("Training network heads")
    MODEL.train(dataset_train, dataset_val,
                learning_rate=CONFIG.LEARNING_RATE,
                epochs=settings.EPOCH,
                layers='heads')


if __name__ == '__main__':
    print("運行環境參數配置: {}".format(args))
    print("----------")
    print("名稱:", args.name)
    print("資料集路徑:", args.dataset)
    print("權重檔案:", args.weights)
    print("日誌資料夾:", args.logs)

    #######################
    #   訓練模型配置       #
    ####################
    print("載入訓練模型配置: ")
    print("  - 訓練配置 (Training)")
    settings.RECOGNIZABLE_NAME = args.name
    CONFIG = settings.TrainingConfig()
    CONFIG.NAME = settings.RECOGNIZABLE_NAME
    # # 顯示配置檔案
    print("顯示配置設定")
    CONFIG.display()

    #######################
    #   創建訓練模型       #
    ####################
    MODEL = model_lib.MaskRCNN(
        mode="training",
        config=CONFIG,
        model_dir=args.logs
    )

    #######################
    #   載入權重檔案       #
    ####################
    # 選擇需加載的權重檔案
    if args.weights.lower() == "coco":
        WEIGHTS_PATH = settings.COCO_WEIGHTS_PATH
        # 如果找不到檔案，就下載權重檔案
        if not os.path.exists(WEIGHTS_PATH):
            utils.download_trained_weights(WEIGHTS_PATH)

    elif args.weights.lower() == "last":
        # 找到上一次訓練的權重檔案
        WEIGHTS_PATH = MODEL.find_last()
    elif args.weights.lower() == "imagenet":
        WEIGHTS_PATH = MODEL.get_imagenet_weights()
    else:
        WEIGHTS_PATH = args.weights

    # 載入權重檔案
    print("載入權重檔案 ", WEIGHTS_PATH)
    if args.weights.lower() == "coco":
        MODEL.load_weights(
            WEIGHTS_PATH,
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
            WEIGHTS_PATH,
            by_name=True
        )

    # 進行訓練或是偵測辨識
    train(args.dataset)
