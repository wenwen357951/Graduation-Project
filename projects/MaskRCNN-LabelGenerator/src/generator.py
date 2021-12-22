from argparser import args
import os
import sys

sys.path.append("../../../")
from modules.trclab import vhp

if __name__ == '__main__':
    # 讀取標籤
    vhp_label = vhp.OrganLabel(args.label)
    # 讀入資料集
    seg_dataset = vhp.OrganDataset(args.segmentation, "*.bmp")
    # 設置標籤
    seg_dataset.set_label(vhp_label)
    # 匯出標記區域根據目標圖片(映射圖片)至輸出位置
    seg_dataset.export_label_area(args.target, "*.jpg", os.path.join(args.logs, args.output))
