
import enum

from spatialmath import SE3
from typing import Union

from assistant.items.locations import *
from assistant.items.BaseItem import BaseItem


class Block(BaseItem):

    def __init__(self,
                 pos_id: int,
                 location: Union[BlockStartLocations(start_locations[self.pos_id]),
                                 BlockEndLocations(end_locations[self.pos_id])],
                 pose: SE3 = SE3(0, 0, 0),
                 width: float = 0.1,
                 height: float = 0.1,
                 length: float = 0.1):

        super(Block, self).__init__(pose=pose)

        self.pos_id = pos_id
        self.location = location
        self.width = width
        self.height = height
        self.length = length

        self.home_location = BlockStartLocations(self.pos_id)

    def __str__(self):
        return f"Block{self.pos_id}"