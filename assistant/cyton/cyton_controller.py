
import socket
import numpy as np

from assistant.cyton.cyton import CytonGamma300
from assistant.cyton.cyton_connection import CytonConnection
from assistant.items.BaseItem import BaseItem

from typing import List
from spatialmath import SE3
from roboticstoolbox import jtraj

from assistant.cyton.cyton import CytonGamma300
from assistant.items.Block import Block


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

        # TODO: This is probably not the starting point all the time. Find this out
        self.current_angles = self.robot.qz

        self.go_home()

    ###############################
    # Sending Commands and Angles #
    ###############################

    def set_angles(self, q: List):
        if self.client is not None:
            self.client.send_angles(q)
        else:
            # TODO: printout
            pass

        self.current_angles = q

    def run_trajectory(self, qs: List[List[float]]):
        for q in qs:
            self.set_pose(q)

    def set_pose(self, T: SE3):
        """
        Sets the pose for the robot. If connected, then it sets the robot's end effector pose.
        :param q: Pose (SE3)
        :return:
        """
        q = self.robot.ikine_LM(T)
        self.set_angles(q)
        # TODO: fake printouts

    #############
    # Go Places #
    #############

    def go_home(self):
        """
        Goes back to initial starting point
        :return: None
        """
        self.set_angles(self.robot.qz)

    def goto_pickup(self, item: Block):
        """
        Goes to the pickup location
        :return: None
        """
        self.open_gripper(item)  # open gripper to pick up object (or keep gripper open)

        robot_pickup_pose = self.robot.ikine_LM(item.pose, q0=self.pose)
        traj = jtraj(self.pose, robot_pickup_pose, 100)

        self.run_trajectory(traj)
        self.close_gripper(item)  # close gripper upon object pickup

    def goto_dropoff(self, item: Block, location: SE3):
        """
        Goes to the dropoff location
        :return: None
        """
        robot_dropoff_pose = self.robot.ikine_LM(location, q0=self.pose)
        traj = jtraj(self.pose, robot_dropoff_pose, 100)

        self.run_trajectory(traj)
        self.open_gripper(item)  # open gripper to drop off object

    ####################
    # General Commands #
    ####################

    def set_gripper(self, gripper_value):
        """
        Sets the gripper width
        :param gripper_value: The desired gripper width
        :return: None
        """
        gripper_joint_index = 5  # Index of the joint controlling gripper for Cyton Gamma 300

        # Set the joint position to the desired gripper_value (see `cyton.py`)
        gripper_joint_position = self.robot.set_joint_position(gripper_joint_index, gripper_value)
        gripper_joint_position

        print(f"Gripper joint position: {gripper_joint_position}")

    def open_gripper(self, item: Block):
        """
        Opens the gripper
        :return: None
        """
        width = item.width  # in meters
        some_offset = 0.01  # in meters

        # Add an offset to the block width to open the gripper
        open_gripper_pos = self.set_gripper(width + some_offset)
        open_gripper_pos

        print(f"Open gripper position: {open_gripper_pos}")


    # NOTE: `some_offset`` is a value we need to define to ensure the gripper is open enough to 
    # pick up the block or closed enough to grip it. We can define this value based on our 
    # gripper's specifications or through experimentation.


    def close_gripper(self, item: Block):
        """
        Closes the gripper
        :return: None
        """
        width = item.width  # in meters
        some_offset = 0.01  # in meters

        #  Subtract an offset from the block width to close the gripper
        closed_gripper_pos = self.set_gripper(width - some_offset)
        closed_gripper_pos

        print(f"Closed gripper position: {closed_gripper_pos}")

    def pick_and_place(self, item: Block, dropoff_location: SE3):
        """
        Executes a pick-and-place sequence with the robot.
        :param item: The object to be picked up
        :param dropoff_location: The drop-off location for the object
        :return: None
        """
        # Go to object (cube) location
        self.goto_pickup(item)

        # Move to drop-off location
        self.goto_dropoff(item, dropoff_location)


if __name__ == "__main__":
    controller = CytonController(client=CytonConnection())
