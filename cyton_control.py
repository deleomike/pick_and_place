import time

from assistant.sensors import MyoGestures, MyoController, LeapController
from assistant.cyton.cyton_connection import CytonConnection
from assistant.cyton.cyton_controller import CytonController
from assistant.scheduler import Scheduler
from assistant.items.Block import Block
from assistant.items.locations import BlockEndLocations


def main():

    ########
    # Plan #
    ########

    blocks = [Block(idx + 1, color="blue", location=e) for idx, e in enumerate(BlockEndLocations)]
    # blocks = [Block(1, color="blue", location=BlockEndLocations.A)]
    scheduler = Scheduler(blocks)

    print("PLAN: ", scheduler.execute())

    ###############
    # Controllers #
    ###############

    client = CytonConnection()

    controller = CytonController(client=client)

    leap = LeapController()
    myo = MyoController()

    leap.start()
    myo.start()

    #################
    # State Machine #
    #################

    state = 'waiting'  # state can be waiting, pickup, inspect, pickup_fail, pickup_succ, drop_loc, drop

    pickup_number = 0
    printed = 0
    number_good_pickup = 0
    number_bad_pickup = 0
    while True:

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
                controller.go_human_show()
                state = 'pickup_success'
                printed = 0

        time.sleep(5)


if __name__ == "__main__":
    main()
