
from spatialmath import SE3

from assistant.cyton.cyton import CytonGamma300
from assistant.cyton.cyton_controller import CytonController
from assistant.items.Block import Block


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
        Block(pos_id=1,width=width,height=height,length=length,pose=SE3([0.5, 0, 0.5])),
        Block(pos_id=2,width=width,height=height,length=length,pose=SE3([0.5, 0, 0.6])),
        Block(pos_id=3,width=width,height=height,length=length,pose=SE3([0.5, 0, 0.7])),
        Block(pos_id=4,width=width,height=height,length=length,pose=SE3([0.5, 0, 0.8])),
        Block(pos_id=5,width=width,height=height,length=length,pose=SE3([0.5, 0, 0.9]))
    ]

    # Define the list of drop-off locations
    dropoff_locations = [
        SE3([0, 0.5, 0.5]),
        SE3([0, 0.6, 0.5]),
        SE3([0, 0.7, 0.5]),
        SE3([0, 0.8, 0.5]),
        SE3([0, 0.9, 0.5])
    ]

    # Create a CytonController instance and establish a connection
    controller = CytonController(robot=robot, starting_pose=starting_pose, connect=True)

    # Loop through the items and their drop-off locations, and execute the pick-and-place sequence for each item
    for cube, dropoff_location in zip(cubes, dropoff_locations):
        controller.pick_and_place(cube, dropoff_location)

    # Robot returns home
    controller.goto_home()

    # Disconnect the robot
    robot.disconnect()


if __name__ == "__main__":
    main()
