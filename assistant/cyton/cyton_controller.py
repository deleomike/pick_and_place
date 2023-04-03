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

    def go_home(self):
        self.set_pose(self.robot.qz)

    def grab_object(self, item: BaseItem):
        robot_object_pose = self.robot.ikine_LM(item.pose, q0=self.pose)

        traj = jtraj(self.pose, robot_object_pose, 100)


if __name__ == "__main__":

    controller = CytonController(connect=True)