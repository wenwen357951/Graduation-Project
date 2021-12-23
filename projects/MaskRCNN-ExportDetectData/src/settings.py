import os
import sys

# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append("../../../")
from modules.trclab import config as docs
from modules.mrcnn.config import Config

DEBUG_MODE = 1
DEFAULT_LOGS_DIR = os.path.join(docs.LOGS_DIR, "MaskRCNN-ExportDetectData")
docs.create_folder_if_not_exists(DEFAULT_LOGS_DIR)

####################
#   訓練模型配置
####################
# 訓練的類別數量 (需要包含背景)
# 背景 + 需識別類型數量
CLASSES_TXT = os.path.join(docs.RESOURCES_KFOLD_DIR, "peritoneal_cavity_without_color.txt")
# # # DON'T TOUCH # # #
RECOGNIZABLE_NAME = "Peritoneal"
CLASSES = [line.strip() for line in open(CLASSES_TXT, 'r', encoding="UTF-8")]
CLASSES_NUM = len(CLASSES)
CLASS_LIST_WITH_BG = CLASSES.copy()
CLASS_LIST_WITH_BG.insert(0, "BG")


#######################


####################
#   推理配置
####################
class InferenceConfig(Config):
    NAME = "Peritoneal"
    NUM_CLASSES = 1 + CLASSES_NUM
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    USE_MINI_MASK = False
