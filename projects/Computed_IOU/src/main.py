import json
import os
import sys

import numpy as np

sys.path.append("../../../modules")
import modules.mrcnn.model as model_lib
import skimage.io
import skimage.draw
from modules.mrcnn import visualize
from modules.mrcnn import utils
from modules.mrcnn.config import Config
from modules.trclab import config as docs


# import mrcnn.model as model_lib
# import skimage.io
# import skimage.draw
# from mrcnn import visualize
# from mrcnn import utils
# from mrcnn.config import Config
# from trclab import config as docs
def inference():
    config = InferenceConfigConfig()

    dataset = PeritonealDataset()
    dataset.load_peritoneal(docs.DATASET_KFOLD_A, "val")
    dataset.prepare()

    model = model_lib.MaskRCNN(mode="inference", model_dir=docs.LOGS_DIR, config=config)
    model.load_weights(MODEL_WEIGHT_PATH, by_name=True)

    for ids in dataset.image_ids:
        image, image_meta, gt_class_id, gt_bbox, gt_mask = model_lib.load_image_gt(dataset, config, ids)
        info = dataset.image_info[ids]
        print(ids)
        print("image ID: {}.{} ({}) {}".format(info["source"], info["id"], ids,
                                               dataset.image_reference(ids)))

        r = model.detect([image], verbose=1)[0]

        print(gt_bbox.shape)
        print(gt_class_id.shape)
        print(gt_mask.shape)
        print("- - - - -")
        print(r['rois'].shape)
        print(r['class_ids'].shape)
        print(r['scores'].shape)
        print(r['masks'].shape)

        gt_match, pred_match, overlaps = \
            utils.compute_matches(
                gt_bbox, gt_class_id, gt_mask,
                r['rois'], r['class_ids'], r['scores'], r['masks'])

        print(gt_match)
        print(pred_match)
        print(overlaps)

        visualize.display_differences(
            image,
            gt_bbox, gt_class_id, gt_mask,
            r['rois'], r['class_ids'], r['scores'], r['masks'],
            CLASSES
        )

    #
    # visualize.display_differences(image,
    #                               gt_bbox, gt_class_id, gt_mask,
    #                               pred_bboxes, pred_ids, pred_scores, pred_masks,
    #                               dataset.class_names, score_threshold=0.8)

    # image = imread(filename)
    # result = model.detect([image], verbose=1)
    # global res
    # res = result[0]

    # visualize.display_instances(
    #     image,
    #     r['rois'],
    #     r['masks'],
    #     r['class_ids'],
    #     CLASSES,
    #     r['scores'],
    # )

    # filename_list = glob2.glob(os.path.join(IMAGE_DIR, "*.jpg"), recursive=True)
    # image_list = []
    # count = 0
    # temp_list = []
    # for filename in filename_list:
    #     temp_list.append(imread(filename))
    #     if count > 2:
    #         image_list.append(temp_list)
    #         temp_list = []
    #         count = 0
    #     else:
    #         count += 1
    #
    # if 0 < count <= 2 and len(temp_list) > 0:
    #     image_list.append(temp_list)
    #
    # for images in image_list:
    #     result_list = model.detect(images, verbose=1)
    #     for result in result_list:

    # result_list = model.detect(image_list, verbose=1)

    # print(len(result_list))


if __name__ == '__main__':
    MODEL_WEIGHT_PATH = os.path.join(
        docs.LOGS_DIR,
        "Weights/coco/peritoneal_a_coco20211104T2156",
        "mask_rcnn_peritoneal_a_coco_0100.h5")
    if not os.path.exists(MODEL_WEIGHT_PATH):
        raise FileNotFoundError("Did not find this weight " + MODEL_WEIGHT_PATH)

    TRAINING_NAME = "Peritoneal_A_COCO"
    IMAGE_DIR = os.path.join(docs.DATASET_KFOLD_A, "val")
    CLASSES = [line.strip() for line in
               open(os.path.join(
                   docs.RESOURCES_KFOLD_DIR,
                   "peritoneal_cavity_without_color.txt"
               ), "r", encoding="UTF-8")]
    CLASSES_NUM = len(CLASSES)

    print("Loaded Classes:", CLASSES)
    print("Classes Count:", len(CLASSES))


    class PeritonealDataset(utils.Dataset):
        def load_peritoneal(self, dataset_dir, subset):
            for x in range(CLASSES_NUM):
                self.add_class(TRAINING_NAME, x + 1, CLASSES[x])

            assert subset in ["train", "val"]
            dataset_dir = os.path.join(dataset_dir, subset)

            annotations = json.load(open(os.path.join(dataset_dir, "via_region_data.json")))
            annotations = list(annotations.values())
            annotations = [a for a in annotations if a['regions']]

            for a in annotations:
                if type(a['regions']) is dict:
                    polygons = [r['shape_attributes'] for r in a['regions'].values()]
                    names = [r['region_attributes'] for r in a['regions'].values()]

                else:
                    polygons = [r['shape_attributes'] for r in a['regions']]
                    names = [r['region_attributes'] for r in a['regions']]

                image_path = os.path.join(dataset_dir, a['filename'])
                image = skimage.io.imread(image_path)
                height, width = image.shape[:2]

                self.add_image(
                    TRAINING_NAME,
                    image_id=a['filename'],  # use file name as a unique image id
                    path=image_path,
                    width=width, height=height,
                    polygons=polygons, names=names)

        def load_mask(self, image_id):
            image_info = self.image_info[image_id]
            class_names = image_info["names"]

            if image_info["source"] != TRAINING_NAME:
                return super(self.__class__, self).load_mask(image_id)

            info = self.image_info[image_id]
            mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                            dtype=np.uint8)
            for i, p in enumerate(info["polygons"]):
                rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
                mask[rr, cc, i] = 1

            class_ids = np.zeros([len(info["polygons"])])
            for i, p in enumerate(class_names):
                if p['name'] in CLASSES:
                    class_ids[i] = CLASSES.index(p['name']) + 1

            class_ids = class_ids.astype(int)
            return mask.astype(np.bool_), class_ids

        def image_reference(self, image_id):
            """Return the docs of the image."""
            info = self.image_info[image_id]
            print("----polygons")
            print(type(info["polygons"]))
            print("----polygons")
            if info["source"] == TRAINING_NAME:
                return info["id"]
            else:
                super(self.__class__, self).image_reference(image_id)


    CLASSES.insert(0, "BG")


    class InferenceConfigConfig(Config):
        NAME = TRAINING_NAME
        IMAGES_PER_GPU = 1
        NUM_CLASSES = len(CLASSES)
        USE_MINI_MASK = False


    inference()
