import numpy as np
import WorldMap
from Pheromone import getUnitedPheromoneAtCenterOfGravity
import Position
import math
from PheromoneType import PheromoneType

# sigma in normal distribution
RANDOMNESS_SIGMA = 0.3


class Ant:
    def __init__(self, position: Position, worldMap: WorldMap):
        self.position = position
        self.seeing_angle = 60
        self.walking_speed = 100
        self.direction = 0
        self.eating_radius = 0.5
        self.seeing_radius = 3
        # self.age = 0
        self.speed = 1
        self.holding_food = False
        self.worldMap = worldMap

    def update(self):
        # Na podstawie czy self.holding_food = True - wybierz kierunek do domu lub kierunek do jedzenia
        # Rusz się self.move(kierunek)
        # Spróbuj podnieść jedzenie
        self.tryToTakeFood()
        # Na podstawie tego, czy TERAZ masz jedzenie, stwórz odpowiedniego feromona
        self.move(self.decide())

        if self.holding_food:
            self.mark_food_trail()
        else:
            self.mark_return_trail()

        # self.age +=1
        pass

    def setMap(self, worldMap: WorldMap):
        self.worldMap = worldMap

    def decide(self):
        # take self.holding_food = False into consideration
        if self.holding_food:
            pheromoneToTrack = PheromoneType.HOME
        else:
            pheromoneToTrack = PheromoneType.TRAIL

        # Detect pheromones in cone shape in front of the ant.
        # Take the angle from ant's `self.sense_angle`.
        sensedPheromones = self.worldMap.getPheromonesInCircularSector()
        centerOfPheromones = calculateAveragePheromonePosition(
            detectedPheromones, pheromoneToTrack
        )

        pheromoneAngle = self.position.angleToPoint(pheromoneCenter.position)
        weightedNormalDistributionSigma = RANDOMNESS_SIGMA / pheromoneCenter.strength

        randomizedAngle = (
            np.random.normal(pheromoneAngle, weightedNormalDistributionSigma, 1)
            * math.pi
        )
        # Roll a dice and depending on the result:
        # Go right
        # Go left
        # Go towards the center of trail pheromones (towards food)
        # - this option should have the biggest chance of happening
        # If you have food go towards the center of "return to base pheromones"

        # Return the angle of "desired movement"
        # Use this getPheromonesInCircularSector(self, startingPoint, direction, range)

        return randomizedAngle

    def move(self, direction):

        moveAngle = self.direction + self.decide()
        newPosition = Position(
            oldPosition.x + self.speed * math.cos(moveAngle),
            oldPosition.y + self.speed * math.sin(moveAngle),
        oldPosition = self.position
        )
        self.position = newPosition

        # wywołaj move na mapie

        # (Possible in the future) Check for obstacles on your path.

        # Create a "move" vector depending on the "direction" and "walking_speed" constant.
        # The "walking_speed" depends on whether the ant holds food.
        # (Possible in the future) The "walking_speed" depends on the ant's age.
        # (Possible in the future) The "walking_speed" depends on the angle of the terrain.
        # (Possible in the future) The "walking_speed" depends on the wind.

        # Spawn a "ReturnPheromone" or "FoodPheromone" depending on the current state of "holding_food".
        if self.holding_food:
            self.mark_food_trail()
        else:
            self.mark_return_trail()

        # self.map.updateAntPosition(self, wantedPosition)
        pass

    def mark_food_trail(self):
        # Invoke when you have found food.
        # It will be used in order for other ants to find the food more optimally.

        # Spawn a "FoodPheromone" object.
        # This object will have lifespan that will gradually go down until it disappears.

        # self.map.addPheromone(typ ...
        pass

    def mark_return_trail(self):
        # Invoke when you are looking for food.
        # It will be used in order to find optimal return path to the nest.

        # Spawn a "ReturnPheromone" object.
        # This object will have lifespan that will gradually go down until it disappears.
        # self.map.addPheromone(typ ...
        pass

    def tryToTakeFood(self):
        # foodToEat = self.map.getFoodInRadius(self, position:Position, radius:float)
        # if the foodToEat is not null - change your type to "carrying food= true"
        # else do nothing
        foodToEat = self.worldMap.getFoodInRadius(self.position, self.radius)

        if foodToEat:
            self.holding_food = True

    def putDownFood(self):
        self.holding_food = False
