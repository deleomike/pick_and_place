
from spatialmath import SE3

from assistant.cyton import CytonController, CytonGamma300, CytonConnection
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

    start_positions = [SE3([0.1, 0, i/100]) for i in range(5)]
    end_positions = [SE3([0.1, i/100, 0]) for i in range(5)]

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

    client = CytonConnection()

    # Create a CytonController instance and establish a connection
    controller = CytonController(robot=robot, client=client)

    # Loop through the items and their drop-off locations, and execute the pick-and-place sequence for each item
    for cube in cubes:
        controller.pick_and_place(cube)

    # Robot returns home
    controller.go_home()

    # Disconnect the robot
    controller.disconnect()


if __name__ == "__main__":
    main()
