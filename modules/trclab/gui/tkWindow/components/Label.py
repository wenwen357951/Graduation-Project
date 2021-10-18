import tkinter as tk

from trclab.gui.tkWindow import ComponentType
from trclab.gui.tkWindow.components.Component import Component


class Label(Component):
    def __init__(self, internal_name: str, serialize_data: str = None):
        super().__init__(ComponentType.LABEL, internal_name, serialize_data)
        if serialize_data is None:
            self._config = {
                'fg': '#000',
                'font': ('Arial', 12)
            }

    def create(self, tk_window: tk.Tk):
        label_item = tk.Label(tk_window, self._config)
        label_item.grid(self._layout)
