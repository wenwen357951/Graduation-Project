import os
import sys
import config

sys.path.append("../../../")
from docs import config as docs

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append(docs.MODULES_DIR)
# noinspection PyUnresolvedReferences
from mrcnn.config import Config


# 訓練配置
class TrainingConfig(Config):
    NAME = config.RECOGNIZABLE_NAME
    IMAGES_PER_GPU = config.IMAGES_PER_GPU
    NUM_CLASSES = config.NUM_CLASSES
    STEPS_PER_EPOCH = config.STEPS_PER_EPOCH
    DETECTION_MIN_CONFIDENCE = config.DETECTION_MIN_CONFIDENCE


# 辨識偵測配置
class InferenceConfig(TrainingConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
