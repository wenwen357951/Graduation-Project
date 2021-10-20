import os
import sys

# Import docs config
sys.path.append("../../../docs")
# noinspection PyUnresolvedReferences
import config

# Append modules dir to system path
sys.path.append(config.MODULES_DIR)
# noinspection PyUnresolvedReferences
# Import trclab modules
import trclab.vhp as vhp

if __name__ == '__main__':
    CT_DIRS = [
        config.ASSETS_ALIGNMENT_CT_RESIZE_DIR,
        config.ASSETS_DA_M_CT_DIR,
        config.ASSETS_DA_CT_L_5o_DIR,
        config.ASSETS_DA_CT_L_10o_DIR,
        config.ASSETS_DA_CT_R_5o_DIR,
        config.ASSETS_DA_CT_R_10o_DIR,
        config.ASSETS_DA_M_CT_L_5o_DIR,
        config.ASSETS_DA_M_CT_L_10o_DIR,
        config.ASSETS_DA_M_CT_R_5o_DIR,
        config.ASSETS_DA_M_CT_R_10o_DIR
    ]
    SEG_DIRS = [
        config.ASSETS_VHP_SEG_DIR,
        config.ASSETS_DA_M_SEG_DIR,
        config.ASSETS_DA_SEG_L_5o_DIR,
        config.ASSETS_DA_SEG_L_10o_DIR,
        config.ASSETS_DA_SEG_R_5o_DIR,
        config.ASSETS_DA_SEG_R_10o_DIR,
        config.ASSETS_DA_M_SEG_L_5o_DIR,
        config.ASSETS_DA_M_SEG_L_10o_DIR,
        config.ASSETS_DA_M_SEG_R_5o_DIR,
        config.ASSETS_DA_M_SEG_R_10o_DIR
    ]
    OUTPUT_NAME = [
        "normal.json",
        "mirror.json",
        "normal_l5.json",
        "normal_l10.json",
        "normal_r5.json",
        "normal_r10.json",
        "mirror_l5.json",
        "mirror_l10.json",
        "mirror_r5.json",
        "mirror_r10.json",
    ]

    for (ct, seg, out) in zip(CT_DIRS, SEG_DIRS, OUTPUT_NAME):
        print(ct, seg, out)
        # 讀取標籤
        vhp_label = vhp.OrganLabel(os.path.join(config.ACP_LABEL_DIR, "peritoneal_cavity.txt"))
        # 讀入資料集
        seg_dataset = vhp.OrganDataset(seg, "*.bmp")
        # 設置標籤
        seg_dataset.set_label(vhp_label)
        # 匯出標記區域根據目標圖片(映射圖片)至輸出位置
        seg_dataset.export_label_area(ct, "*.jpg", os.path.join(config.LOGS_DIR, out))
