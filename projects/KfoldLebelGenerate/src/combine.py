import os
import sys

sys.path.append("../../../modules")
from modules.trclab import config

OUTPUT_DIR = os.path.join(config.LOGS_DIR, "k-fold")
LABEL_PATH_DICT = {
    "A_LABEL_PATH":

        'E:/PCP-NEW/Graduation-Project/logs/k-fold/A/via_region_data.json',

    "B_LABEL_PATH":

        'E:/PCP-NEW/Graduation-Project/logs/k-fold/B/via_region_data.json',

    "C_LABEL_PATH":

        'E:/PCP-NEW/Graduation-Project/logs/k-fold/C/via_region_data.json',

    "D_LABEL_PATH":

        'E:/PCP-NEW/Graduation-Project/logs/k-fold/D/via_region_data.json',

    "E_LABEL_PATH":

        'E:/PCP-NEW/Graduation-Project/logs/k-fold/E/via_region_data.json'

}


def main():
    for path_fold in LABEL_PATH_DICT:
        target = LABEL_PATH_DICT[path_fold]



if __name__ == '__main__':
    main()
