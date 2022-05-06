import numpy as np
import WorldMap
from Pheromone import calculateAveragePheromonePosition, Pheromone
import Position
import math
from PheromoneType import PheromoneType

# sigma in normal distribution
RANDOMNESS_SIGMA = 0.3


class Ant:
    def __init__(self, position: Position, worldMap: WorldMap):
        self.position = position
        self.direction = np.random.uniform(low=-np.pi, high=np.pi)
        self.walkingSpeed = 5

        self.seeing_radius = 80
        self.seeing_angle = 60

        self.eating_radius = 4
        self.holding_food = False
        self.worldMap = worldMap


    def __str__(self):
        return "<Ant: walkingSpeed={0}, direction={1}, seeingRadius={2}, seeingAngle={3}, eatingRadius={4}, holdingFood={5}, lifeCounter={6}, position={7}>".format(self.walkingSpeed, self.direction, self.seeing_radius, self.seeing_angle, self.eating_radius, self.holding_food, self.lifeCounter, self.position.__str__())

    def update(self):
        # Na podstawie czy self.holding_food = True - wybierz kierunek do domu lub kierunek do jedzenia
        # Rusz się self.move(kierunek)
        # Spróbuj podnieść jedzenie
        self.tryToTakeFood()
        # Na podstawie tego, czy TERAZ masz jedzenie, stwórz odpowiedniego feromona
        self.move(self.decide())

        self.mark_pheromones()

    def decide(self):
        """
        Calculate an angle with a bit of randomness. Moving in this direction should yield a big chance of encountering the requested type of `Pheromones`.
        """

        # Base your decision on whether you're holding food or not.
        # If you are, then you should try to find a way to the nest.
        # Otherwise, try to find a way to get closer to the food.

        # Detect pheromones in circular sector shape in front of the ant.
        detectedPheromones = self.worldMap.getPheromonesInCircularSector(
            self.position, self.direction, self.seeing_radius, self.seeing_angle
        )

        # Calculate the "center of strength" (center of mass) of the pheromones. Filter by your state ("holding_food").
        if self.holding_food:
            pheromoneToTrack = PheromoneType.HOME
        else:
            pheromoneToTrack = PheromoneType.TRAIL

        centerOfPheromones = calculateAveragePheromonePosition(
            detectedPheromones, pheromoneToTrack
        )

        if centerOfPheromones is not None:
            weightedNormalDistributionSigma = (
                RANDOMNESS_SIGMA / centerOfPheromones.strength
            )
            return (
                np.random.normal(
                    self.position.angleToPoint(centerOfPheromones.position),
                    weightedNormalDistributionSigma,
                    1,
                )
                * math.pi
            )

        else:
            return self.direction + np.random.uniform(low=-np.pi / 2, high=np.pi / 2)
        # Roll a dice and depending on the result:
        # Go right
        # Go left
        # Go towards the center of trail pheromones (towards food)
        # - this option should have the biggest chance of happening
        # If you have food go towards the center of "return to base pheromones"

        # Return the angle of "desired movement"
        # Use this getPheromonesInCircularSector(self, startingPoint, direction, range)

    def move(self, moveDirection):
        self.position.add(
            self.walkingSpeed * math.cos(moveDirection),
            self.walkingSpeed * math.sin(moveDirection),
        )
        self.worldMap.limitAntPosition(self)
        self.direction = moveDirection

        # wywołaj move na mapie

        # (Possible in the future) Check for obstacles on your path.

        # Create a "move" vector depending on the "direction" and "walking_speed" constant.
        # The "walking_speed" depends on whether the ant holds food.
        # (Possible in the future) The "walking_speed" depends on the ant's age.
        # (Possible in the future) The "walking_speed" depends on the angle of the terrain.
        # (Possible in the future) The "walking_speed" depends on the wind.

        # Spawn a "ReturnPheromone" or "FoodPheromone" depending on the current state of "holding_food".

        # self.map.updateAntPosition(self, wantedPosition)
        pass

    def mark_pheromones(self):
        if self.holding_food:
            self.mark_food_trail()
        else:
            self.mark_return_trail()

    def mark_food_trail(self):
        self.worldMap.addPheromones(Pheromone(PheromoneType.TRAIL, self.position))
        # Invoke when you have found food.
        # It will be used in order for other ants to find the food more optimally.

        # Spawn a "FoodPheromone" object.
        # This object will have lifespan that will gradually go down until it disappears.

        # self.map.addPheromone(typ ...
        pass

    def mark_return_trail(self):
        self.worldMap.addPheromones(Pheromone(PheromoneType.HOME, self.position))
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
        foodToEat = self.worldMap.getFoodInRadius(self.position, self.eating_radius)

        if foodToEat:
            self.holding_food = True

    def putDownFood(self):
        self.holding_food = False
