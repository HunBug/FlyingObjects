from abc import ABC, abstractmethod
from datetime import datetime

from .flying_object import FlyingObject


class DataWriterBase(ABC):
    @abstractmethod
    def write_object(self, object: FlyingObject):
        raise NotImplementedError()

    @abstractmethod
    def write_object_state(
        self, object: FlyingObject, current_time: datetime, sector: str
    ):
        raise NotImplementedError()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def log_simulation_start(self, start_time: datetime):
        pass

    @abstractmethod
    def log_simulation_end(self, end_time: datetime):
        pass

    @abstractmethod
    def log_simulation_progress(self, progress: float):
        pass
