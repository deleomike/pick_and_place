
import enum

NUM_BLOCKS = 5


# TODO: Program the q vectors from the static robot class
class RobotSpecialLocations(enum.Enum):
    SHOW = 1
    HOME = 2


# TODO: Program the relative pose here from the robot
class BlockStartLocations(enum.Enum):
    B1 = 1
    B2 = 2
    B3 = 3
    B4 = 4
    B5 = 5


# TODO: Program the relative pose here from the robot
class BlockEndLocations(enum.Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5


if __name__ == "__main__":
    loc = BlockStartLocations.B5

    print(loc.name)
