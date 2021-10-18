import json

from trclab.gui.tkWindow.ComponentType import ComponentType
from trclab.gui.tkWindow.components.Properties import Properties
from trclab.gui.tkWindow.layout.GridLayout import GridLayout
from trclab.serialize.ISerializable import ISerializable


class Component(ISerializable):
    def __init__(self, comp_type: ComponentType, internal_name: str, serialize_data: str = None):
        self._comp_type = comp_type
        self._internal_name = internal_name
        if serialize_data is not None:
            self.serialize_data = serialize_data
            self.deserialize()
        else:
            self._config = dict()
            self._layout = {
                GridLayout.COLUMN.value: 0,
                GridLayout.ROW.value: 0
            }

    def layout(self, g_layout: GridLayout, value: any):
        self._layout[g_layout.value] = value

    def set(self, properties: Properties, value: any):
        self._config[properties.value] = value

    def get(self, properties: Properties) -> any:
        return self._config[properties.value]

    def internal_name(self, name: str):
        self._internal_name = name

    def serialize(self) -> str:
        rst = dict()
        rst[self._internal_name] = {}
        rst[self._internal_name]['type'] = self._comp_type.value
        rst[self._internal_name]['metadata'] = self._config
        rst[self._internal_name]['layout'] = self._layout
        return json.dumps(rst)

    def deserialize(self):
        data = dict(json.loads(self.serialize_data))
        original_internal_name = str(list(data.keys())[0])
        compType = ComponentType(data[original_internal_name]['type'])
        self._comp_type = compType
        self._config = data[original_internal_name]['metadata']
        self._layout = data[original_internal_name]['layout']

    def create(self, tk_window):
        pass
