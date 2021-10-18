from enum import Enum


class GridLayout(Enum):
    COLUMN = 'column'
    COLUMN_SPAN = 'column'
    ROW = 'row'
    ROW_SPAN = 'rowspan'
    STICKY = 'sticky'
    MARGIN_X = 'padx'
    MARGIN_Y = 'pady'
    PADDING_X = 'ipadx'
    PADDING_Y = 'ipady'
