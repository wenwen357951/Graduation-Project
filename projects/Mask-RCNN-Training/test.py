import os
import random
import sys

sys.path.append("../../modules")

import skimage.io
# noinspection PyUnresolvedReferences
import mrcnn.model as modellib
# noinspection PyUnresolvedReferences
from mrcnn import visualize
# noinspection PyUnresolvedReferences
from mrcnn.config import Config
# noinspection PyUnresolvedReferences
from trclab import config as docs

MODEL_WEIGHT_PATH = os.path.join(docs.LOGS_DIR, "peritoneal_a_coco20211103T2100", "mask_rcnn_peritoneal_a_coco_0026.h5")

if not os.path.exists(MODEL_WEIGHT_PATH):
    print('Did not find this weight' + MODEL_WEIGHT_PATH)

IMAGE_DIR = os.path.join(docs.DATASET_KFOLD_E, "val")
CLASSES = [line.strip() for line in
           open(os.path.join(docs.RESOURCES_KFOLD_DIR,
                             "peritoneal_cavity_without_color.txt"), 'r', encoding="UTF-8")]
CLASSES_NUM = len(CLASSES)

print("Classes: ", CLASSES)
print("Classes size: ", CLASSES_NUM)


class BottleConfig(Config):
    NAME = "Peritoneal_A_COCO"

    IMAGES_PER_GPU = 2

    NUM_CLASSES = 1 + CLASSES_NUM


class InferenceConfig(BottleConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


CLASSES.insert(0, "BG")

config = InferenceConfig()
model = modellib.MaskRCNN(mode="inference", model_dir=docs.LOGS_DIR, config=config)
model.load_weights(MODEL_WEIGHT_PATH, by_name=True)
class_names = CLASSES
file_names = next(os.walk(IMAGE_DIR))[2]

random_image = os.path.join(IMAGE_DIR, random.choice(file_names))
print(file_names)
print(random_image)

image = skimage.io.imread(random_image)
results = model.detect([image], verbose=1)
r = results[0]
visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                            class_names, r['scores'])
