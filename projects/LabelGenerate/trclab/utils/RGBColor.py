import json

from trclab.serialize.ISerializable import ISerializable


class RGBColor(ISerializable):
    def __init__(self, r: int = 0, g: int = 0, b: int = 0, serialize_data: str = None):
        self.serialize_data = serialize_data
        self.color = {
            "red": r if 0 <= r <= 255 else 0,
            "green": g if 0 <= g <= 255 else 0,
            "blue": b if 0 <= b <= 255 else 0
        }

        if serialize_data is not None:
            self.color = self.deserialize()

    def get(self) -> dict:
        return self.color

    def red(self) -> int:
        return self.color["red"]

    def green(self) -> int:
        return self.color["green"]

    def blue(self) -> int:
        return self.color["blue"]

    def serialize(self) -> json:
        return json.dumps(self.color)

    def deserialize(self) -> dict:
        return json.loads(self.serialize_data)
