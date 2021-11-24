import argparse

import settings

parser = argparse.ArgumentParser(
    description="訓練 Mask R-CNN 來偵測辨識腹腔器官",
    add_help=True,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    "command",
    metavar="<command>",
    help="'train' 或是 'detect'"
)

parser.add_argument(
    '--dataset',
    required=False,
    metavar="/docs/to/your/dataset/",
    help="資料集的資料集路徑"
)

parser.add_argument(
    '--weights',
    required=True,
    metavar="/docs/to/weights.h5/",
    help="權重檔案(.h5)的路徑或 'coco'"
)

parser.add_argument(
    '--logs',
    required=False,
    default=settings.DEFAULT_LOGS_DIR,
    metavar="輸出日誌的路徑"
)

parser.add_argument(
    '--image',
    required=False,
    metavar="放入需要偵測辨識的圖片路徑"
)

parser.add_argument(
    '--video',
    required=False,
    metavar="放入需要偵測辨識的影片路徑"
)

args = parser.parse_args()

