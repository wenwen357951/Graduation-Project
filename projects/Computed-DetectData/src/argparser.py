import argparse
import settings

parser = argparse.ArgumentParser(
    description="計算 Mask R-CNN 模型辨識輸出數據檔案",
    add_help=True,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '--jsondir',
    required=True,
    metavar="/path/to/your/jsonfile/dir",
    help="辨識輸出資料數據檔案的路徑"
)

parser.add_argument(
    '--logs',
    required=False,
    default=settings.DEFAULT_LOGS_DIR,
    metavar="輸出日誌的路徑"
)

args = parser.parse_args()
