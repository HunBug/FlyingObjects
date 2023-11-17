from datetime import datetime
from sqlalchemy import ForeignKey, Integer, Interval, create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from .flying_object import FlyingObject
from .data_writer import DataWriterBase
import logging

OrmBase = declarative_base()

class FlyingObjectOrm(OrmBase):
    __tablename__ = 'flying_objects'

    object_id = Column(String(32), primary_key=True)
    payload = Column(String(200), nullable=False)  # 100 bytes in hex, encoded
    created_time = Column(DateTime, nullable=False)
    speed = Column(Float, nullable=False)

    # Additional static properties if any

class FlyingObjectStateOrm(OrmBase):
    __tablename__ = 'flying_object_states'

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_id = Column(String(32), ForeignKey('flying_objects.object_id'))
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    angle = Column(Float, nullable=True)
    state_time = Column(DateTime, nullable=False)
    expire_time = Column(Float, nullable=False)
    sector = Column(String(1), nullable=False)


class SqlDataWriter(DataWriterBase):

    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri)
        OrmBase.metadata.create_all(self.engine)
        self.commit_interval = 10000
        self.session = None

    def connect(self):
        self.session = Session(self.engine)

    def close(self):
        if self.session is not None:
            self.session.commit()

    def write_object(self, object: FlyingObject):
        new_object = FlyingObjectOrm(
            object_id=object.object_id,
            payload=object.payload,
            speed=object.speed,
            created_time=object.creation_time,
        )
        self.session.add(new_object)
        self._batch_commit()

    def write_object_state(self, object: FlyingObject, current_time: datetime, sector: str):
        new_state = FlyingObjectStateOrm(
            object_id=object.object_id,
            x=object.position.x,
            y=object.position.y,
            angle=object.angle,
            state_time=current_time,
            expire_time=(object.arrive_time - current_time).total_seconds(),
            sector=sector
        )
        self.session.add(new_state)
        self._batch_commit()

    def _batch_commit(self):
        if len(self.session.new) % self.commit_interval == 0:
            self.session.commit()
            self.session.expunge_all()
            logging.info(f"Committed {self.commit_interval} objects to the database")