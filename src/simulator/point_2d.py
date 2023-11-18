from dataclasses import dataclass


@dataclass(frozen=True)
class Point2D:
    x: float
    y: float
