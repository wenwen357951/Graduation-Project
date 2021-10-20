import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

# Assets Dir
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

# # Assets VHP Dir
ASSETS_VHP_DIR = os.path.join(ASSETS_DIR, "vhp")
ASSETS_VHP_CT_RESIZE_DIR = os.path.join(ASSETS_VHP_DIR, "(VKH) CT Images Resize (1000 X 570)")
ASSETS_VHP_SEG_DIR = os.path.join(ASSETS_VHP_DIR, "(VKH) Segmented Images (1000 X 570)")

# # Assets Alignment Dir
ASSETS_ALIGNMENT_DIR = os.path.join(ASSETS_DIR, "alignment")
ASSETS_ALIGNMENT_CT_DIR = os.path.join(ASSETS_ALIGNMENT_DIR, "CT Image (494 x 281)")
ASSETS_ALIGNMENT_CT_RESIZE_DIR = os.path.join(ASSETS_ALIGNMENT_DIR, "CT Image Resize (1000 x 570)")

# # Assets DataAugmentationImage Dir
ASSETS_DA_DIR = os.path.join(ASSETS_DIR, "DataAugmentationImage")
# Normal
ASSETS_DA_DIR = os.path.join(ASSETS_DA_DIR, "Normal")
# CT
ASSETS_DA_CT_DIR = os.path.join(ASSETS_DA_DIR, "CT")
ASSETS_DA_CT_L_DIR = os.path.join(ASSETS_DA_CT_DIR, "Left")
ASSETS_DA_CT_L_5o_DIR = os.path.join(ASSETS_DA_CT_L_DIR,  "CtTurnLeft5Degree (1000 x 570)")
ASSETS_DA_CT_L_10o_DIR = os.path.join(ASSETS_DA_CT_L_DIR, "CtTurnLeft10Degree (1000 x 570)")
ASSETS_DA_CT_R_DIR = os.path.join(ASSETS_DA_CT_DIR, "Right")
ASSETS_DA_CT_R_5o_DIR = os.path.join(ASSETS_DA_CT_R_DIR, "CtTurnRight5Degree (1000 x 570)")
ASSETS_DA_CT_R_10o_DIR = os.path.join(ASSETS_DA_CT_R_DIR, "CtTurnRight10Degree (1000 x 570)")
# SEG
ASSETS_DA_SEG_DIR = os.path.join(ASSETS_DA_DIR, "SEG")
# SEG L
ASSETS_DA_SEG_L_DIR = os.path.join(ASSETS_DA_SEG_DIR, "Left")
ASSETS_DA_SEG_L_10o_DIR = os.path.join(ASSETS_DA_SEG_L_DIR, "SegLeft10Degree (1000 X 570)")
ASSETS_DA_SEG_L_5o_DIR = os.path.join(ASSETS_DA_SEG_L_DIR, "SegLeft5Degree (1000 X 570)")
# SEG R
ASSETS_DA_SEG_R_DIR = os.path.join(ASSETS_DA_SEG_DIR, "Right")
ASSETS_DA_SEG_R_10o_DIR = os.path.join(ASSETS_DA_SEG_R_DIR, "SegRight10Degree (1000 X 570)")
ASSETS_DA_SEG_R_5o_DIR = os.path.join(ASSETS_DA_SEG_R_DIR, "SegRight5Degree (1000 X 570)")
# Mirror
ASSETS_DA_M_DIR = os.path.join(ASSETS_DA_DIR, "Mirror")
# CT
ASSETS_DA_M_CT_DIR = os.path.join(ASSETS_DA_M_DIR, "CT")
ASSETS_DA_M_CT_RS_DIR = os.path.join(ASSETS_DA_M_CT_DIR, "MirrorCtResize (1000 x 570)")
# CT L
ASSETS_DA_M_CT_L_DIR = os.path.join(ASSETS_DA_M_CT_DIR, "Left")
ASSETS_DA_M_CT_L_5o_DIR = os.path.join(ASSETS_DA_M_CT_L_DIR, "MirrorCtTurnLeft5Degree (1000 x 570)")
ASSETS_DA_M_CT_L_10o_DIR = os.path.join(ASSETS_DA_M_CT_L_DIR, "MirrorCtTurnLeft10Degree (1000 x 570)")
# CT R
ASSETS_DA_M_CT_R_DIR = os.path.join(ASSETS_DA_M_CT_DIR, "Right")
ASSETS_DA_M_CT_R_5o_DIR = os.path.join(ASSETS_DA_M_CT_R_DIR, "MirrorCtTurnRight5Degree (1000 x 570)")
ASSETS_DA_M_CT_R_10o_DIR = os.path.join(ASSETS_DA_M_CT_R_DIR, "MirrorCtTurnRight10Degree (1000 x 570)")
# SEG
ASSETS_DA_M_SEG_DIR = os.path.join(ASSETS_DA_M_DIR, "SEG")
ASSETS_DA_M_SEG_DIR = os.path.join(ASSETS_DA_M_SEG_DIR, "MirrorSegmentedImages (1000 X 570)")
# SEG L
ASSETS_DA_M_SEG_L_DIR = os.path.join(ASSETS_DA_M_SEG_DIR, "Left")
ASSETS_DA_M_SEG_L_5o_DIR = os.path.join(ASSETS_DA_M_SEG_L_DIR, "MirrorSegLeft5Degree (1000 X 570)")
ASSETS_DA_M_SEG_L_10o_DIR = os.path.join(ASSETS_DA_M_SEG_L_DIR, "MirrorSegLeft10Degree (1000 X 570)")
# SEG R
ASSETS_DA_M_SEG_R_DIR = os.path.join(ASSETS_DA_M_SEG_DIR, "Right")
ASSETS_DA_M_SEG_R_5o_DIR = os.path.join(ASSETS_DA_M_SEG_R_DIR, "MirrorSegRight5Degree (1000 X 570)")
ASSETS_DA_M_SEG_R_10o_DIR = os.path.join(ASSETS_DA_M_SEG_R_DIR, "MirrorSegRight10Degree (1000 X 570)")

# # Modules
MODULES_DIR = os.path.join(ROOT_DIR, "modules")

# Projects
PROJECTS_DIR = os.path.join(ROOT_DIR, "projects")

# # Label Generate
PROJECTS_LG_DIR = os.path.join(PROJECTS_DIR, "LabelGenerate")

# Logs
LOGS_DIR = os.path.join(ROOT_DIR, "logs")

# Resources
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")

# # AbdominalCavityProject
RESOURCES_ACP_DIR = os.path.join(RESOURCES_DIR, "AbdominalCavityProject")
ACP_DATASET = os.path.join(RESOURCES_ACP_DIR, "dataset")
ACP_LABEL_DIR = os.path.join(RESOURCES_ACP_DIR, "label")
