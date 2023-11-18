from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Index
from sqlalchemy.ext.declarative import declarative_base

OrmBase = declarative_base()


class FlyingObjectOrm(OrmBase):
    __tablename__ = "flying_objects"

    object_id = Column(String(32), primary_key=True)
    simulation_id = Column(Integer, ForeignKey("simulations.id"))
    payload = Column(String(200), nullable=False)  # 100 bytes in hex, encoded
    created_time = Column(DateTime, nullable=False)
    speed = Column(Float, nullable=False)

    # Additional static properties if any


class FlyingObjectStateOrm(OrmBase):
    __tablename__ = "flying_object_states"

    id = Column(Integer, primary_key=True, autoincrement=True)
    object_id = Column(String(32), ForeignKey("flying_objects.object_id"))
    simulation_id = Column(Integer, ForeignKey("simulations.id"))
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    angle = Column(Float, nullable=True)
    state_time = Column(DateTime, nullable=False)
    expire_time = Column(Float, nullable=False)
    sector = Column(String(1), nullable=False)


class SimulationOrm(OrmBase):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_start = Column(DateTime, nullable=False)
    simulation_end = Column(DateTime, nullable=True)
    last_update = Column(DateTime, nullable=False)
    completion = Column(Float, nullable=False)


Index(
    "idx_flying_object_states_on_object_id_and_time",
    FlyingObjectStateOrm.simulation_id,
    FlyingObjectStateOrm.object_id,
    FlyingObjectStateOrm.state_time,
)
Index(
    "idx_flying_object_states_on_sector_and_time",
    FlyingObjectStateOrm.simulation_id,
    FlyingObjectStateOrm.sector,
    FlyingObjectStateOrm.state_time,
)
