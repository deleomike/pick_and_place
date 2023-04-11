
from spatialmath import SE3

from assistant.cyton.cyton import CytonGamma300
from assistant.cyton.cyton_controller import CytonController
from assistant.items.Block import Block
from assistant.items.locations import *
from assistant.items.poses import poses


def main():
    # Create a CytonGamma300 robot object
    robot = CytonGamma300()

    # Define the starting pose for the robot
    starting_pose = robot.qz

    # Define the block dimensions (in meters)
    width = 0.022098    # or 0.87 inches (by inspection)
    height = 0.022098   # or 0.87 inches (by inspection)
    length = 0.022098   # or 0.87 inches (by inspection)

    # Define the list of cubes and their properties
    cubes = [
        Block(pos_id=1,
              location=loc_1,
              pose=poses[0],
              width=width,
              height=height,
              length=length),
        Block(pos_id=2,
              location=loc_2,
              pose=poses[1],
              width=width,
              height=height,
              length=length),
        Block(pos_id=3,
              location=loc_3,
              pose=poses[2],
              width=width,
              height=height,
              length=length),
        Block(pos_id=4,
              location=loc_4,
              pose=poses[3],
              width=width,
              height=height,
              length=length),
        Block(pos_id=5,
              location=loc_5,
              pose=poses[4],
              width=width,
              height=height,
              length=length)
    ]

    # Create a CytonController instance and establish a connection
    controller = CytonController(robot=robot, starting_pose=starting_pose, connect=True)

    # Loop through the items and their drop-off locations, and execute the pick-and-place sequence for each item
    for cube in cubes:
        controller.pick_and_place(cube)

    # Robot returns home
    controller.goto_home()

    # Disconnect the robot
    robot.disconnect()


if __name__ == "__main__":
    main()
