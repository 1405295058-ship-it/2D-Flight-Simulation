from enum import Enum, auto


class RenderType(Enum):
    POLYGON = auto()
    SPRITE = auto()


class RenderItem:
    def __init__(
        self,
        render_type: RenderType,
        *,
        shape=None,
        color=None,
        image=None,
    ):
        self.render_type = render_type
        self.shape = shape
        self.color = color
        self.image = image
        