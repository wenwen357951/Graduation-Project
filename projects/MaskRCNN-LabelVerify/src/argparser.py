import argparse

parser = argparse.ArgumentParser(
    description="驗證 Mask-RCNN 訓練用的標記檔案(JSON)",
    add_help=True,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '--dataset',
    required=True,
    metavar="/path/to/your/dataset",
    help="資料集的路徑"
)

args = parser.parse_args()
