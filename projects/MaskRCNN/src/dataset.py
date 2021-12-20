import json
import os.path
import sys
import skimage.io
import skimage.draw
import numpy as np
import settings

sys.path.append("../../../")
from modules.mrcnn import utils


class CPCDataset(utils.Dataset):
    def load_via(self, dataset_dir, subset):
        for x in range(settings.CLASSES_NUM):
            self.add_class(
                settings.RECOGNIZABLE_NAME,
                x + 1,
                settings.CLASSES[x]
            )

        assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset)

        annotations = json.load(open(os.path.join(dataset_dir, "via_region_data.json")))
        annotations = list(annotations.values())

        annotations = [a for a in annotations if a["regions"]]

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
                settings.RECOGNIZABLE_NAME,
                image_id=a["filename"],
                path=image_path,
                width=width, height=height,
                polygons=polygons, names=names
            )

    def load_mask(self, image_id):
        image_info = self.image_info[image_id]
        class_names = image_info["names"]
        if image_info["source"] != settings.RECOGNIZABLE_NAME:
            return super(self.__class__, self).load_mask(image_id)

        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1

        class_ids = np.zeros([len(info["polygons"])])
        for i, p in enumerate(class_names):
            if p['name'] in settings.CLASSES:
                class_ids[i] = settings.CLASSES.index(p['name']) + 1

        class_ids = class_ids.astype(int)
        return mask.astype(np.bool_), class_ids

    def image_reference(self, image_id):
        info = self.image_info[image_id]
        if info["source"] == settings.RECOGNIZABLE_NAME:
            return info["docs"]
        else:
            super(self.__class__, self).image_reference(image_id)
