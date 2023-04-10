import socket

import numpy as np

import time
from statistics import mode


class CytonController:
    """
    Management class for performing specific actions with the cyton gamma robot. Also provides an interface for
    sending commands to the robot
    """

    def __init__(self, connect: bool = False):

        self.connect = connect

        self.sock: socket.socket = None
        self.udp_ip = None
        self.udp_port = None

        if self.connect:
            self.establish_connection()

        print(f"Setting starting pose to home")

        self.go_home()

        time.sleep(5)

        # print(f"Setting starting pose to one")
        #
        # self.go_one()
        #
        # time.sleep(5)

        # print(f"Setting starting pose to two")
        #
        # self.go_two()
        #
        # time.sleep(5)
        #
        # print(f"Setting starting pose to three")
        #
        # self.go_three()
        #
        # time.sleep(5)
        #
        # print(f"Setting starting pose to four")
        #
        # self.go_four()
        #
        # time.sleep(5)
        #
        # print(f"Setting starting pose to human")
        #
        # self.go_human()


        # self.set_pose(self.pose)

    # def __del__(self):
    #     self.sock.shutdown()

    def establish_connection(self, udp_ip: str = "127.0.0.1", udp_port: int = 8888) -> bool:
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """
        print(f"Establishing Connection at {udp_ip}:{udp_port}")

        self.udp_ip = udp_ip
        self.udp_port = udp_port

        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        self.sock.connect((self.udp_ip, self.udp_port))


        print("Connection established")

    def set_angles(self, q):
        """
        Sets the pose for the robot. If connected, then it sets the robot's end effector pose.
        :param q: Pose (SE3)
        :return:
        """
        # TODO

        data = np.array(q, dtype=np.double)
        data = data.view(np.uint8)
        print(data)

        if self.connect:
            try:
                self.sock.sendto(data, (self.udp_ip, self.udp_port))
                time.sleep(0.2)

            except Exception as e:
                # recreate the socket and reconnect
                print(f"Error connecting to {self.udp_ip}:{self.udp_port}. Reconnecting")
                self.establish_connection(self.udp_ip, self.udp_port)

                self.sock.send(data)
        # TODO: fake printouts

    # def set_pose(self, P: SE3):

    def go_home(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([0, 0, 0, 0, 0, 0, 0, 0])
        print("Going to home")

    def go_one(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.01])
        print("Going to one")

    def go_two(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
        print("Going to two")

    def go_three(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.01])
        print("Going to three")

    def go_four(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
        print("Going to four")

    def go_human(self):
        # self.set_pose(self.robot.qz)
        self.set_angles([0.0, -0.7, 0.0, -0.7, 0.0, -0.7, 0.0, 0.01])
        print("Going to human")

    def pickup(self):
        pass

    def drop(self):
        pass


class leapController:
    """
    """

    def __init__(self, connect: bool = False):

        self.connect = connect

        self.sock: socket.socket = None
        self.udp_ip = None
        self.udp_port = None

        self.fingers = []
        self.finger_mode = 0

        if self.connect:
            self.establish_connection()

    def establish_connection(self, udp_ip: str = "127.0.0.1", udp_port: int = 5005) -> bool:
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """
        print(f"Establishing Connection at {udp_ip}:{udp_port}")

        self.udp_ip = udp_ip
        self.udp_port = udp_port


    def read_leap(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        self.sock.bind((self.udp_ip, self.udp_port))
        self.fingers = []
        for ii in range(100):
            data, addr = self.sock.recvfrom(1)
            self.fingers.append(data[0])
        self.finger_mode = mode(self.fingers)
        self.sock.close()

class myoController:
    """
    """

    def __init__(self, connect: bool = False):

        self.connect = connect

        self.sock: socket.socket = None
        self.udp_ip = None
        self.udp_port = None

        self.movement = []
        self.movement_mode = 0

        if self.connect:
            self.establish_connection()

    def establish_connection(self, udp_ip: str = "127.0.0.1", udp_port: int = 5006) -> bool:
        """
        Establishes a connection to the robot
        :return: True/False whether the connection was successful
        """
        print(f"Establishing Connection at {udp_ip}:{udp_port}")

        self.udp_ip = udp_ip
        self.udp_port = udp_port


    def read_myo(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP

        self.sock.bind((self.udp_ip, self.udp_port))
        self.movement = []
        for ii in range(5):
            data, addr = self.sock.recvfrom(1)
            self.movement.append(data[0])
        self.movement_mode = mode(self.movement)
        if self.movement_mode == 1:
            print('flexion')
        elif self.movement_mode == 2:
            print('extension')
        elif self.movement_mode == 3:
            print('rest')
        self.sock.close()

if __name__ == "__main__":

    controller = CytonController(connect=True)

    leap = leapController(connect=True)

    myo = myoController(connect=True)

    state = 'waiting'  # state can be waiting, pickup, inspect, pickup_fail, pickup_succ, drop_loc, drop
    pickup_number = 0
    printed = 0
    while True:
        if state == 'waiting':
            print("waiting for pickup location")
            leap.read_leap()
            if leap.finger_mode == 1:
                controller.go_one()
            elif leap.finger_mode == 2:
                controller.go_two()
            elif leap.finger_mode == 3:
                controller.go_three()
            elif leap.finger_mode == 4:
                controller.go_four()
            if leap.finger_mode == 5:
                state = 'waiting'
            else:
                pickup_number = leap.finger_mode
                state = 'pickup'
        elif state == 'pickup':
            controller.pickup()
            print("Going to user for inspection")
            state = 'inspect'
        elif state == 'inspect':
            if printed == 0:
                controller.go_human()
                print("waiting for inspection")
                printed = 1

            myo.read_myo()
            if myo.movement_mode == 1:
                state = 'pickup_fail'
                print("Failed pickup")
                printed = 0
            elif myo.movement_mode == 2:
                state = 'pickup_success'
                print("Successful pickup")
                printed = 0
        elif state == 'pickup_fail':
            if pickup_number == 1:
                controller.go_one()
            elif pickup_number == 2:
                controller.go_two()
            elif pickup_number == 3:
                controller.go_three()
            elif pickup_number == 4:
                controller.go_four()
            state = 'drop'
        elif state == 'pickup_success':
            print("waiting for drop-off location")
            leap.read_leap()
            if leap.finger_mode == 1:
                controller.go_one()
            elif leap.finger_mode == 2:
                controller.go_two()
            elif leap.finger_mode == 3:
                controller.go_three()
            elif leap.finger_mode == 4:
                controller.go_four()
            elif leap.finger_mode == 5:
                controller.go_human()
            state = 'drop'
        elif state == 'drop':
            if printed == 0:
                print("waiting for dropoff approval")
                printed = 1
            myo.read_myo()
            if myo.movement_mode == 2:
                print("Dropping object")
                controller.drop()
                controller.go_home()
                state = 'waiting'
                printed = 0

        time.sleep(5)



    # controller.set_angles([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0])
    # q = [0, 0.7, 0, 0.7, 0, 0.7, 0, 0.1]
    #
    # controller.set_angles(q)