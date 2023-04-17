
import numpy as np

from math import pi
from roboticstoolbox import DHRobot, RevoluteDH, PrismaticDH, RevoluteMDH, PrismaticMDH
from assistant.items.BaseItem import BaseItem
from assistant.exceptions import FailedIKINE


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

        links = [
            # Base Joint
            RevoluteDH(d=0.120, a=0, alpha=pi / 2, qlim=shoulder_lim),
            # Elbow Joint
            RevoluteDH(d=0, a=0.1408, alpha=-pi/2, qlim=elbow_lim, offset=pi/2),
            # Elbow
            RevoluteDH(d=0, a=0.0718, alpha=-pi/2, qlim=elbow_lim),
            # Elbow
            RevoluteDH(d=0, a=0.0718, alpha=pi/2, qlim=elbow_lim),
            # wrist
            RevoluteDH(d=0, a=0.1296, alpha=pi/2, qlim=np.array([-115, 115]) * deg),
            # wrist
            RevoluteDH(alpha=-pi/2, qlim=np.array([-170, 170]) * deg)
        ]

        self._links = links

        super().__init__(self._links, name="Cyton Gamma 300", manufacturer="Robai")

        self.num_joints = len(self.links) + 1

        self.gripper_open_value = 0.0143

        # zero angles, L shaped pose
        self._qz = np.zeros(self.num_joints)  # create instance attribute
        self._qz[-1] = self.gripper_open_value

    def clamp_gripper_value(self, joint_value: float) -> float:
        """
        Set the joint position for the given joint index
        :param joint_index: The index of the joint to set
        :param joint_value: The desired joint value
        :return: The updated joint value
        """

        # Check if the joint_value is within the joint limits and clamp if necessary
        if joint_value < 0:
            joint_value = 0
        elif joint_value > self.gripper_open_value:
            joint_value = self.gripper_open_value

        return joint_value

    @property
    def qz(self):
        return self._qz

    def safe_ikine_LM(self, *args, **kwargs):
        ikine_res = self.ikine_LM(*args, **kwargs)

        if ikine_res.success:
            return ikine_res
        else:
            raise FailedIKINE(ikine_obj=ikine_res)


if __name__ == '__main__':

    robot = CytonGamma300()
    print(robot)