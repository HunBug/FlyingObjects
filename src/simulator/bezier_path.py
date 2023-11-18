import math
from datetime import datetime, timedelta
from typing import Optional

from .point_2d import Point2D


class BezierPath:
    def __init__(self, start: Point2D, end: Point2D, control_point: Point2D):
        self.start = start  # TODO add immutable property
        self.end = end  # TODO add immutable property
        self.control_point = control_point  # TODO add immutable property

        self._length: Optional[float] = None

    def get_length(self) -> float:  # TODO add property decorator
        """
        Get the length of the Bezier curve.

        :return: The length of the curve.
        """
        if self._length is None:
            self._length = self._calculate_length()  # TODO add resuluion parameter
        return self._length

    def _calculate_length(self, num_segments: int = 100) -> float:
        """
        Approximate the length of a quadratic Bezier curve by dividing it into small segments.

        :param steps: The number of segments to divide the curve into for approximation.
        :return: The approximate length of the curve.
        """
        length = 0
        previous_point = self.start

        for step in range(1, num_segments + 1):
            t = step / num_segments
            current_point, _ = self._quadratic_bezier(t)
            length += math.dist(
                [previous_point.x, previous_point.y], [current_point.x, current_point.y]
            )
            previous_point = current_point

        return length

    def calculate_arrive_time(self, start_time: datetime, speed: float) -> datetime:
        """
        Calculate the expiration time for the object to reach its destination.

        :param start_time: The time when the object starts moving.
        :param initial_position: The initial position (x, y) of the object.
        :param control_point: The waypoint (x, y) for the Bezier curve.
        :param destination: The destination (x, y) of the object.
        :param speed: The speed of the object in units/s.
        :return: The expiration time.
        """
        total_distance = self.get_length()
        travel_time = total_distance / speed
        expire_time = start_time + timedelta(seconds=travel_time)
        return expire_time

    def calculate_position_and_angle(
        self, start_time: datetime, current_time: datetime, speed: float
    ) -> tuple[Point2D, float]:
        """
        Calculate the object's current position on its path.

        :param start_time: The time when the object starts moving.
        :param current_time: The current time.
        :param initial_position: The initial position (x, y) of the object.
        :param control_point: The waypoint (x, y) for the Bezier curve.
        :param destination: The destination (x, y) of the object.
        :param speed: The speed of the object in units/s.
        :return: The current position (x, y) of the object.
        """
        total_distance = self.get_length()
        # Time elapsed since the start of the movement
        time_elapsed = current_time - start_time

        # Calculate how far along the path the object should be
        # distance_covered = time_elapsed.microseconds * speed / 1000000
        distance_covered = time_elapsed.total_seconds() * speed
        distance_covered = min(distance_covered, total_distance)
        t = distance_covered / total_distance

        # Calculate the current position on the Bezier curve
        return self._quadratic_bezier(t)

    def _quadratic_bezier(self, t: float) -> tuple[Point2D, float]:
        """
        Calculate the position on a quadratic Bezier curve at time t.

        :param t: Parameter ranging from 0 to 1, where 0 is the start and 1 is the end of the curve.
        :return: (x, y) coordinates on the Bezier curve at time t.
        """
        if t < 0 or t > 1:
            raise ValueError("t must be between 0 and 1")

        x = (
            (1 - t) ** 2 * self.start.x
            + 2 * (1 - t) * t * self.control_point.x
            + t**2 * self.end.x
        )
        y = (
            (1 - t) ** 2 * self.start.y
            + 2 * (1 - t) * t * self.control_point.y
            + t**2 * self.end.y
        )

        # Derivative of the quadratic Bezier curve
        dx = 2 * (1 - t) * (self.control_point.x - self.start.x) + 2 * t * (
            self.end.x - self.control_point.x
        )
        dy = 2 * (1 - t) * (self.control_point.y - self.start.y) + 2 * t * (
            self.end.y - self.control_point.y
        )

        # Calculate the angle (in radians)
        angle = math.atan2(dy, dx)
        return (Point2D(x, y), angle)
