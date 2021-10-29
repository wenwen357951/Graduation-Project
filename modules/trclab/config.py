import os

ROOT_DIR = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))

# Assets Dir
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

# # Assets VHP Dir
ASSETS_VHP_DIR = os.path.join(ASSETS_DIR, "vhp")
DATASET_VHP_SEG = os.path.join(ASSETS_VHP_DIR, "(VKH) Segmented Images (1000 X 570)")
DATASET_VHP_CT_RESIZE = os.path.join(ASSETS_VHP_DIR, "(VKH) CT Images Resize (1000 X 570)")

# # Assets Alignment Dir
ASSETS_ALIGNMENT_DIR = os.path.join(ASSETS_DIR, "alignment")
DATASET_ALIGNMENT_CT = os.path.join(ASSETS_ALIGNMENT_DIR, "CT Image (494 x 281)")
DATASET_ALIGNMENT_CT_RESIZE = os.path.join(ASSETS_ALIGNMENT_DIR, "CT Image Resize (1000 x 570)")

# # Assets Data Augmentation Dir
ASSETS_DA_DIR = os.path.join(ASSETS_DIR, "data-augmentation")
# # # Normal
ASSETS_DA_NORMAL_DIR = os.path.join(ASSETS_DA_DIR, "Normal")
# # # # CT
ASSETS_DA_CT_DIR = os.path.join(ASSETS_DA_NORMAL_DIR, "CT")
# # # # # CT L
ASSETS_DA_CT_L_DIR = os.path.join(ASSETS_DA_CT_DIR, "Left")
DATASET_DA_CT_L_5o = os.path.join(ASSETS_DA_CT_L_DIR, "CT Left 5Degree (1000 x 570)")
DATASET_DA_CT_L_10o = os.path.join(ASSETS_DA_CT_L_DIR, "CT Left 10Degree (1000 x 570)")
# # # # # CT R
ASSETS_DA_CT_R_DIR = os.path.join(ASSETS_DA_CT_DIR, "Right")
DATASET_DA_CT_R_5o = os.path.join(ASSETS_DA_CT_R_DIR, "CT Right 5Degree (1000 x 570)")
DATASET_DA_CT_R_10o = os.path.join(ASSETS_DA_CT_R_DIR, "CT Right 10Degree (1000 x 570)")
# # # # SEG
ASSETS_DA_SEG_DIR = os.path.join(ASSETS_DA_NORMAL_DIR, "SEG")
# # # # # SEG L
ASSETS_DA_SEG_L_DIR = os.path.join(ASSETS_DA_SEG_DIR, "Left")
DATASET_DA_SEG_L_5o = os.path.join(ASSETS_DA_SEG_L_DIR, "SEG Left 5Degree (1000 X 570)")
DATASET_DA_SEG_L_10o = os.path.join(ASSETS_DA_SEG_L_DIR, "SEG Left 10Degree (1000 X 570)")
# # # # # SEG R
ASSETS_DA_SEG_R_DIR = os.path.join(ASSETS_DA_SEG_DIR, "Right")
DATASET_DA_SEG_R_5o = os.path.join(ASSETS_DA_SEG_R_DIR, "SEG Right 5Degree (1000 X 570)")
DATASET_DA_SEG_R_10o = os.path.join(ASSETS_DA_SEG_R_DIR, "SEG Right 10Degree (1000 X 570)")
# # # Mirror
ASSETS_DA_M_DIR = os.path.join(ASSETS_DA_DIR, "Mirror")
# # # # CT
ASSETS_DA_M_CT_DIR = os.path.join(ASSETS_DA_M_DIR, "CT")
DATASET_DA_M_CT_RS = os.path.join(ASSETS_DA_M_CT_DIR, "CT Resize Mirror (1000 x 570)")
# # # # # CT L
ASSETS_DA_M_CT_L_DIR = os.path.join(ASSETS_DA_M_CT_DIR, "Left")
DATASET_DA_M_CT_L_5o = os.path.join(ASSETS_DA_M_CT_L_DIR, "CT Resize Mirror Left 5Degree (1000 x 570)")
DATASET_DA_M_CT_L_10o = os.path.join(ASSETS_DA_M_CT_L_DIR, "CT Resize Mirror Left 10Degree (1000 x 570)")
# # # # # CT R
ASSETS_DA_M_CT_R_DIR = os.path.join(ASSETS_DA_M_CT_DIR, "Right")
DATASET_DA_M_CT_R_5o = os.path.join(ASSETS_DA_M_CT_R_DIR, "CT Resize Mirror Right 5Degree (1000 x 570)")
DATASET_DA_M_CT_R_10o = os.path.join(ASSETS_DA_M_CT_R_DIR, "CT Resize Mirror Right 10Degree (1000 x 570)")
# # # # SEG
ASSETS_DA_M_SEG_DIR = os.path.join(ASSETS_DA_M_DIR, "SEG")
DATASET_DA_M_SEG = os.path.join(ASSETS_DA_M_SEG_DIR, "SEG Mirror (1000 X 570)")
# # # # # SEG L
ASSETS_DA_M_SEG_L_DIR = os.path.join(ASSETS_DA_M_SEG_DIR, "Left")
DATASET_DA_M_SEG_L_5o = os.path.join(ASSETS_DA_M_SEG_L_DIR, "SEG Mirror Left 5Degree (1000 X 570)")
DATASET_DA_M_SEG_L_10o = os.path.join(ASSETS_DA_M_SEG_L_DIR, "SEG Mirror Left 10Degree (1000 X 570)")
# # # # # SEG R
ASSETS_DA_M_SEG_R_DIR = os.path.join(ASSETS_DA_M_SEG_DIR, "Right")
DATASET_DA_M_SEG_R_5o = os.path.join(ASSETS_DA_M_SEG_R_DIR, "SEG Mirror Right 5Degree (1000 X 570)")
DATASET_DA_M_SEG_R_10o = os.path.join(ASSETS_DA_M_SEG_R_DIR, "SEG Mirror Right 10Degree (1000 x 570)")

# # Modules
MODULES_DIR = os.path.join(ROOT_DIR, "modules")

# # Projects
PROJECTS_DIR = os.path.join(ROOT_DIR, "projects")
# # # Label Generate
PROJECTS_LG_DIR = os.path.join(PROJECTS_DIR, "LabelGenerate")

# Logs
LOGS_DIR = os.path.join(ROOT_DIR, "logs")

# Resources
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
LABEL_MRCNN_DIR = os.path.join(RESOURCES_DIR, "VHP_MRCNN_LABEL")
LABEL_MRCNN_M = os.path.join(LABEL_MRCNN_DIR, "mirror.json")
LABEL_MRCNN_M_L5 = os.path.join(LABEL_MRCNN_DIR, "mirror_l5.json")
LABEL_MRCNN_M_L10 = os.path.join(LABEL_MRCNN_DIR, "mirror_l10.json")
LABEL_MRCNN_M_R5 = os.path.join(LABEL_MRCNN_DIR, "mirror_r5.json")
LABEL_MRCNN_M_R10 = os.path.join(LABEL_MRCNN_DIR, "mirror_r10.json")
LABEL_MRCNN = os.path.join(LABEL_MRCNN_DIR, "normal.json")
LABEL_MRCNN_L5 = os.path.join(LABEL_MRCNN_DIR, "normal_l5.json")
LABEL_MRCNN_L10 = os.path.join(LABEL_MRCNN_DIR, "normal_l10.json")
LABEL_MRCNN_R5 = os.path.join(LABEL_MRCNN_DIR, "normal_r5.json")
LABEL_MRCNN_R10 = os.path.join(LABEL_MRCNN_DIR, "normal_r10.json")

# # TrainingDataset
RESOURCES_ACP_DIR = os.path.join(RESOURCES_DIR, "TrainingDataset")
ACP_DATASET = os.path.join(RESOURCES_ACP_DIR, "dataset")
ACP_LABEL_DIR = os.path.join(RESOURCES_ACP_DIR, "label")
