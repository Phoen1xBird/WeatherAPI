from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func

from database.orm._base_class import Base
from database.orm._annotations import (
    IntegerPrimaryKey,
    IntegerColumn,
    TextColumn,
    TimestampWTColumn,
    DoubleColumn
)

class WeatherRequests(Base):
    __tablename__ = "weather_requests"
    
    id: Mapped[IntegerPrimaryKey] = mapped_column()
    created_at: Mapped[TimestampWTColumn] = mapped_column(nullable=False, default=func.now())
    lat: Mapped[DoubleColumn] = mapped_column(nullable=False)
    lon: Mapped[DoubleColumn] = mapped_column(nullable=False)
    weather_main: Mapped[TextColumn] = mapped_column(nullable=False)
    temp: Mapped[DoubleColumn] = mapped_column(nullable=False)
    wind_speed: Mapped[DoubleColumn] = mapped_column(nullable=False)
