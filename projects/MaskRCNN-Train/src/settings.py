import os
import sys

# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append("../../../")
from modules.trclab import config as docs
from modules.mrcnn.config import Config

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_LOGS_DIR = os.path.join(docs.LOGS_DIR, "MaskRCNN-Train")
docs.create_folder_if_not_exists(DEFAULT_LOGS_DIR)
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")


####################
#   訓練模型配置
####################
# GPU 可容納圖片數
# 如果顯示卡記憶體容量12GB，可以剛好使用兩張圖片
IMAGES_PER_GPU = 4
# 訓練的類別數量 (需要包含背景)
# 背景 + 需識別類型數量
CLASSES_TXT = os.path.join(docs.RESOURCES_KFOLD_DIR, "peritoneal_cavity_without_color.txt")
# 每個迭代的訓練次數
EPOCH = 1000
STEPS_PER_EPOCH = 100
# 跳過自信度 < 90% 的偵測辨識
DETECTION_MIN_CONFIDENCE = 0.9

# # # DON'T TOUCH # # #
RECOGNIZABLE_NAME = "Peritoneal"
CLASSES = [line.strip() for line in open(CLASSES_TXT, 'r', encoding="UTF-8")]
CLASSES_NUM = len(CLASSES)
CLASS_LIST_WITH_BG = CLASSES.copy().insert(0, "BG")
#######################


####################
#   訓練配置
####################
class TrainingConfig(Config):
    NAME = RECOGNIZABLE_NAME
    IMAGES_PER_GPU = IMAGES_PER_GPU
    NUM_CLASSES = 1 + CLASSES_NUM
    STEPS_PER_EPOCH = STEPS_PER_EPOCH
    DETECTION_MIN_CONFIDENCE = DETECTION_MIN_CONFIDENCE
