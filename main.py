from assistant.cyton.cyton import CytonGamma300
from assistant.cyton.cyton_controller import CytonController
from assistant.scheduler import Scheduler
from assistant.items.Block import Block
from assistant.items.locations import BlockEndLocations

blocks = [Block(idx + 1, color="blue", location=e) for idx, e in enumerate(BlockEndLocations)]
# blocks = [Block(1, color="blue", location=BlockEndLocations.A)]
scheduler = Scheduler(blocks)

print("PLAN: ", scheduler.execute())