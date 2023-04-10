import numpy as np

from math import pi
from roboticstoolbox import DHRobot, RevoluteDH, PrismaticDH, RevoluteMDH, PrismaticMDH
from assistant.items.BaseItem import BaseItem




class CytonGamma300(DHRobot):
    """
    Create model of cyton gamma 300 manipulator

    :notes:

    :references:

    """

    def __init__(self):
        deg = pi / 180

        elbow_rotate = 105
        shoulder_lim = np.array([-150, 150]) * deg
        elbow_lim = np.array([-elbow_rotate, elbow_rotate]) * deg

        Links =[
            # Base Joint
            RevoluteDH(d=0.120, a=0, alpha=pi / 2, qlim=shoulder_lim),
            # Elbow Joint
            RevoluteDH(d=0, a=0.1408, alpha=-pi/2, qlim=elbow_lim, offset=pi/2),
            # Elbow
            RevoluteDH(d=0, a=0.0718, alpha=-pi/2, qlim=elbow_lim),
            # Elbow
            RevoluteDH(d=0, a=0.718, alpha=pi/2, qlim=elbow_lim),
            # wrist
            RevoluteDH(d=0, a=0.1296, alpha=pi/2, qlim=np.array([-115, 115]) * deg),
            # wrist
            RevoluteDH(alpha=-pi/2, qlim=np.array([-170, 170]) * deg)
        ]

        super().__init__(Links, name="Cyton Gamma 300", manufacturer="Robai")

        # zero angles, L shaped pose
        self._qz = np.zeros(6)  # create instance attribute

    @property
    def qz(self):
        return self._qz


if __name__ == '__main__':

    robot = CytonGamma300()
    print(robot)