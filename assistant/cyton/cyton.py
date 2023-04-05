
import numpy as np

from math import pi
from roboticstoolbox import DHRobot, RevoluteDH, PrismaticDH, RevoluteMDH, PrismaticMDH
from assistant.items.BaseItem import BaseItem


class CytonGamma300(DHRobot):
    """
    Create model of Cyton Gamma 300 manipulator
    """
    def __init__(self):
        deg = pi / 180

        elbow_rotate = 105
        shoulder_lim = np.array([-150, 150]) * deg
        elbow_lim = np.array([-elbow_rotate, elbow_rotate]) * deg

        links =[
            # Base Joint
            RevoluteDH(d=0.120, a=0, alpha=pi / 2, qlim=shoulder_lim),
            # First Elbow Joint
            RevoluteDH(d=0, a=0.1408, alpha=-pi/2, qlim=elbow_lim, offset=pi/2),
            RevoluteDH(d=0, a=0.0718, alpha=-pi/2, qlim=elbow_lim),
            RevoluteDH(d=0, a=0.718, alpha=pi/2, qlim=elbow_lim),
            RevoluteDH(d=0, a=0.1296, alpha=pi/2, qlim=elbow_lim),
            RevoluteDH(alpha=-pi/2)
        ]

        super().__init__(links, name="Cyton Gamma 300", manufacturer="Robai")

        # zero angles, L shaped pose
        self._qz = np.zeros(6)  # create instance attribute

    def set_joint_position(self, joint_index: int, joint_value: float):
        """
        Sets the joint position for the specified joint index
        :param joint_index: The index of the joint to be set
        :param joint_value: The desired joint angle value
        :return: None
        """
        if 0 <= joint_index < len(self.links):
            self._qz[joint_index] = joint_value
            self.fkine(self._qz)  # Recalculate the end-effector pose based on the new joint values
        else:
            print(f"Invalid joint index: {joint_index}. Joint index should be between 0 and {len(self.links) - 1}.")

    @property
    def qz(self):
        return self._qz


if __name__ == '__main__':

    robot = CytonGamma300()
    print(robot)
