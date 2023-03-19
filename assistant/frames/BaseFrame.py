from abc import ABC, abstractmethod
from spatialmath import SE3


class BaseFrame(ABC):

    def __init__(self, pose: SE3):
        self.pose = pose