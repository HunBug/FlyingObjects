from datetime import datetime, timedelta
from random import choice, randint, uniform
import string
from .point_2d import Point2D
from .world import World
from .flying_object import FlyingObject
from .sector import Sector
import logging

class Generator:
    def __init__(self, start_time: datetime,
                 simulation_duration: timedelta = timedelta(hours=10),
                 simulation_resolution: timedelta = timedelta(milliseconds=150),
                 num_objects=500):
        self.world = self._initialize_world()
        self.simulation_duration = simulation_duration
        self.num_objects = num_objects
        self.start_time = start_time
        self.simulation_resolution = simulation_resolution


    def _initialize_world(self) -> World:
        # Initialize the world with the specified size and number of sectors
        # Km to m conversion
        world_site = Sector(Sector.Boundary(0, True),
                            Sector.Boundary(1000 * 1000, True),
                            Sector.Boundary(0, True),
                            Sector.Boundary(1000 * 1000, True)
                            )
        # todo add sectors
        return World(world_site, None)


    def _create_object(self, creation_time: datetime) -> FlyingObject:
        # Create a single object with random properties
        object_id = self._generate_object_id()
        initial_pos = self._generate_initial_position()
        speed = self._generate_speed()
        payload = self._generate_payload()

        obj = FlyingObject(object_id, initial_pos, speed, creation_time, payload)
        return obj
    

    def run_simulation(self):
        object_creation_times: list[datetime] = self._generate_object_creation_times(
            self.start_time, self.simulation_duration, self.num_objects
        )
        # Run the simulation for the specified duration
        current_time = self.start_time
        while current_time < self.start_time + self.simulation_duration:
            # Check if there are any objects to create
            while (len(object_creation_times) > 0 and
                    object_creation_times[-1] <= current_time):
                # Create a new object and add it to the world
                obj = self._create_object(current_time)
                destination = self._generate_initial_position() # todo add destination generation
                way_point = self._generate_initial_position() # todo add way_point generation
                obj.set_path(destination=destination, way_point=way_point)
                self.world.add_object(obj)
                object_creation_times.pop()

            # Update the world and remove expired objects
            self.world.update(current_time)

            self._debug_log(current_time)

            # Sleep until the next simulation step
            current_time += self.simulation_resolution

    def _debug_log(self, current_time: datetime):
        # logging.debug(f"Current time: {current_time}")
        # logging.debug(f"Number of objects: {len(self.world.objects)}")
        if len(self.world.objects) > 0:
            first_object = list(self.world.objects.values())[0]
            logging.debug(f"Current time: {current_time} -> {first_object.arrive_time - current_time} {first_object.position.x}")

    def _generate_object_creation_times(self, start_time: datetime,
                                        simulation_duration: timedelta,
                                        num_objects: int) -> list[datetime]:
        """
        Generate random creation times for objects within the simulation timeframe.

        :param start_time: The start time of the simulation (datetime object).
        :param simulation_duration: Duration of the simulation in seconds.
        :param num_objects: The number of objects to generate times for.
        :return: A list of datetime objects representing creation times for each object.
        """
        delta_times: list[int] = []
        simulation_miliseconds = simulation_duration.total_seconds() * 1000

        for _ in range(num_objects):
            random_miliseconds = randint(0, simulation_miliseconds)
            delta_times.append(random_miliseconds)

        delta_times = sorted(delta_times, reverse=True)

        creation_times = [
            start_time + timedelta(milliseconds=creation_time)
              for creation_time in delta_times]

        return creation_times

    def _generate_object_id(self, length: int = 32) -> str:
        """
        Generate a random object ID.

        :return: A random object ID.
        """
        # A string matching the regular expression [0-9a-z]{32}
        characters = string.ascii_lowercase + string.digits
        return ''.join(choice(characters) for _ in range(length))
    
    def _generate_initial_position(self) -> Point2D:
        """
        Generate a random initial position for an object.

        :return: A random initial position.
        """
        # A random position within the world
        x = uniform(self.world.world_size.x_lower.boundary, self.world.world_size.x_upper.boundary)
        y = uniform(self.world.world_size.y_lower.boundary, self.world.world_size.y_upper.boundary)
        return Point2D(x, y)
    
    def _generate_speed(self, min: float = 10, max: float = 80) -> float:
        # he objects speed is immutable and between 10 to 80 m/s
        return uniform(min, max)
    
    def _generate_payload(self, length: int = 200) -> str:
        """
        Generate a random payload for an object.

        :return: A random payload.
        """
        # A random hexadecimal data with the size of 100 bytes -> 200 hexadecimal characters
        characters = string.hexdigits
        return ''.join(choice(characters) for _ in range(length))