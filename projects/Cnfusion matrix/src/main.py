import json

import numpy
import numpy as np
import os
import pandas as pd
import random
import skimage.draw
import skimage.io
import sys
from sklearn.metrics import confusion_matrix

sys.path.append("../../../modules")
from modules.mrcnn import utils, visualize
from modules.mrcnn import model as model_lib
from modules.mrcnn.config import Config
from modules.trclab import config as docs


# noinspection DuplicatedCode
def inference(show_image=True, verbose=0, generator=True):
    config = InferenceConfigConfig()
    dataset = PeritonealDataset()
    dataset.load_peritoneal(docs.DATASET_KFOLD_C, "val")
    dataset.prepare()

    model = model_lib.MaskRCNN(mode="inference", model_dir=docs.LOGS_DIR, config=config)
    model.load_weights(MODEL_WEIGHT_PATH, by_name=True)

    # ground-truth and predictions lists
    gt_tot = np.array([])
    pred_tot = np.array([])
    # mAP list
    mAP_ = []

    saved_dir = os.path.join(docs.LOGS_DIR, "iou")
    json_file = os.path.join(saved_dir, "gt_pred_test.json")

    if generator:
        for image_id in dataset.image_ids:
            image, image_meta, gt_class_ids, gt_bbox, gt_masks = \
                model_lib.load_image_gt(dataset, config, image_id)

            results = model.detect([image], verbose=verbose)
            r = results[0]
            pred_bbox = r["rois"]
            pred_class_ids = r["class_ids"]
            pred_scores = r["scores"]
            pred_masks = r["masks"]

            if show_image:
                visualize.display_instances(
                    image=image,
                    boxes=gt_bbox,
                    masks=gt_masks,
                    class_ids=gt_class_ids,
                    class_names=dataset.class_names,
                    title="Gt Image")
                visualize.display_instances(
                    image=image,
                    boxes=pred_bbox,
                    masks=pred_masks,
                    class_ids=pred_class_ids,
                    class_names=dataset.class_names,
                    scores=pred_scores,
                    title="Pred Image")

            gt, pr = utils.gt_pred_lists(
                gt_class_ids=gt_class_ids,
                gt_bboxes=gt_bbox,
                pred_class_ids=pred_class_ids,
                pred_bboxes=pred_bbox
            )

            print(np.array(gt))
            print(np.array(pr))

            gt_tot = np.append(gt_tot, gt)
            pred_tot = np.append(pred_tot, pr)

            # precision_, recall_, AP_
            ap_, precision_, recall_, overlap_ = utils.compute_ap(
                gt_boxes=gt_bbox,
                gt_class_ids=gt_class_ids,
                gt_masks=gt_masks,
                pred_boxes=pred_bbox,
                pred_class_ids=pred_class_ids,
                pred_scores=pred_scores,
                pred_masks=pred_masks)

            mAP_.append(ap_)
            print("Average precision of this image : ", ap_)
            print("The actual mean average precision for the whole images (matterport methode) ", sum(mAP_) / len(mAP_))

        # check if the vectors len are equal
        print("the actual len of the gt vectors is : ", len(gt_tot))
        print("the actual len of the pred vectors is : ", len(pred_tot))
        print(gt_tot)
        print(pred_tot)

        gt_tot = gt_tot.astype(int)
        pred_tot = pred_tot.astype(int)

        gt_pred_tot_json = {
            "gt_tot": gt_tot,
            "pred_tot": pred_tot
        }
        df = pd.DataFrame(gt_pred_tot_json)
        if not os.path.exists(saved_dir):
            os.mkdir(saved_dir)
        df.to_json(json_file)

    json_data = json.load(open(json_file, 'r', encoding="UTF-8"))
    gt_tot = np.array([int(json_data["gt_tot"][idx]) for idx in json_data["gt_tot"]])
    pred_tot = np.array([int(json_data["pred_tot"][idx]) for idx in json_data["pred_tot"]])

    print("Loaded GT:", gt_tot, ",Length:", len(gt_tot))
    print("Loaded PR :", pred_tot, ",Length:", len(pred_tot))

    conf_m = confusion_matrix(gt_tot, pred_tot)
    num_classes = len(dataset.class_names[1:])
    #
    fp = [0] * num_classes
    fn = [0] * num_classes
    tp = [0] * num_classes

    print(conf_m)
    for i in range(conf_m.shape[0]):
        fn[i] += np.sum(conf_m[i]) - np.diag(conf_m)[i]
        fp[i] += np.sum(np.transpose(conf_m)[i]) - np.diag(conf_m)[i]
        for j in range(conf_m.shape[1]):
            if i == j:
                tp[i] += conf_m[i][j]

    print("size:", len(tp), ",tp:", tp, "sum:", sum(tp))
    print("size:", len(fp), ",fp:", fp, "sum:", sum(fp))
    print("size:", len(fn), ",fn:", fn, "sum:", sum(fn))


# noinspection DuplicatedCode
if __name__ == '__main__':
    PRETRAINING_WEIGHT_TYPE = "coco"
    LOGS_WEIGHTS_DIR = "peritoneal_e_coco20211105T1435"
    MODEL_WEIGHT_PATH = os.path.join(
        docs.LOGS_WEIGHTS_DIR, PRETRAINING_WEIGHT_TYPE, LOGS_WEIGHTS_DIR,
        "mask_rcnn_peritoneal_e_{}_0100.h5".format(PRETRAINING_WEIGHT_TYPE))
    if not os.path.exists(MODEL_WEIGHT_PATH):
        raise FileNotFoundError("Did not find this weight " + MODEL_WEIGHT_PATH)

    TRAINING_NAME = "Peritoneal_A_COCO"
    # noinspection DuplicatedCode
    CLASSES = [line.strip() for line in
               open(os.path.join(
                   docs.RESOURCES_KFOLD_DIR,
                   "peritoneal_cavity_without_color.txt"
               ), "r", encoding="UTF-8")]
    CLASSES_NUM = len(CLASSES)

    print("Loaded Classes:", CLASSES)
    print("Classes Count:", len(CLASSES))


    class PeritonealDataset(utils.Dataset):
        # noinspection DuplicatedCode
        def load_peritoneal(self, dataset_dir, subset):
            for idx, x in enumerate(CLASSES):
                self.add_class(TRAINING_NAME, idx + 1, x)

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

        # noinspection DuplicatedCode
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
            if info["source"] == TRAINING_NAME:
                return info["docs"]
            else:
                super(self.__class__, self).image_reference(image_id)


    class InferenceConfigConfig(Config):
        NAME = TRAINING_NAME
        IMAGES_PER_GPU = 1
        NUM_CLASSES = 1 + len(CLASSES)
        USE_MINI_MASK = False


    inference()
