import logging
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from shared.models import FlyingObjectOrm, FlyingObjectStateOrm, OrmBase, SimulationOrm

from .data_writer import DataWriterBase
from .flying_object import FlyingObject


class SqlDataWriter(DataWriterBase):
    def __init__(self, db_uri: str, simulation_id: int = None):
        self._engine = create_engine(db_uri)
        OrmBase.metadata.create_all(self._engine)
        self.commit_interval = 10000
        self._session = None
        self._object_cache = []
        self._simulation_id: int = simulation_id
        self.last_log_time = datetime.now()
        self.log_frequency = timedelta(seconds=10)

    def connect(self):
        self._session = Session(self._engine)

    def close(self):
        self._batch_commit(force=True)
        if self._session is not None:
            self._session.commit()

    def write_object(self, object: FlyingObject):
        simulation_id = self._get_simulation()
        new_object = FlyingObjectOrm(
            object_id=object.object_id,
            simulation_id=simulation_id,
            payload=object.payload,
            speed=object.speed,
            created_time=object.creation_time,
        )
        # self.session.add(new_object)
        self._object_cache.append(new_object)
        self._batch_commit()

    def write_object_state(
        self, object: FlyingObject, current_time: datetime, sector: str
    ):
        simulation_id = self._get_simulation()
        new_state = FlyingObjectStateOrm(
            object_id=object.object_id,
            simulation_id=simulation_id,
            x=object.position.x,
            y=object.position.y,
            angle=object.angle,
            state_time=current_time,
            expire_time=(object.arrive_time - current_time).total_seconds(),
            sector=sector,
        )
        # self.session.add(new_state)
        self._object_cache.append(new_state)
        self._batch_commit()

    def _batch_commit(self, force=False):
        # if len(self.session.new) % self.commit_interval == 0:  # Too slow according to profiler
        if (len(self._object_cache) > self.commit_interval) or force:
            # self.session.add_all(self.object_cache)
            self._session.bulk_save_objects(self._object_cache)
            self._session.commit()
            self._session.expunge_all()
            logging.info(f"Committed {self.commit_interval} objects to the database")
            self._object_cache = []

    def log_simulation_start(self, start_time: datetime) -> int:
        if self._simulation_id is not None:
            raise ValueError("Simulation ID is already set")
        new_simulation = SimulationOrm(
            simulation_start=start_time, last_update=start_time, completion=0.0
        )
        self._session.add(new_simulation)
        self._session.commit()
        self._simulation_id = new_simulation.id
        return self._simulation_id

    def log_simulation_end(self, end_time: datetime):
        simulation_id = self._get_simulation()
        simulation = self._session.query(SimulationOrm).get(simulation_id)
        simulation.simulation_end = end_time
        simulation.last_update = end_time
        simulation.completion = 1.0
        self._session.commit()

    def log_simulation_progress(self, progress: float):
        current_time = datetime.now()
        if current_time - self.last_log_time < self.log_frequency:
            return
        simulation_id = self._get_simulation()
        simulation = self._session.query(SimulationOrm).get(simulation_id)
        simulation.last_update = current_time
        simulation.completion = progress
        self._session.commit()
        self.last_log_time = current_time

    def _get_simulation(self):
        if self._simulation_id is None:
            raise ValueError("Simulation ID is not set")
        return self._simulation_id
