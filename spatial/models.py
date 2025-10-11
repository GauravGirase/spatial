from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Features(Base):
    __tablename__ = "Feature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    feature_type: Mapped[str] = mapped_column(String(50))
    geo_location: Mapped[dict] = mapped_column(JSON)  # Store GeoJSON as dict