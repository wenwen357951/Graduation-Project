import os
import sys

sys.path.append("../../../docs")
import config

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append(config.MODULES_DIR)
# noinspection PyUnresolvedReferences
from mrcnn.config import Config

####################
#   訓練模型配置
####################

# 可識別名稱
RECOGNIZABLE_NAME = "Peritoneal"
# GPU 可容納圖片數
# 如果顯示卡記憶體容量12GB，可以剛好使用兩張圖片
IMAGES_PER_GPU = 4
# 訓練的類別數量 (需要包含背景)
# 背景 + 需識別類型數量
NUM_CLASSES = 1 + 1
# 每個迭代的訓練次數
STEPS_PER_EPOCH = 100
# 跳過自信度 < 90% 的偵測辨識
DETECTION_MIN_CONFIDENCE = 0.9


# 訓練配置
class TrainingConfig(Config):
    NAME = RECOGNIZABLE_NAME
    IMAGES_PER_GPU = IMAGES_PER_GPU
    NUM_CLASSES = NUM_CLASSES
    STEPS_PER_EPOCH = STEPS_PER_EPOCH
    DETECTION_MIN_CONFIDENCE = DETECTION_MIN_CONFIDENCE


# 辨識偵測配置
class InferenceConfig(TrainingConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
