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
ASSETS_DATAAUGMENTATIONIMAGE_DIR = os.path.join(ASSETS_DIR, "DataAugmentationImage")
ASSETS_DATAAUGMENTATIONIMAGE_CT_TURN_LEFT_5DEGREE_DIR = os.path.join(ASSETS_DATAAUGMENTATIONIMAGE_DIR,  "CtTurnLeft5Degree")
ASSETS_DATAAUGMENTATIONIMAGE_CT_RIGHT_LEFT_5DEGREE_DIR = os.path.join(ASSETS_DATAAUGMENTATIONIMAGE_DIR, "CtTurnRight5Degree")
ASSETS_DATAAUGMENTATIONIMAGE_MIRROR_CT_TURN_LEFT_5DEGREE_DIR = os.path.join(ASSETS_DATAAUGMENTATIONIMAGE_DIR, "MirrorCtTurnLeft5Degree")
ASSETS_DATAAUGMENTATIONIMAGE_MIRROR_CT_TURN_RIGHT_5DEGREE_DIR = os.path.join(ASSETS_DATAAUGMENTATIONIMAGE_DIR, "MirrorCtTurnRight5Degree")
ASSETS_DATAAUGMENTATIONIMAGE_MIRROR_CT_RESIZE = os.path.join(ASSETS_DATAAUGMENTATIONIMAGE_DIR, "MirrorCtResize")

# Modules
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
