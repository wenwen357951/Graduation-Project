import argparse
import settings

parser = argparse.ArgumentParser(
    description="輸出 Mask R-CNN 偵測辨識出之資料數據",
    add_help=True,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '--name',
    required=True,
    default="Peritoneal_TEST",
    metavar="'Recognizable Name'",
    help="可辨識名稱"
)

parser.add_argument(
    '--dataset',
    required=True,
    metavar="/docs/to/your/dataset/",
    help="資料集的資料集路徑"
)

parser.add_argument(
    '--weights',
    required=True,
    metavar="/docs/to/weights.h5/",
    help="權重檔案(.h5)的路徑或 'coco' or 'imagenet'"
)

parser.add_argument(
    '--logs',
    required=False,
    default=settings.DEFAULT_LOGS_DIR,
    metavar="輸出日誌的路徑"
)

args = parser.parse_args()
