import json
import tkinter as tk

import trclab.gui.tkWindow.components as tkComponent
from trclab.gui.tkWindow.Attributes import Attributes
from trclab.gui.tkWindow.ComponentType import ComponentType
from trclab.serialize.ISerializable import ISerializable


class TkWindow(ISerializable):
    def __init__(self, serialize_data: str = None):
        self.master = tk.Tk()
        self.displayable = False
        self.window_info = dict()
        self.components = list()
        if serialize_data is not None:
            self._serialize_data = serialize_data
            self.deserialize()
            self.__build__()

        else:
            self.window_info = {
                'title': "New Window",
                'width': 800,
                'height': 600,
            }
            self.components = list()

    def display(self) -> bool:
        if self.displayable:
            self.master.mainloop()
            return True
        return False

    def get(self, attr: Attributes) -> any:
        return self.window_info[attr.value]

    def __build__(self):
        self.master.title(self.window_info[Attributes.TITLE.value])
        self.master.geometry(
            f'{self.window_info[Attributes.WIDTH.value]}x{self.window_info[Attributes.HEIGHT.value]}')

        for comp in self.components:
            comp.create(self.master)

        self.displayable = True

    def serialize(self) -> str:
        rst = self.window_info.copy()
        rst['component'] = {}
        for comp in self.components:
            data = json.loads(comp.serialize())
            head = list(data)[0]
            rst['component'][head] = {}
            rst['component'][head] = data[head]
        return json.dumps(rst)

    def deserialize(self):
        data = json.loads(self._serialize_data)
        self.window_info[Attributes.TITLE.value] = data[Attributes.TITLE.value]
        self.window_info[Attributes.WIDTH.value] = data[Attributes.WIDTH.value]
        self.window_info[Attributes.HEIGHT.value] = data[Attributes.HEIGHT.value]
        for comp in data['component']:
            component = None
            comp_data = data['component'][comp]
            comp_type = data['component'][comp]['type']
            rst = dict()
            rst[comp] = comp_data
            if ComponentType(comp_type) == ComponentType.LABEL:
                component = tkComponent.Label(comp, json.dumps(rst))
            elif ComponentType(comp_type) == ComponentType.BUTTON:
                component = tkComponent.Button(comp, json.dumps(rst))

            self.components.append(component)
