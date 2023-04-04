
import socket

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

        self.sock: socket.socket = None
        self.udp_ip = None
        self.udp_port = None

        if self.connect:
            self.establish_connection()

        print(f"Setting starting pose to {self.pose}")

        self.set_pose(self.pose)


    def establish_connection(self, udp_ip: str = "127.0.0.1", udp_port: int = 5005) -> bool:
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """
        print(f"Establishing Connection to {self.robot.name} at {udp_ip}:{udp_port}")

        self.udp_ip = udp_ip
        self.udp_port = udp_port

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP


    def set_pose(self, q: SE3):
        """
        Sets the pose for the robot. If connected, then it sets the robot's end effector pose.
        :param q: Pose (SE3)
        :return:
        """
        # TODO

        if self.connect:
            try:
                self.sock.send(q)
            except Exception as e:
                # recreate the socket and reconnect
                print(f"Error connecting to {self.udp_ip}:{self.udp_port}. Reconnecting")
                self.establish_connection(self.udp_ip, self.udp_port)

                self.sock.send(q)
        # TODO: fake printouts


    def open_gripper(self):
        """
        Opens the gripper
        :return: None
        """
        self.robot.open_gripper()


    def close_gripper(self):
        """
        Closes the gripper
        :return: None
        """
        self.robot.close_gripper()


    def goto_pickup(self, item: BaseItem):
        """
        Goes to the pickup location
        :return: None
        """
        self.open_gripper()     # open gripper to pick up object (or keep gripper open)

        robot_pickup_pose = self.robot.ikine_LM(item.pose, q0=self.pose)
        traj = jtraj(self.pose, robot_pickup_pose, 100)

        self.set_pose(traj)
        self.close_gripper()    # close gripper upon object pickup


    def goto_dropoff(self, location: SE3):
        """
        Goes to the dropoff location
        :return: None
        """
        robot_dropoff_pose = self.robot.ikine_LM(location, q0=self.pose)
        traj = jtraj(self.pose, robot_dropoff_pose, 100)

        self.set_pose(traj)
        self.open_gripper()     # open gripper to drop off object


    def pick_and_place(self, item: BaseItem, dropoff_location: SE3):
        """
        Executes a pick-and-place sequence with the robot.
        :param item: The object to be picked up
        :param dropoff_location: The drop-off location for the object
        :return: None
        """
        # Go to object (cube) location
        self.goto_pickup(item)

        # Move to drop-off location
        self.goto_dropoff(dropoff_location)


    def goto_home(self):
        """
        Goes back to initial starting point
        :return: None
        """
        self.close_gripper()     # close gripper for the home state
        self.set_pose(self.robot.qz)


if __name__ == "__main__":
    controller = CytonController(connect=True)
