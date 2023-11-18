from dataclasses import dataclass

from .point_2d import Point2D


class Sector:
    @dataclass(frozen=True)
    class Boundary:
        boundary: float
        inclusive: bool

    def __init__(
        self,
        name: str,
        x_lower: Boundary,
        x_upper: Boundary,
        y_lower: Boundary,
        y_upper: Boundary,
    ) -> None:
        """
        Initializes a sector with the specified bounds.

        :param x_lower: The lower x bound of the sector.
        :param x_upper: The upper x bound of the sector.
        :param y_lower: The lower y bound of the sector.
        :param y_upper: The upper y bound of the sector.
        """
        self.x_lower = x_lower
        self.x_upper = x_upper
        self.y_lower = y_lower
        self.y_upper = y_upper
        self.name = name

        # Validate the sector bounds
        if x_lower.boundary > x_upper.boundary or y_lower.boundary > y_upper.boundary:
            raise ValueError("Invalid sector bounds")

    def contains(self, point: Point2D) -> bool:
        """
        Determines if an object is within the bounds of the sector.

        :param obj: The object to check.
        :return: True if the object is within the sector, False otherwise.
        """

        contains = True
        if self.x_lower.inclusive:
            if point.x < self.x_lower.boundary:
                contains = False
        else:
            if point.x <= self.x_lower.boundary:
                contains = False

        if self.x_upper.inclusive:
            if point.x > self.x_upper.boundary:
                contains = False
        else:
            if point.x >= self.x_upper.boundary:
                contains = False

        if self.y_lower.inclusive:
            if point.y < self.y_lower.boundary:
                contains = False
        else:
            if point.y <= self.y_lower.boundary:
                contains = False

        if self.y_upper.inclusive:
            if point.y > self.y_upper.boundary:
                contains = False
        else:
            if point.y >= self.y_upper.boundary:
                contains = False

        return contains
