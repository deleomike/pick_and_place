from spatialmath import SE3
from assistant.items.locations import BlockEndLocations, BlockStartLocations
from assistant.items.BaseItem import BaseItem
from typing import Union


class Block(BaseItem):

    def __init__(self,
                 pos_id: int,
                 color: str,
                 location: Union[BlockStartLocations, BlockEndLocations],
                 pose: SE3 = SE3(0, 0, 0),
                 width: float = 0.1,
                 height: float = 0.1,
                 length: float = 0.1):

        super(Block, self).__init__(pose=pose)

        self.location = location
        self.pos_id = pos_id
        self.color = color
        self.width = width
        self.height = height
        self.length = length

        self.home_location = BlockStartLocations(self.pos_id)

    def __str__(self):
        return f"Block{self.pos_id}"

