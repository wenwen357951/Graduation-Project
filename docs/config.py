import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

# Assets Dir
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

# # Assets VHP Dir
ASSETS_VHP_DIR = os.path.join(ASSETS_DIR, "vhp")
ASSETS_VHP_CT_DIR = os.path.join(ASSETS_VHP_DIR, "CT Image (494 x 281)")
ASSETS_VHP_CT_RESIZE_DIR = os.path.join(ASSETS_VHP_DIR, "CT Image Resize (1000 x 570)")

# # Assets Alignment Dir
ASSETS_ALIGNMENT_DIR = os.path.join(ASSETS_DIR, "alignment")
ASSETS_ALIGNMENT_CT_RESIZE_DIR = os.path.join(ASSETS_ALIGNMENT_DIR, "(VKH) CT Images Resize (1000 X 570)")
ASSETS_ALIGNMENT_SEG_DIR = os.path.join(ASSETS_ALIGNMENT_DIR, "(VKH) CT Images Resize (1000 X 570)")

# Projects
PROJECTS_DIR = os.path.join(ROOT_DIR, "projects")

# # Liver Tumor Resection
PROJECTS_LTR_DIR = os.path.join(PROJECTS_DIR, "LiverTumorResection")
