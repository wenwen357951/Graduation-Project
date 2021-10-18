import os
from datetime import datetime
from argparser import args
import settings
import sys

sys.path.append("../../../")
from docs import config as docs

#######################
#   匯入 Mask R-CNN  #
####################

# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append(docs.MODULES_DIR)
# noinspection PyUnresolvedReferences
from mrcnn import model as model_lib, utils


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

    if args.command == "train":
        config = settings.TrainingConfig()
    else:
        config = settings.InferenceConfig()

    # # 顯示配置檔案
    config.display()

    #######################
    #   創建訓練模型       #
    ####################
    if args.command == "train":
        model = model_lib.MaskRCNN(
            mode="training",
            config=config,
            model_dir=args.logs
        )
    else:
        model = model_lib.MaskRCNN(
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
        weights_path = model.find_last()
    elif args.weights.lower() == "imagenet":
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    # 載入權重檔案
    print("Loading weights ", weights_path)
    if args.weights.lower() == "coco":
        model.load_weights(
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
        model.load_weights(
            weights_path,
            by_name=True
        )

    # 進行訓練或是偵測辨識
    if args.command == "train":
        train(model)
    elif args.command == "detect":
        detect_and_color_splash(
            model,
            image_path=args.image,
            video_path=args.video
        )
    else:
        print("'{}' 無法識別"
              "請使用 'train' 或是 'detect'".format(args.command))
