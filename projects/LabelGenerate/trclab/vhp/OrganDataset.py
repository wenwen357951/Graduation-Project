import numpy
import json
import os

from glob2 import glob
from multiprocessing import Pool, Manager

from trclab.utils.ProgressBar import ProgressBar
from trclab.vhp.OrganImage import OrganImage
from trclab.vhp.OrganImageReader import OrganImageReader

processing_manager = Manager()
lock = processing_manager.Lock()


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def data_process(image, label, target_dir, extension):
    image_name = os.path.basename(image.get_file())
    progress_bar = ProgressBar(2, "Start Process Image {}".format(image_name))

    progress_bar.update("Processing...")
    oir = OrganImageReader(image, label)
    data = json.loads("{}")

    organ_list = oir.find_organ()
    progress_bar.update("Found Organ Count {}".format(len(organ_list)))
    progress_bar.add_max_val(len(organ_list))

    target_basename = image.basename[:-len(image.extension)] + extension
    target_file_size = os.path.getsize(os.path.join(target_dir, target_basename))
    key = target_basename + str(target_file_size)
    progress_bar.update("Generate Data Key {}".format(key))

    data[key] = {}
    data[key]['fileref'] = ''
    data[key]['size'] = target_file_size
    data[key]['filename'] = target_basename
    data[key]['base64_img_data'] = ''
    data[key]['file_attributes'] = {}
    data[key]['regions'] = {}
    progress_bar.update("Init Basic Data Format")

    region_idx = 0
    for idx, organ in enumerate(organ_list):
        progress_bar.update("Processing Organ {}".format(idx))
        index = oir.get_index(organ)
        filter_image = oir.filter_from_index(index)
        contours = oir.get_contours(filter_image)
        for n in range(0, len(contours)):
            list_x = []
            list_y = []
            for point in contours[n]:
                for x, y in point:
                    list_x.append(x)
                    list_y.append(y)

            data[key]['regions'][region_idx] = {}
            data[key]['regions'][region_idx]['shape_attributes'] = {}
            data[key]['regions'][region_idx]['shape_attributes']['name'] = 'polygon'
            data[key]['regions'][region_idx]['shape_attributes']['all_points_x'] = list_x
            data[key]['regions'][region_idx]['shape_attributes']['all_points_y'] = list_y
            data[key]['regions'][region_idx]['region_attributes'] = {}
            data[key]['regions'][region_idx]['region_attributes']['name'] = str(oir.get_index(organ))
            region_idx += 1

    progress_bar.finish("Process Successful!")
    return data


class OrganDataset:
    def __init__(self, image_dir: str, extension: str = "*.jpg"):
        self.images = list()
        self.extension = extension
        self.images_label = None

        load_images = glob(os.path.join(image_dir, extension), recursive=True)
        progress_bar = ProgressBar(len(load_images), title="Loaded Organ Dataset")
        for img in load_images:
            progress_bar.update("process image %s" % os.path.basename(img))
            self.images.append(OrganImage(img))

        progress_bar.finish('Dataset loaded successful!')

    def set_label(self, vhp_label):
        self.images_label = vhp_label

    def export_label_area(self, target_dir, patten: str, output_file):
        if self.images_label is None:
            raise FileNotFoundError

        with open(output_file, 'w+') as export_file:
            export_file.write("{\n}")

        target_name_split = patten.split('.')
        target_extension = target_name_split[len(target_name_split) - 1]

        # progress_bar = ProgressBar(len(self.images), "Export label area")
        # counter = 0

        rst = []
        with Pool(5) as pool:
            process_data = []
            for image in self.images:
                process = (image, self.images_label, target_dir, target_extension)
                process_data.append(process)

            rst = pool.starmap(data_process, process_data)

        merged_dict = dict()
        if len(rst) != 0:
            for data in rst:
                merged_dict.update(data)

        with open(output_file, 'w') as out_file:
            json.dump(merged_dict, out_file, default=int, cls=MyEncoder)

        # for image in self.images:
        #     counter += 1
        #     progress_bar.update("Process Image (%s/%s)" % (counter, len(self.images)))
        #     oir = OrganImageReader(image, self.images_label, progress_bar)
        #     progress_bar.update("Find organ and get list (%s/%s)" % (counter, len(self.images)), just_message=True)
        #     organ_list = oir.find_organ()
        #     progress_bar.update("Get index of all founded organs (%s/%s)" % (counter, len(self.images)),
        #                         just_message=True)
        #
        #     target_basename = image.basename[:-len(image.extension)] + target_extension
        #     target_file_size = os.path.getsize(os.path.join(target_dir, target_basename))
        #     key = target_basename + str(target_file_size)
        #
        #     data[key] = {}
        #     data[key]['fileref'] = ''
        #     data[key]['size'] = target_file_size
        #     data[key]['filename'] = target_basename
        #     data[key]['base64_img_data'] = ''
        #     data[key]['file_attributes'] = {}
        #     data[key]['regions'] = {}
        #
        #     region_idx = 0
        #     progress_bar.update("Start Process %s (%s/%s)" % (key, counter, len(self.images)), just_message=True)
        #     for organ in organ_list:
        #         index = oir.get_index(organ)
        #         filter_image = oir.filter_from_index(index)
        #         contours = oir.get_contours(filter_image)
        #         for n in range(0, len(contours)):
        #             progress_bar.update("Processing... %s-%d (%s/%s)" % (key, n, counter, len(self.images)),
        #                                 just_message=True)
        #             list_x = []
        #             list_y = []
        #             for point in contours[n]:
        #                 for x, y in point:
        #                     list_x.append(x)
        #                     list_y.append(y)
        #
        #             data[key]['regions'][region_idx] = {}
        #             data[key]['regions'][region_idx]['shape_attributes'] = {}
        #             data[key]['regions'][region_idx]['shape_attributes']['name'] = 'polygon'
        #             data[key]['regions'][region_idx]['shape_attributes']['all_points_x'] = list_x
        #             data[key]['regions'][region_idx]['shape_attributes']['all_points_y'] = list_y
        #             data[key]['regions'][region_idx]['region_attributes'] = {}
        #             data[key]['regions'][region_idx]['region_attributes']['name'] = str(oir.get_index(organ))
        #             region_idx += 1
        #         progress_bar.update("%s Process successful! (%s/%s)" % (key, counter, len(self.images)),
        #                             just_message=True)

        # progress_bar.finish("Exported label area successful!")
        #
