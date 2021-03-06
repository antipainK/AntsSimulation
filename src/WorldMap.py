from __future__ import annotations

from typing import Union

from Food import Food
import Pheromone
import Ant
import Position
import numpy as np

from quadTree.Rectangle import Rectangle
from quadTree.QuadTree import QuadTree


class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.boundary = Rectangle(width / 2, height / 2, width, height)
        self.pheromones = QuadTree(self.boundary)
        self.ants = []
        self.foods = QuadTree(self.boundary)
        self.nestPosition = Position.Position(0, 0)

    @classmethod
    def emptyObject(self) -> WorldMap:
        return WorldMap(0, 0)

    def __str__(self):
        return "<WorldMap: width={0}, height={1}, pheromonesAmount={2}, antsAmount={3}, foodsAmount={4}>".format(
            self.width,
            self.height,
            len(self.pheromones),
            len(self.ants),
            len(self.foods),
        )

    def getPheromonesInCircle(
        self, startingPoint: Position.Position, range: float
    ) -> list:
        queriedPheromones = []
        self.pheromones.query_radius(
            (startingPoint.x, startingPoint.y), range, found_objects=queriedPheromones
        )
        return queriedPheromones

    def addPheromones(self, pheromone: Pheromone.Pheromone) -> None:
        self.pheromones.insert(pheromone)

    def updatePheromones(self) -> None:
        """
        Iterate over the pheromones and decrease their strength. Delete those, whose strength is 0 or less.
        """

        def deleteOldPheromones(objectA: Pheromone):
            return objectA.strength <= 0

        pheromonesToDiscard = []
        foundPheromones = []
        self.pheromones.query(
            self.boundary,
            found_objects=foundPheromones,
            delete_condition_function=deleteOldPheromones,
        )
        for pheromone in foundPheromones:
            pheromone.strength -= 1

            if pheromone.strength <= 0:
                pheromonesToDiscard.append(pheromone)

    def addAnt(self, ant: Ant.Ant) -> None:
        self.ants.append(ant)

    def limitAntPosition(self, ant: Ant.Ant) -> None:
        # Limit the position by map borders.
        wantedPosition = ant.position
        realisticPosition = Position.Position(
            min(max(wantedPosition.x, 0), self.width),
            min(max(wantedPosition.y, 0), self.height),
        )
        if (
            realisticPosition.x != wantedPosition.x
            or realisticPosition.y != wantedPosition.y
        ):
            ant.direction = wantedPosition.angleToPoint(realisticPosition)
            # ant.direction = np.random.uniform(low=-np.pi, high=np.pi)
        ant.position = realisticPosition

    def leapAntPosition(self, ant: Ant.Ant) -> None:
        """If an Ant went over the border, teleport it to the other side of the map."""
        wantedPosition = ant.position
        realisticPosition = Position.Position(
            wantedPosition.x % self.width,
            wantedPosition.y % self.height,
        )
        ant.position = realisticPosition

    def spawnFoodClump(
        self, position: Position.Position, amount: int, recoil: float = 25.0
    ) -> None:
        for _ in range(amount):
            food_position = position.copy().add(
                np.random.uniform(low=-recoil, high=recoil),
                np.random.uniform(low=-recoil, high=recoil),
            )
            self.foods.insert(Food(food_position))

    def getFoodInRadius(
        self, midpoint: Position.Position, radius: float, pop: bool = False
    ) -> Union[Food, None]:
        """
        Searches for the food around the `midpoint` position and if it finds any, it deletes it from the `QuadTree` structure and returns it.
        :param midpoint: The center of a circle that will be queried.
        :param radius: The radius of the queried circle.
        :return: The found `Food` object or `None` if there isn't any.
        """
        food = []
        if self.foods.query_radius(
            (midpoint.x, midpoint.y), radius, found_objects=food, findAmount=1, pop=pop
        ):
            return food[0]
        return None
