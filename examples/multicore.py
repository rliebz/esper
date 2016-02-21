import esper
import random
import time


#################################
# Define some generic components:
#################################
class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


##########################
#  Define some Processors:
##########################
class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            pos.x += vel.x
            pos.y += vel.y
            print("Local", vel.y)


class GravityProcessor(esper.ParallelProcessor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, vel in self.world.get_component(Velocity):
            vel.y *= 0.98
            print("Core2", vel.y)


###############
#  Helper utils
###############
def create_entities(world, number):
    for _ in range(number // 2):
        enemy = world.create_entity()
        world.add_component(enemy, Position(x=random.randint(0, 500), y=random.randint(0, 500)))
        world.add_component(enemy, Velocity())


if __name__ == "__main__":
    world = esper.World()
    create_entities(world, 55)

    movement_proc = MovementProcessor()
    # gravity_proc = GravityProcessor()

    world.add_processor(movement_proc)
    # world.add_processor(gravity_proc)
    world.process()

    time.sleep(3)
