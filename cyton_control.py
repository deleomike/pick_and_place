from assistant.sensors import MyoController, LeapController
from assistant.cyton.cyton_connection import CytonConnection
from assistant.cyton.cyton_controller import CytonController
from assistant.scheduler import Scheduler
from assistant.items.Block import Block
from assistant.items.locations import BlockEndLocations
from assistant.state_machine import PickPlaceStateMachine


def main():

    ########
    # Plan #
    ########

    # blocks = [Block(idx + 1) for idx, e in enumerate(BlockEndLocations)]
    # # blocks = [Block(1, color="blue", location=BlockEndLocations.A)]
    # scheduler = Scheduler(blocks)
    #
    # print("PLAN: ", scheduler.execute())

    ###############
    # Controllers #
    ###############

    client = CytonConnection()

    controller = CytonController(client=client)

    leap = LeapController()
    myo = MyoController()

    #################
    # State Machine #
    #################

    state_machine = PickPlaceStateMachine(controller=controller, leap_controller=leap, myo_controller=myo)

    state_machine.run()


if __name__ == "__main__":
    main()
