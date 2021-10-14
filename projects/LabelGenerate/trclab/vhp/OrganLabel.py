import json

from trclab.serialize.ISerializable import ISerializable
from trclab.utils.ProgressBar import ProgressBar


class OrganLabel(ISerializable):
    def __init__(self, label_file: str, deserialize: bool = False):
        self.labels = []
        self.rgb_list = []
        if not deserialize:
            progress = ProgressBar(sum(1 for _ in open(label_file)), 'Load organ label')
            with open(label_file, 'r') as labels:
                for line in labels:
                    line = line.rstrip().replace('\t', ',')
                    progress.update("process line '%s'" % line)
                    if line.startswith('#') or not line.strip():
                        continue

                    rst = line.split(',')
                    self.labels.append([rst[0], (int(rst[1]), int(rst[2]), int(rst[3])), rst[4], rst[5]])

            progress.finish("Label loaded successful!")

        else:
            self.deserialize_file = label_file
            self.deserialize()

    def get_rgb_list(self):
        rgb_set = []
        for label in self.labels:
            rgb_set.append(label[1])

        return rgb_set

    def serialize(self):
        data = {}
        for n in range(0, len(self.labels)):
            data[n] = {}
            data[n]['organ_name'] = self.labels[n][0]
            data[n]['color'] = {}
            data[n]['color']['r'] = self.labels[n][1][0]
            data[n]['color']['g'] = self.labels[n][1][1]
            data[n]['color']['b'] = self.labels[n][1][2]
            data[n]['index'] = {}
            data[n]['index']['start'] = self.labels[n][2]
            data[n]['index']['end'] = self.labels[n][3]

        return json.dumps(data)

    def deserialize(self):
        data = json.load(open(self.deserialize_file, 'r'))
        for n in range(0, len(data)):
            index = str(n)
            name = data[index]['organ_name']
            r = data[index]['color']['r']
            g = data[index]['color']['g']
            b = data[index]['color']['b']
            start = data[index]['index']['start']
            end = data[index]['index']['end']
            self.labels.append([name, (int(r), int(g), int(b)), start, end])
