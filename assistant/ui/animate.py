
from spatialmath import SE3

from assistant.cyton import CytonController, CytonGamma300, CytonConnection
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

    start_positions = [SE3([0.1, 0, i/100]) for i in range(5)]
    end_positions = [SE3([0.1, i/100, 0]) for i in range(5)]

    # Define the list of cubes and their properties
    cubes = [Block(pos_id=idx, width=width, height=height, length=length, pose=position) for idx, position in enumerate(start_positions)]
    # cubes = [
    #     Block(pos_id=1,width=width,height=height,length=length,pose=SE3([0.1, 0, -0.08])),
    #     Block(pos_id=2,width=width,height=height,length=length,pose=SE3([0.1, 0, -0.075])),
    #     Block(pos_id=3,width=width,height=height,length=length,pose=SE3([0.1, 0, 0.0])),
    #     Block(pos_id=4,width=width,height=height,length=length,pose=SE3([0.1, 0, 0.075])),
    #     Block(pos_id=5,width=width,height=height,length=length,pose=SE3([0.1, 0, 0.15]))
    # ]

    # Define the list of drop-off locations
    dropoff_locations = [
        SE3([0, -0.15, 0.1]),
        SE3([0, -0.075, 0.1]),
        SE3([0, 0.0, 0.1]),
        SE3([0, 0.075, 0.1]),
        SE3([0, 0.15, 0.1])
    ]

    client = CytonConnection()

    # Create a CytonController instance and establish a connection
    controller = CytonController(robot=robot, client=client)

    # Loop through the items and their drop-off locations, and execute the pick-and-place sequence for each item
    for cube, dropoff_location in zip(cubes, end_positions):
        controller.pick_and_place(cube, dropoff_location)

    # Robot returns home
    controller.go_home()

    # Disconnect the robot
    controller.disconnect()


if __name__ == "__main__":
    main()
