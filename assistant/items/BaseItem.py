from abc import ABC, abstractmethod
from spatialmath import SE3


class BaseItem(ABC):

    def __init__(self, pose: SE3):
        self.pose = pose

    def set_xyz(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z