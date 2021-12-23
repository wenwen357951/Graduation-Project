import os
import sys

# 為系統添加此專案路徑，來找到 mrcnn 函式庫
sys.path.append("../../../")
from modules.trclab import config as docs

DEBUG_MODE = 1
DEFAULT_LOGS_DIR = os.path.join(docs.LOGS_DIR, "Computed_DetectData")
docs.create_folder_if_not_exists(DEFAULT_LOGS_DIR)

CLASSES_TXT = os.path.join(docs.RESOURCES_KFOLD_DIR, "peritoneal_cavity_without_color.txt")
CLASSES = [line.strip() for line in open(CLASSES_TXT, 'r', encoding="UTF-8")]
CLASS_LIST_WITH_BG = CLASSES.copy()
CLASS_LIST_WITH_BG.insert(0, "BG")
