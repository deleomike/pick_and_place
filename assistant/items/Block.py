
from spatialmath import SE3
from assistant.items.BaseItem import BaseItem


class Block(BaseItem):

    def __init__(self,
                 pos_id: int,
                 width: float,
                 height: float,
                 length: float,
                 pose: SE3):

        super(Block, self).__init__(pose=pose)

        self.pos_id = pos_id  # position id
        self.width = width    # block width
        self.height = height  # block height
        self.length = length  # block length
