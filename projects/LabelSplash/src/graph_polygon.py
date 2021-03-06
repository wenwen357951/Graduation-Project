import cv2
import json
import numpy as np
import os
import random
import sys

# Import doc.config
sys.path.append("../../../")
from modules.trclab import config


def random_color():
    return random.choice(range(128, 256)), random.choice(range(128, 256)), random.choice(range(128))


# noinspection PyUnresolvedReferences
def main():
    image_dir = config.DATASET_DA_CT_R_5o
    files = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
    img_file = random.choice(files)

    with open(os.path.join(config.LOGS_DIR, "CtTurnRight5Degree.json"), 'r') as json_file:
        json_data = json.load(json_file)

    if json_data is None:
        return

    filename_hj = "{}{}".format(os.path.basename(img_file), os.path.getsize(img_file))
    # filename_or = os.docs.join(
    #     config.ASSETS_DA_CT_RIGHT_5o_DIR,
    #     "{}".format(
    #         os.docs.basename(img_file)
    #         os.docs.basename(img_file).split('.')[0]
    #     )
    data = json_data[filename_hj]
    size = len(data["regions"])

    image_h = cv2.imread(img_file)

    # image_o = cv2.imread(filename_or)

    mask_image_h = np.array(image_h)
    # mask_image_o = np.array(image_o)

    regions = data["regions"]
    for idx in range(size):
        region = regions[str(idx)]
        shape_attributes = region["shape_attributes"]
        points_x = shape_attributes["all_points_x"]
        points_y = shape_attributes["all_points_y"]

        region_points = np.array([[[x, y]] for x, y in zip(points_x, points_y)])

        cv2.polylines(mask_image_h, region_points, isClosed=True, color=random_color(), thickness=3)
        # cv2.polylines(mask_image_o, region_points, isClosed=True, color=random_color(), thickness=3)

    cv2.imshow("Image_HJ", mask_image_h)
    # cv2.imshow("Image_OR", mask_image_o)

    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()


# mina
if __name__ == '__main__':
    main()
