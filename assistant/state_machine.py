import time

from enum import Enum
from pynput import keyboard
from assistant.cyton import CytonConnection, CytonController
from assistant.sensors import LeapController, MyoController, MyoGestures


class State(Enum):
    WAITING = "waiting"
    PICKUP = "pickup"


class PickPlaceStateMachine:

    def __init__(self,
                 controller: CytonController,
                 leap_controller: LeapController,
                 myo_controller: MyoController):

        self.controller = controller
        self.leap = leap_controller
        self.myo = myo_controller
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

        self.keyboard_listener.start()
        self.leap.start()
        self.myo.start()

        self.state = "waiting"
        # TODO: What is the difference between save state and state?
        self.save_state = self.state
        self.space = False

        self.pickup_number: int = 0
        self.printed: bool = False
        self.printed_pause: bool = False
        self.number_good_pickup: int = 0
        self.number_bad_pickup: int = 0

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.controller.disconnect()
        self.leap.stop()
        self.myo.stop()

    def on_press(self, key):
        if key == keyboard.Key.space:
            self.space ^= True
        else:
            self.space ^= False

    def run(self):
        try:
            self._state_machine_loop_()
        except KeyboardInterrupt:
            print("Caught CTRL+C. Shutting Down.")
            self.disconnect()

    def _state_machine_loop_(self):

        while True:

            if not self.space:
                self.printed_pause = False

                if self.state == 'waiting':
                    print("waiting for pickup location")
                    if self.leap.finger_mode == 1:
                        self.go_one_pick()
                    elif self.leap.finger_mode == 2:
                        self.go_two_pick()
                    elif self.leap.finger_mode == 3:
                        self.go_three_pick()
                    elif self.leap.finger_mode == 4:
                        self.go_four_pick()
                    if self.leap.finger_mode == 5 or self.leap.finger_mode == 0:
                        self.state = 'waiting'
                    else:
                        self.pickup_number = self.leap.finger_mode
                        self.state = 'pickup'

                elif self.state == 'pickup':
                    self.pickup()
                    print("Going to user for inspection")
                    self.state = 'inspect'

                elif self.state == 'inspect':
                    if not self.printed:
                        self.go_human_show()
                        print("waiting for inspection")
                        self.printed = True
                    if self.myo.gesture == MyoGestures.WRIST_OUT:
                        self.state = 'pickup_fail'
                        print("Failed pickup")
                        self.printed = False
                        self.number_bad_pickup = self.number_bad_pickup + 1
                    elif self.myo.gesture == MyoGestures.WRIST_IN:
                        self.state = 'pickup_success'
                        print("Successful pickup")
                        self.number_good_pickup = self.number_good_pickup + 1
                        self.printed = True

                elif self.state == 'pickup_fail':

                    if self.pickup_number == 1:
                        self.go_one_place()
                    elif self.pickup_number == 2:
                        self.go_two_place()
                    elif self.pickup_number == 3:
                        self.go_three_place()
                    elif self.pickup_number == 4:
                        self.go_four_place()
                    self.state = 'drop'

                elif self.state == 'pickup_success':
                    print("waiting for drop-off location")

                    if self.leap.finger_mode == 1:
                        self.go_one_place()
                        self.state = 'drop'
                    elif self.leap.finger_mode == 2:
                        self.go_two_place()
                        self.state = 'drop'
                    elif self.leap.finger_mode == 3:
                        self.go_three_place()
                        self.state = 'drop'
                    elif self.leap.finger_mode == 4:
                        self.go_four_place()
                        self.state = 'drop'
                    elif self.leap.finger_mode == 5:
                        self.go_human_place()
                        print("Dropping object")
                        self.drop()
                        time.sleep(1.5)
                        self.go_home()
                        self.state = 'waiting'
                        self.printed = False

                elif self.state == 'drop':
                    if not self.printed:
                        print("waiting for drop-off approval")
                        self.printed = True
                    if self.myo.gesture == MyoGestures.FLEXION:
                        print("Dropping object")
                        self.drop()
                        time.sleep(1.5)
                        self.controller.go_home()
                        self.state = 'waiting'
                        self.printed = False
                    elif self.myo.gesture == MyoGestures.EXTENSION:
                        self.state = 'failed_drop'
                        self.printed = False

                elif self.state == 'failed_drop':
                    if not self.printed:
                        print("waiting for new drop-off location")
                        self.printed = True
                    if self.leap.finger_mode == 1:
                        self.go_intermediate()
                        time.sleep(2)
                        self.go_one_place()
                        self.state = 'drop'
                        self.printed = False
                    elif self.leap.finger_mode == 2:
                        self.go_intermediate()
                        time.sleep(2)
                        self.go_two_place()
                        self.state = 'drop'
                        self.printed = False
                    elif self.leap.finger_mode == 3:
                        self.go_intermediate()
                        time.sleep(2)
                        self.go_three_place()
                        self.state = 'drop'
                        self.printed = False
                    elif self.leap.finger_mode == 4:
                        self.go_intermediate()
                        time.sleep(2)
                        self.go_four_place()
                        self.state = 'drop'
                        self.printed = False
                    elif self.leap.finger_mode == 5:
                        self.go_intermediate()
                        time.sleep(2)
                        self.go_human_place()
                        print("Dropping object")
                        self.drop()
                        time.sleep(1.5)
                        self.go_home()
                        self.state = 'waiting'
                        self.printed = False
                time.sleep(5)

            else:
                if not self.printed_pause:
                    print("Pausing for now")
                    self.printed_pause = True

    def go_home(self):

        self.controller.go_home()
        self.save_state = "home"
        print("Going to home")

    def go_one_pick(self):
        self.controller.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.013])
        self.save_state = "one-pick"
        print("Going to one")

    def go_two_pick(self):
        self.controller.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.013])
        self.save_state = "two-pick"
        print("Going to two")

    def go_three_pick(self):
        self.controller.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.013])
        self.save_state = "three-pick"
        print("Going to three")

    def go_four_pick(self):
        self.controller.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.013])
        self.save_state = "four-pick"
        print("Going to four")

    def go_one_place(self):
        self.controller.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.01])
        self.save_state = "one-place"
        print("Going to one")

    def go_two_place(self):
        self.controller.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
        self.save_state = "two-place"
        print("Going to two")

    def go_three_place(self):
        self.controller.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.01])
        self.save_state = "three-place"
        print("Going to three")

    def go_four_place(self):
        self.controller.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
        self.save_state = "four-place"
        print("Going to four")

    def go_human_show(self):
        self.controller.set_angles([0.0, -0.7, 0.0, -0.7, 0.0, -0.7, 0.0, 0.01])
        self.save_state = "human-show"
        print("Going to human")

    def go_human_place(self):
        self.controller.set_angles([0.0, -0.7, 0.0, -0.7, 0.0, -0.7, 0.0, 0.01])
        self.save_state = "human-place"
        print("Going to human")

    def go_intermediate(self):
        self.controller.set_angles([0.33, 0.53, 0.0, 0.82, 0.0, 0.72, 0.0, 0.01])

    def pickup(self):
        if self.save_state == "one-pick":
            self.controller.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.01])
            print("Picking up cuboid from block 1")

        elif self.save_state == "two-pick":
            self.controller.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
            print("Picking up cuboid from block 2")

        elif self.save_state == "three-pick":
            self.controller.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.01])
            print("Picking up cuboid from block 3")

        elif self.save_state == "four-pick":
            self.controller.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.01])
            print("Picking up cuboid from block 4")

        else:
            print("Command not understood")

    def drop(self):
        if self.save_state == "one-place":
            self.controller.set_angles([1.058, 1.061, 0.0, 1.309, 0.0, 0.811476, 0.0, 0.013])
            print("Placing cuboid in block 1")

        elif self.save_state == "two-place":
            self.controller.set_angles([0.557, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.013])
            print("Placing cuboid in block 2")

        elif self.save_state == "three-place":
            self.controller.set_angles([0.0, 0.979, 0.0, 1.46989, 0.0, 0.811476, 0.0, 0.013])
            print("Placing cuboid in block 3")

        elif self.save_state == "four-place":
            self.controller.set_angles([-0.5011, 1.0612, 0.0, 1.309, 0.0, 0.725, 0.0, 0.013])
            print("Placing cuboid in block 4")

        elif self.save_state == "human-drop":
            self.controller.set_angles([0.0, -0.7, 0.0, -0.7, 0.0, -0.7, 0.0, 0.013])
            print("Placing cuboid in operator hand")

        else:
            print("Command not understood")


if __name__ == "__main__":
    client = CytonConnection()

    controller = CytonController(client=client)

    leap = LeapController()
    myo = MyoController()

    #################
    # State Machine #
    #################

    state_machine = PickPlaceStateMachine(controller=controller, leap_controller=leap, myo_controller=myo)

    state_machine.run()