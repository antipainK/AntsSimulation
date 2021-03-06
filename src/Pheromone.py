from __future__ import annotations

from typing import Union

from Position import Position
from PheromoneType import PheromoneType


class Pheromone:
    def __init__(
        self,
        pheromoneType: PheromoneType,
        position: Position,
        startingStrength: int = 150,
    ):
        self.type = pheromoneType
        self.position = position
        self.startingStrength = startingStrength
        self.strength = startingStrength

    def __str__(self):
        return "<Pheromone '{0}': strength={1}, position={2}>".format(
            "Home" if self.type == PheromoneType.HOME else "Trail",
            self.strength,
            self.position.__str__(),
        )


def calculateAveragePheromonePosition(
    pheromones, trackedType
) -> Union[Pheromone, None]:
    # TODO It's not working "great", ants often get stuck looped into each other. Create another way of "deciding".
    x_sum = 0
    y_sum = 0
    strength_sum = 0

    for pheromone in pheromones:
        if pheromone.type == trackedType:
            x_sum += pheromone.position.x * pheromone.strength
            y_sum += pheromone.position.y * pheromone.strength
            strength_sum += pheromone.strength

    if strength_sum == 0:
        return None

    else:
        return Pheromone(
            trackedType,
            Position(x_sum / strength_sum, y_sum / strength_sum),
            strength_sum,
        )


def calculatePheromonesStrength(startingPosition, pheromones, trackedType) -> float:
    strength_sum = 0

    for pheromone in pheromones:
        if pheromone.type == trackedType:
            strength_sum += (
                pheromone.strength
            )  # / max(                1.0, pheromone.position.distanceToObject(startingPosition))

    return strength_sum
