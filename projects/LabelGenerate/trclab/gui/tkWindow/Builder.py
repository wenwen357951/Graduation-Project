from trclab.gui.tkWindow.Attributes import Attributes
from trclab.gui.tkWindow.ComponentType import ComponentType
from trclab.gui.tkWindow.TkWindow import TkWindow
from trclab.gui.tkWindow.components.Component import Component


class Builder:
    def __init__(self, title: str = "New Window", width: int = 800, height: int = 600, serialize_data: str = None):
        if serialize_data is not None:
            self._window = TkWindow(serialize_data=serialize_data)

        else:
            self._window = TkWindow()
            self.set_attr(Attributes.TITLE, title)
            self.set_attr(Attributes.WIDTH, width)
            self.set_attr(Attributes.HEIGHT, height)

    def get_attr(self, attr: Attributes) -> any:
        return self._window.get(attr)

    def set_attr(self, attr: Attributes, value: any):
        self._window.window_info[attr.value] = value

    def append_component(self, component: Component):
        self._window.components.append(component)

    def get_components(self) -> list[Component]:
        return self._window.components

    def get_components_by_type(self, component_type: ComponentType) -> list[Component]:
        select = []
        for comp in self._window.components:
            # noinspection PyProtectedMember
            if component_type is comp._comp_type:
                select.append(comp)

        return select

    def get_components_by_internal_name(self, text: str, fuzzy=False) -> list[Component]:
        select = []
        for comp in self._window.components:
            # noinspection PyProtectedMember
            internal_name = str(comp._internal_name)
            if (fuzzy and text in internal_name) or (not fuzzy and text == internal_name):
                select.append(comp)

        return select

    def build(self) -> TkWindow:
        self._window.__build__()
        return self._window
