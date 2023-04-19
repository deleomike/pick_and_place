import socket

import numpy as np

import time

from statistics import mode
from pynput import keyboard
from assistant.sensors import MyoController, MyoGestures, LeapController
from assistant.cyton import CytonConnection, CytonController

save_state = "waiting"
space = False


def on_press(key):
    global space
    if key == keyboard.Key.space:
        space ^= True
    else:
        space ^= False




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
        global save_state
        self.set_angles([0, 0, 0, 0, 0, 0, 0, 0.013])
        save_state = "home"
        print("Going to home")

    def go_one_pick(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.013])
        save_state = "one-pick"
        print("Going to one")

    def go_two_pick(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.013])
        save_state = "two-pick"
        print("Going to two")

    def go_three_pick(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.013])
        save_state = "three-pick"
        print("Going to three")

    def go_four_pick(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.013])
        save_state = "four-pick"
        print("Going to four")

    def go_one_place(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.01])
        save_state = "one-place"
        print("Going to one")

    def go_two_place(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
        save_state = "two-place"
        print("Going to two")

    def go_three_place(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.01])
        save_state = "three-place"
        print("Going to three")

    def go_four_place(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
        save_state = "four-place"
        print("Going to four")

    def go_human_show(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([0.0, -0.7, 0.0, -0.7, 0.0, -0.7, 0.0, 0.01])
        save_state = "human-show"
        print("Going to human")

    def go_human_place(self):
        # self.set_pose(self.robot.qz)
        global save_state
        self.set_angles([0.0, -0.7, 0.0, -0.7, 0.0, -0.7, 0.0, 0.01])
        save_state = "human-place"
        print("Going to human")

    def go_intermediate(self):
        self.set_angles([0.33, 0.53, 0.0, 0.82, 0.0, 0.72, 0.0, 0.01])

    def pickup(self):
        if save_state == "one-pick":
            self.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.01])
            print("Picking up cuboid from block 1")

        elif save_state == "two-pick":
            self.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
            print("Picking up cuboid from block 2")

        elif save_state == "three-pick":
            self.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.01])
            print("Picking up cuboid from block 3")

        elif save_state == "four-pick":
            self.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
            print("Picking up cuboid from block 4")

        else:
            print("Command not understood")

    def drop(self):
        if save_state == "one-place":
            self.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.013])
            print("Placing cuboid in block 1")

        elif save_state == "two-place":
            self.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.013])
            print("Placing cuboid in block 2")

        elif save_state == "three-place":
            self.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.013])
            print("Placing cuboid in block 3")

        elif save_state == "four-place":
            self.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.013])
            print("Placing cuboid in block 4")

        elif save_state == "human-drop":
            self.set_angles([0.0, -0.7, 0.0, -0.7, 0.0, -0.7, 0.0, 0.013])
            print("Placing cuboid in operator hand")

        else:
            print("Command not understood")


if __name__ == "__main__":

    client = CytonConnection(send_port=8888, recv_port=8889)

    controller = CytonController(client=client)

    leap = LeapController()
    myo = MyoController()

    leap.start()
    myo.start()

    state = 'waiting'  # state can be waiting, pickup, inspect, pickup_fail, pickup_succ, drop_loc, drop

    pickup_number = 0
    printed = 0
    printed_pause = 0
    number_good_pickup = 0
    number_bad_pickup = 0

    listener = keyboard.Listener(
        on_press=on_press)
    listener.start()


    while True:
        if not space:
            printed_pause = 0
            if state == 'waiting':
                print("waiting for pickup location")
                if leap.finger_mode == 1:
                    controller.go_one_pick()
                elif leap.finger_mode == 2:
                    controller.go_two_pick()
                elif leap.finger_mode == 3:
                    controller.go_three_pick()
                elif leap.finger_mode == 4:
                    controller.go_four_pick()
                if leap.finger_mode == 5 or leap.finger_mode == 0:
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
                    controller.go_human_show()
                    print("waiting for inspection")
                    printed = 1

                if myo.gesture == 4:
                    state = 'pickup_fail'
                    print("Failed pickup")
                    printed = 0
                    number_bad_pickup = number_bad_pickup + 1
                elif myo.gesture == 3:
                    state = 'pickup_success'
                    print("Successful pickup")
                    number_good_pickup = number_good_pickup + 1
                    printed = 0
            elif state == 'pickup_fail':
                if pickup_number == 1:
                    controller.go_one_place()
                elif pickup_number == 2:
                    controller.go_two_place()
                elif pickup_number == 3:
                    controller.go_three_place()
                elif pickup_number == 4:
                    controller.go_four_place()
                state = 'drop'
            elif state == 'pickup_success':
                print("waiting for drop-off location")
                if leap.finger_mode == 1:
                    controller.go_one_place()
                    state = 'drop'
                elif leap.finger_mode == 2:
                    controller.go_two_place()
                    state = 'drop'
                elif leap.finger_mode == 3:
                    controller.go_three_place()
                    state = 'drop'
                elif leap.finger_mode == 4:
                    controller.go_four_place()
                    state = 'drop'
                elif leap.finger_mode == 5:
                    controller.go_human_place()
                    print("Dropping object")
                    controller.drop()
                    time.sleep(1.5)
                    controller.go_home()
                    state = 'waiting'
                    printed = 0
            elif state == 'drop':
                if printed == 0:
                    print("waiting for drop-off approval")
                    printed = 1
                if myo.gesture == 1:
                    print("Dropping object")
                    controller.drop()
                    time.sleep(1.5)
                    controller.go_home()
                    state = 'waiting'
                    printed = 0
                elif myo.gesture == 2:
                    state = 'failed_drop'
                    printed = 0
            elif state == 'failed_drop':
                if printed == 0:
                    print("waiting for new drop-off location")
                    printed = 1
                if leap.finger_mode == 1:
                    controller.go_intermediate()
                    time.sleep(2)
                    controller.go_one_place()
                    state = 'drop'
                    printed = 0
                elif leap.finger_mode == 2:
                    controller.go_intermediate()
                    time.sleep(2)
                    controller.go_two_place()
                    state = 'drop'
                    printed = 0
                elif leap.finger_mode == 3:
                    controller.go_intermediate()
                    time.sleep(2)
                    controller.go_three_place()
                    state = 'drop'
                    printed = 0
                elif leap.finger_mode == 4:
                    controller.go_intermediate()
                    time.sleep(2)
                    controller.go_four_place()
                    state = 'drop'
                    printed = 0
                elif leap.finger_mode == 5:
                    controller.go_intermediate()
                    time.sleep(2)
                    controller.go_human_place()
                    print("Dropping object")
                    controller.drop()
                    time.sleep(1.5)
                    controller.go_home()
                    state = 'waiting'
                    printed = 0
            time.sleep(5)

        else:
            if printed_pause == 0:
                print("Pausing for now")
                printed_pause = 1
            pass

    # controller.set_angles([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0])
    # q = [0, 0.7, 0, 0.7, 0, 0.7, 0, 0.1]
    #
    # controller.set_angles(q)