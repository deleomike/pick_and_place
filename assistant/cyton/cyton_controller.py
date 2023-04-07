import socket

from assistant.cyton.cyton import CytonGamma300
from assistant.cyton.cyton_connection import CytonConnection
from assistant.items.BaseItem import BaseItem

from typing import List
from spatialmath import SE3
from roboticstoolbox import jtraj


class CytonController:
    """
    Management class for performing specific actions with the cyton gamma robot. Also provides an interface for
    sending commands to the robot
    """

    def __init__(self,
                 robot: CytonGamma300 = CytonGamma300(),
                 starting_pose: SE3 = None,
                 client: CytonConnection = None):

        self.robot = robot
        self.client = client

        if starting_pose is None:
            self.pose = self.robot.qz

        print(f"Setting starting pose to {self.pose}")

        self.go_home()

    def set_angles(self, q: List):
        if self.client is not None:
            self.client.send_angles(q)
        else:
            # TODO: printout
            pass

    def set_pose(self, T: SE3):
        """
        Sets the pose for the robot. If connected, then it sets the robot's end effector pose.
        :param q: Pose (SE3)
        :return:
        """
        # TODO call set angles
        q = self.robot.ikine_6s(T)
        self.set_angles(q)
        # TODO: fake printouts

    def go_home(self):
        self.set_angles(self.robot.qz)

    def grab_object(self, item: BaseItem):
        robot_object_pose = self.robot.ikine_LM(item.pose, q0=self.pose)

        traj = jtraj(self.pose, robot_object_pose, 100)


if __name__ == "__main__":

    controller = CytonController(client=CytonConnection())