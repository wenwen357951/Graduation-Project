import json
import os
import random
import sys

import cv2
import numpy as np

# Import doc.config
sys.path.append("../../../")
from mydocs import config


def random_color():
    return random.choice(range(128, 256)), random.choice(range(128, 256)), random.choice(range(128))


# noinspection PyUnresolvedReferences
def main():
    image_dir = config.ASSETS_ALIGNMENT_CT_RESIZE_DIR
    files = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
    img_file = random.choice(files)

    with open(os.path.join(config.LOGS_DIR, "acp.json"), 'r') as json_file:
        json_data = json.load(json_file)

    if json_data is None:
        return

    filename_hj = "{}{}".format(os.path.basename(img_file), os.path.getsize(img_file))
    filename_or = os.path.join(
        config.ASSETS_VHP_CT_RESIZE_DIR,
        "{}_ct_output.jpg".format(
            os.path.basename(img_file).split('.')[0]
        ))
    data = json_data[filename_hj]
    size = len(data["regions"])

    image_h = cv2.imread(img_file)

    image_o = cv2.imread(filename_or)

    mask_image_h = np.array(image_h)
    mask_image_o = np.array(image_o)

    regions = data["regions"]
    for idx in range(size):
        region = regions[str(idx)]
        shape_attributes = region["shape_attributes"]
        points_x = shape_attributes["all_points_x"]
        points_y = shape_attributes["all_points_y"]

        region_points = np.array([[[x, y]] for x, y in zip(points_x, points_y)])

        cv2.polylines(mask_image_h, region_points, isClosed=True, color=random_color(), thickness=3)
        cv2.polylines(mask_image_o, region_points, isClosed=True, color=random_color(), thickness=3)

    cv2.imshow("Image_HJ", mask_image_h)
    cv2.imshow("Image_OR", mask_image_o)

    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()


# mina
if __name__ == '__main__':
    main()
