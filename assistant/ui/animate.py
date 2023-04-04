
from assistant.cyton.cyton import CytonGamma300
from spatialmath import SE3
from assistant.items.BaseItem import BaseItem
from assistant.cyton.cyton_controller import CytonController


def main():
    # Create a CytonGamma300 robot object
    robot = CytonGamma300()

    # Define the starting pose for the robot
    starting_pose = robot.qz

    # Define the list of items and their poses
    cube_locations = [
        BaseItem(pose=SE3([0.5, 0, 0.5])),
        BaseItem(pose=SE3([0.5, 0, 0.6])),
        BaseItem(pose=SE3([0.5, 0, 0.7])),
        BaseItem(pose=SE3([0.5, 0, 0.8])),
        BaseItem(pose=SE3([0.5, 0, 0.9]))
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
    for cube_location, dropoff_location in zip(cube_locations, dropoff_locations):
        controller.pick_and_place(cube_location, dropoff_location)

    # Robot returns home
    controller.goto_home()

    # Disconnect the robot
    robot.disconnect()
    

if __name__ == "__main__":
    main()
