from assistant.items.BaseItem import BaseItem
from spatialmath import SE3


class Block(BaseItem):

    def __init__(self,
                 color: str,
                 width: float,
                 height: float,
                 length: float,
                 pose: SE3):

        super(Block, self).__init__(pose=pose)

        self.color = color
        self.width = width
        self.height = height
        self.length = length
