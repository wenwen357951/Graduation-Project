import argparse
import settings

parser = argparse.ArgumentParser(
    description="生成 Mask-RCNN 訓練用的標記檔案(JSON)",
    add_help=True,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '--label',
    required=True,
    metavar="/path/to/your/color_label.txt",
    help="顏色標記文件檔案的路徑"
)

parser.add_argument(
    '--segmentation',
    required=True,
    metavar="/path/to/your/segmentation/image set/",
    help="分割圖片集的路徑"
)

parser.add_argument(
    '--target',
    required=True,
    metavar="/path/to/target/image set/",
    help="目標圖片集的路徑"
)

parser.add_argument(
    '--output',
    required=True,
    default="via_region_data.json",
    metavar="output_file_name.json",
    help="輸出檔案名稱"
)

parser.add_argument(
    '--logs',
    required=False,
    default=settings.DEFAULT_LOGS_DIR,
    metavar="輸出日誌的路徑"
)

args = parser.parse_args()
