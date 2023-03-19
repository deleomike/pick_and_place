from assistant.cyton.cyton import CytonGamma300
from spatialmath import SE3
from assistant.items.BaseItem import BaseItem
from roboticstoolbox import jtraj


class CytonController:
    """
    Management class for performing specific actions with the cyton gamma robot. Also provides an interface for
    sending commands to the robot
    """

    def __init__(self, robot: CytonGamma300 = None, starting_pose: SE3 = None, connect: bool = False):

        if robot is None:
            self.robot = CytonGamma300()

        if starting_pose is None:
            self.pose = self.robot.qz

        self.connect = connect

        if self.connect:
            self.establish_connection()

        print(f"Setting starting pose to {self.pose}")

        self.set_pose(self.pose)

    def establish_connection(self) -> bool:
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """
        print(f"Establishing Connection to {self.robot.name}")

        # TODO

    def set_pose(self, q: SE3):
        """
        Sets the pose for the robot. If connected, then it sets the robot's end effector pose.
        :param q: Pose (SE3)
        :return:
        """
        # TODO
        pass

    def grab_object(self, item: BaseItem):
        robot_object_pose = self.robot.ikine_LM(item.pose, q0=self.pose)

        traj = jtraj(self.pose, robot_object_pose, 100)