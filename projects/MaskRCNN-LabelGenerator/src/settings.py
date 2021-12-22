import os
import sys

sys.path.append("../../../")
from modules.trclab import config as docs

DEFAULT_LOGS_DIR = os.path.join(docs.LOGS_DIR, "MaskRCNN-LabelGenerator")
docs.create_folder_if_not_exists(DEFAULT_LOGS_DIR)
