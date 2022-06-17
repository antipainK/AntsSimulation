from Ant import Ant
from Position import Position
import WorldMap


class Nest:
    def __init__(self, position: Position, radius: float, worldMap: WorldMap.WorldMap, antsToSpawn: int=0):
        self.position = position
        self.worldMap = worldMap
        self.radius = radius
        self.antsToSpawn = antsToSpawn
        self.lifeCounter = 4

    @classmethod
    def emptyObject(self):
        return Nest(None, None, None, None)

    def __str__(self):
        return "<Nest: radius={0}, position={1}>".format(
            self.radius, self.position.__str__()
        )

    def update(self):
        # for every ant in radius - take it from the Map class
        # execute ant.putDownFood()
        ants = self.worldMap.ants
        for ant in ants:
            if ant.holding_food:
                if self.position.distanceToObject(ant.position) < self.radius:
                    ant.putDownFood()
                    print(ant)

        self.lifeCounter += 1
        if self.lifeCounter % 4 == 0:
            self.spawnAnt()

    def spawnAnt(self):
        self.worldMap.addAnt(Ant(self.position, self.worldMap))
