from datetime import datetime
from typing import Dict, List, Optional
from flying_object import FlyingObject
from sector import Sector

class World:
    """
    The World class represents the simulation environment.
    It manages and updates the state of all simulation objects within it.
    """

    def __init__(self, world_size: Sector, sectors: Optional[List[Sector]]) -> None:
        """
        Initializes the World with a specific size and number of sectors.

        :param size: The size of the world (e.g., in square units).
        :param sectors: The number of sectors the world is divided into.
        """
        self.world_size = world_size
        self.sectors = sectors
        self.objects: Dict[int, FlyingObject] = {}

    def add_object(self, obj: FlyingObject) -> None:
        """
        Adds a simulation object to the world.

        :param obj: The SimulationObject to add to the world.
        """

        if obj.object_id in self.objects:
            raise ValueError(f"Object with ID {obj.id} already exists in the world")
        if not self._is_valid_position(obj):
            raise ValueError(f"Object with ID {obj.id} is not within the world")
        self.objects[obj.object_id] = obj

    def _remove_object(self, obj_id: int) -> None:
        """
        Removes a simulation object from the world.

        :param obj_id: The ID of the object to remove.
        """
        self.objects.pop(obj_id, None)

    def update(self, current_time: datetime) -> None:
        """
        Updates the state of the world and all objects within it.
        """
        for obj in list(self.objects.values()):
            obj.update(current_time)
            if obj.is_expired:
                self._remove_object(obj.id)
            if not self._is_valid_position(obj):
                self._remove_object(obj.id)

    def _is_valid_position(self, obj: FlyingObject) -> bool:
        """
        Validates the position of an object within the world.

        :param obj: The object whose position is to be validated.
        """
        # check if the object is within the world
        return self.world_size.contains(obj.position)
        

    def find_objects_in_sector(self, sector_number: int) -> List[FlyingObject]:
        """
        Finds and returns all objects in a specified sector.

        :param sector_number: The sector number to search within.
        :return: A list of SimulationObjects in the specified sector.
        """
        return [obj for obj in self.objects.values() if obj.is_in_sector(sector_number)]
