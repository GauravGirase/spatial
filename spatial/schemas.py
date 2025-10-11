from pydantic import BaseModel
from typing import Any, Dict

class FeatureBase(BaseModel):
    name: str
    feature_type: str
    geo_location: Dict[str, Any]  # GeoJSON-like dict

class FeatureCreate(FeatureBase):
    pass

class FeatureUpdate(FeatureBase):
    pass

class Feature(FeatureBase):
    id: int

    class Config:
        orm_mode = True
