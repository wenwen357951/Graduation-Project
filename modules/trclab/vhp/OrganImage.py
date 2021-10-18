import os

import numpy as np
from PIL import Image


class OrganImage:
    def __init__(self, image_file: str):
        self.filepath = image_file
        self.basename = os.path.basename(image_file)
        ts = self.basename.split('.')
        self.extension = ts[len(ts) - 1]
        self._image_rgb_list = None

    def get_rgb_list(self) -> list:
        if self._image_rgb_list is None:
            with Image.open(self.filepath) as image:
                image_rgb = np.array(image)
                color = []
                for rgb in image_rgb:
                    for n in rgb:
                        n = list(n)
                        color.append((n[0], n[1], n[2]))

                self._image_rgb_list = color

        return self._image_rgb_list

    def get_file(self):
        return self.filepath
