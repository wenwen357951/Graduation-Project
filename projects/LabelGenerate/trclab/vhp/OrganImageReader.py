import cv2
import numpy as np
from PIL import Image

from trclab.vhp.OrganImage import OrganImage
from trclab.vhp.OrganLabel import OrganLabel


class OrganImageReader:
    def __init__(self, image: OrganImage, label: OrganLabel):
        self.organ_image = image
        self.image_rgb_list = []
        for rgb in image.get_rgb_list():
            self.image_rgb_list.append([*rgb, ])

        self.image_rgb_set = set(image.get_rgb_list())
        self.label_rgb_list = []
        for rgb in label.get_rgb_list():
            self.label_rgb_list.append([*rgb, ])

        self.label_rgb_set = set(label.get_rgb_list())
        self.intersection_set = self.image_rgb_set.intersection(self.label_rgb_set)
        self.threshold = 127

    def find_organ(self) -> list:
        _mask = []
        for mask in self.intersection_set:
            _mask.append([*mask, ])

        return _mask

    def filter_from_index(self, index: int):
        with Image.open(self.organ_image.get_file()) as image:
            image_arr = np.array(image)
            for y in range(np.size(image_arr, 1)):
                for x in range(np.size(image_arr, 0)):
                    if image_arr[x, y, 0] == self.label_rgb_list[index - 1][0] \
                            and image_arr[x, y, 1] == self.label_rgb_list[index - 1][1] \
                            and image_arr[x, y, 2] == self.label_rgb_list[index - 1][2]:
                        image_arr[x, y] = 255
                    else:
                        image_arr[x, y] = 0
            return image_arr

    def get_contours(self, filter_image):
        image_gray = cv2.cvtColor(filter_image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(image_gray, self.threshold, 255, 0)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) == 0:
            return None

        return contours

    def get_index(self, xyz) -> int:
        return self.label_rgb_list.index(xyz) + 1
