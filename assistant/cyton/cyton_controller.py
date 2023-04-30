
import socket
import time

import numpy as np

from assistant.cyton.cyton import CytonGamma300
from assistant.cyton.cyton_connection import CytonConnection
from assistant.items.BaseItem import BaseItem

from typing import List
from tqdm import tqdm
from spatialmath import SE3
from roboticstoolbox import jtraj
from roboticstoolbox.tools.trajectory import Trajectory

from assistant.cyton.cyton import CytonGamma300
from assistant.items.Block import Block


class CytonController:
    """
    Management class for performing specific actions with the cyton gamma robot. Also provides an interface for
    sending commands to the robot
    """

    def __init__(self,
                 robot: CytonGamma300 = CytonGamma300(),
                 client: CytonConnection = None,
                 dt: float = 0.01):

        self.robot = robot
        self.client = client
        self.dt = dt

        # TODO: This is probably not the starting point all the time. Find this out
        self.current_angles = self.robot.qz

        self.go_home()

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        if self.client is not None:
            self.client.disconnect()

    ###############################
    # Sending Commands and Angles #
    ###############################

    def set_angles(self, q: List):
        if self.client is not None:
            self.client.send_angles(q)
        else:
            print(f"Setting angles without a client: {q}")

        self.current_angles = q
        time.sleep(self.dt)

    def run_trajectory(self, qs: List[List[float]]):
        if type(qs) != List:
            qs = qs.q
        for q in qs:
            self.set_angles(q)

    def set_pose(self, T: SE3):
        """
        Sets the pose for the robot. If connected, then it sets the robot's end effector pose.
        :param T: Pose (SE3)
        :return:
        """
        q = self.robot.ikine_LM(T)
        self.set_angles(q)

        print(f"Setting pose: {T}")
        print(f"Corresponding joint angles: {q}")

    #############
    # Go Places #
    #############

    def go_home(self):
        """
        Goes back to initial starting point
        :return: None
        """
        print("Going Home")
        if (self.current_angles != self.robot.qz).all():
            traj = jtraj(self.current_angles, self.robot.qz, 100)

            self.run_trajectory(traj)
        else:
            self.set_angles(self.robot.qz)

    def goto_pickup(self, item: Block):
        """
        Goes to the pickup location
        :return: None
        """
        self.open_gripper()  # open gripper to pick up object (or keep gripper open)

        robot_pickup_q = self.robot.safe_ikine_LM(item.start_pose)

        robot_pickup_q = robot_pickup_q.q.tolist()
        robot_pickup_q.append(self.current_angles[-1])
        traj = jtraj(self.current_angles,robot_pickup_q, 100)

        self.run_trajectory(traj)
        self.close_gripper(item)  # close gripper upon object pickup

    def goto_dropoff(self, item: Block):
        """
        Goes to the dropoff location
        :return: None
        """
        robot_dropoff_q = self.robot.safe_ikine_LM(item.end_pose)
        robot_q = robot_dropoff_q.q.tolist()
        robot_q.append(self.current_angles[-1])
        traj = jtraj(self.current_angles, robot_q, 100)

        self.run_trajectory(traj)
        self.open_gripper()  # open gripper to drop off object

    ####################
    # General Commands #
    ####################

    def set_gripper(self, gripper_value):
        """
        Sets the gripper width
        :param gripper_value: The desired gripper width
        :return: None
        """

        # Set the joint position to the desired gripper_value (see `cyton.py`)
        gripper_joint_position = self.robot.clamp_gripper_value(gripper_value)

        # Update the current joint angles
        new_angles = self.current_angles
        new_angles[-1] = gripper_joint_position

        # Send the updated joint angles to the robot
        self.set_angles(self.current_angles)

        print(f"Gripper joint position: {gripper_joint_position}")

        return gripper_joint_position

    def open_gripper(self):
        """
        Opens the gripper
        :return: None
        """

        open_gripper_pos = self.set_gripper(self.robot.gripper_open_value)

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

        # Subtract an offset from the block width to close the gripper
        closed_gripper_pos = width - some_offset
        self.set_gripper(closed_gripper_pos)

        print(f"Closed gripper position: {closed_gripper_pos}")

    def pick_and_place(self, item: Block):
        """
        Executes a pick-and-place sequence with the robot.
        :param item: The object to be picked up
        :param dropoff_location: The drop-off location for the object
        :return: None
        """
        # Go to object (cube) location
        self.goto_pickup(item)

        # Move to drop-off location
        self.goto_dropoff(item)


if __name__ == "__main__":
    client = CytonConnection()
    controller = CytonController(client=client)

    controller.set_angles([1.058, 1.061, 0.2, 1.309, 0.0, 0.811476, 0.0, 0.013])

    # controller.set_angles([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01])

    # controller.go_home()