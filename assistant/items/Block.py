
import enum

from spatialmath import SE3
from typing import Union, Tuple

from assistant.items.locations import *
from assistant.items.BaseItem import BaseItem


class Block(BaseItem):

    def __init__(self,
                 pos_id: int,
                 start_location: BlockStartLocations = None,
                 end_location: BlockEndLocations = None,
                 width: float = 0.1,
                 height: float = 0.1,
                 length: float = 0.1):

        super(Block, self).__init__(pose=None)

        self.pos_id = pos_id
        self.width = width
        self.height = height
        self.length = length

        if start_location is None:
            self.start_location = list(BlockStartLocations)[self.pos_id-1]
            
        if end_location is None:
            self.end_location = list(BlockEndLocations)[self.pos_id-1]

    @property
    def start_pose(self):
        return self.start_location.value[0]

    @property
    def end_pose(self):
        return self.end_location.value[0]

    def __str__(self):
        return f"Block{self.pos_id}"