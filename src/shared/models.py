from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, Interval, Column, String, Float, DateTime

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