import sys

sys.path.append("../../../modules")

# noinspection PyUnresolvedReferences
from mrcnn import model as utils


class CPCDataset(utils.Dataset):
    def load_VIA(self, dataset_dir, subset):
