from typing import Optional
from datetime import datetime
import re
import math
from point_2d import Point2D
from bezier_path import BezierPath

class FlyingObject:
    def __init__(self, object_id: str, initial_pos: Point2D, speed: float, creation_time: datetime,
                 payload: str):
        self.object_id = object_id # TODO add immutable property
        self.speed = speed # TODO add immutable property
        self.creation_time = creation_time # TODO add immutable property
        self.payload = payload # TODO add immutable property
        self.initial_pos = initial_pos # TODO add immutable property
        self._validate_initial_data()

        self.path: Optional[BezierPath] = None
        self.arrive_time: Optional[datetime] = None

        self.position: Optional[Point2D] = initial_pos
        self.angle: Optional[float] = None
        self.is_expired: Optional[bool] = None

    def _validate_initial_data(self):
        # object_id: A string matching the regular expression /[0-9a-z]{32}/gmU
        # gmU flags are "default" in Python
        pattern = r"[0-9a-z]{32}"
        if not re.fullmatch(pattern, self.object_id):
            raise ValueError(f"Invalid object_id {self.object_id}. It should match the pattern {pattern}")
        
        # payload: random hexadecimal data with the size of 100 bytes
        # hexadecimal character represents 4 bits, 100 bytes would be represented by 200 hexadecimal characters
        pattern = r"^[0-9a-fA-F]{200}$"
        if not re.fullmatch(pattern, self.payload):
            raise ValueError(f"Invalid payload {self.payload}. It should match the pattern {pattern}")

    # TODO static method
    def _normalize_angle(angle_rad: float) -> float:
        """
        Normalize an angle in radians to be between 0 and 2π.
        It converts negative angles to their positive counterparts.

        :param angle_rad: The angle in radians.
        :return: Normalized angle between 0 and 2π.
        """
        # Ensure the angle is positive and within the range 0 to 2π
        normalized_angle = angle_rad % (2 * math.pi)

        return normalized_angle
    
    def set_path(self, destination: Point2D, way_point: Point2D):
        """
        Set the path for the object to follow.

        :param destination: The destination (x, y) of the object.
        :param way_point: The waypoint (x, y) for the Bezier curve.
        """
        if self.path is not None:
            raise ValueError("The path has already been set")
        self.path = BezierPath(self.initial_pos, destination, way_point)

    def update(self, current_time: datetime) -> tuple[Point2D, float, bool]:
        # TODO should be the results stored in the object?
        if self.path is None:
            raise ValueError("The path has not been set")
        position, angle = self.path.calculate_position_and_angle(self.creation_time, current_time, self.speed)
        angle = FlyingObject._normalize_angle(angle)
        # Determine if the object has expired
        if self.arrive_time is None:
            self.arrive_time = self.path.calculate_arrive_time(self.creation_time, self.speed)
        is_expired = current_time >= self.arrive_time
        
        self.position = position
        self.angle = angle
        self.is_expired = is_expired
        return position, angle, is_expired
        
