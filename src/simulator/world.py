import logging
from datetime import datetime
from typing import Dict, List, Optional

from .data_writer import DataWriterBase
from .flying_object import FlyingObject
from .sector import Sector


class World:
    """
    The World class represents the simulation environment.
    It manages and updates the state of all simulation objects within it.
    """

    def __init__(
        self,
        world_size: Sector,
        sectors: Optional[List[Sector]],
        data_writer: DataWriterBase = None,
    ) -> None:
        """
        Initializes the World with a specific size and number of sectors.

        :param size: The size of the world (e.g., in square units).
        :param sectors: The number of sectors the world is divided into.
        """
        self.world_size = world_size
        self.sectors = sectors
        self.objects: Dict[int, FlyingObject] = {}
        self.data_writer = data_writer

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
        if self.data_writer is not None:
            self.data_writer.write_object(obj)
        logging.info(f"Added object with ID {obj.object_id} to the world")

    def _remove_object(self, obj_id: int) -> None:
        """
        Removes a simulation object from the world.

        :param obj_id: The ID of the object to remove.
        """
        self.objects.pop(obj_id, None)
        logging.info(f"Removed object with ID {obj_id} from the world")

    def update(self, current_time: datetime) -> None:
        """
        Updates the state of the world and all objects within it.
        """
        for obj in list(self.objects.values()):
            obj.update(current_time)
            if obj.is_expired:
                self._remove_object(obj.object_id)
            if not self._is_valid_position(obj):
                self._remove_object(obj.object_id)
        if self.data_writer is not None:
            for obj in self.objects.values():
                self.data_writer.write_object_state(
                    obj, current_time, self._get_sector(obj)
                )

    def _is_valid_position(self, obj: FlyingObject) -> bool:
        """
        Validates the position of an object within the world.

        :param obj: The object whose position is to be validated.
        """
        # check if the object is within the world
        return self.world_size.contains(obj.position)

    def _get_sector(self, obj: FlyingObject) -> str:
        """
        Determines the sector that an object is in.

        :param obj: The object whose sector is to be determined.
        """
        sector_name: str = None
        for sector in self.sectors:
            if sector.contains(obj.position):
                if sector_name is not None:
                    raise ValueError(
                        f"Object with ID {obj.object_id} is in multiple sectors"
                    )
                sector_name = sector.name
        if sector_name is None:
            raise ValueError(f"Object with ID {obj.object_id} is not in any sector")
        return sector_name
