import json
import time
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

JSON_PATH = '/home/j2031linux3090/Graduation-Project/resources/k-fold/A/train/via_region_data.json'
IMAGE_SHAPE=((570, 1000, 3))

def folder_confirm(class_name):
    try:
        if not os.path.isdir('label/{}'.format(str(class_name))):
            os.mkdir('label/{}'.format(str(class_name)))
    except:
        os.mkdir('label/{}'.format(str(class_name)))


if __name__ == '__main__':
    try:
        os.path.isdir('label')
    except:
        os.mkdir('label')

    dic = {}
    json_txt = list()
    with open(JSON_PATH, 'r') as txt:
        json_data = json.load(txt)

        start = time.time()
        # img2 = np.zeros(IMAGE_SHAPE)
        min_x = 1000
        for id in json_data:
            print(id)
            json_txt.append(id)
            # img = cv2.imread('./optest/{}'.format(IMAGE_NAME[json_txt.index(id)]))
            img = np.zeros(IMAGE_SHAPE)

            for index_ in json_data[id]["regions"]:
                img = np.zeros(img.shape)
                class_name = json_data[id]["regions"][index_]["region_attributes"]["name"]
                folder_confirm(class_name)

                x_range = json_data[id]["regions"][index_]["shape_attributes"]["all_points_x"]

                if len(x_range) > 1:
                    min_x = min(len(x_range), min_x)
                    x_range += [x_range[0]]  # 在陣列最後一個加上陣列的第一個，解決圖形漏洞

                y_range = json_data[id]["regions"][index_]["shape_attributes"]["all_points_y"]
                if len(y_range) > 1:
                    y_range += [y_range[0]]

                xy_list = list()
                for i in range(len(x_range)):
                    xy_list.append([x_range[i], y_range[i]])
                color = (255, 255, 255)
                point = np.array(xy_list)

                if len(point) > 0:
                    test_img = cv2.fillPoly(img, [point], color)
                cv2.imwrite('./label/{}/{}.png'.format(class_name, id), test_img)

        print("min x :", min_x)
