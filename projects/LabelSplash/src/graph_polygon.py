import json
import os
import random
import sys

import cv2
import numpy as np

# Import doc.config
sys.path.append("../../../")
from docs import config


def random_color():
    return random.choice(range(256)), random.choice(range(256)), random.choice(range(256))


def main():
    image_dir = config.ASSETS_ALIGNMENT_CT_RESIZE_DIR
    files = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
    img_file = random.choice(files)

    with open(os.path.join(config.LOGS_DIR, "acp_.json"), 'r') as json_file:
        json_data = json.load(json_file)

    if json_data is None:
        return

    filename = "{}{}".format(os.path.basename(img_file), os.path.getsize(img_file))
    data = json_data[filename]
    size = len(data["regions"])

    image = cv2.imread(img_file)

    mask_image = np.array(image)

    regions = data["regions"]
    for idx in range(size):
        region = regions[str(idx)]
        shape_attributes = region["shape_attributes"]
        points_x = shape_attributes["all_points_x"]
        points_y = shape_attributes["all_points_y"]

        region_points = np.array([[[x, y]] for x, y in zip(points_x, points_y)])

        cv2.polylines(mask_image, region_points, isClosed=True, color=random_color(), thickness=1)

    cv2.imshow("Image", mask_image)

    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
