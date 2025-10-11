from sqlalchemy.orm import Session
from .models import Features
from .schemas import FeatureCreate, FeatureUpdate

def get_feature(db: Session, feature_id: int):
    return db.query(Features).filter(Features.id == feature_id).first()

def get_all_features(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Features).offset(skip).limit(limit).all()

def create_feature(db: Session, feature: FeatureCreate):
    db_feature = Features(**feature.dict())
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature

def update_feature(db: Session, feature_id: int, feature: FeatureUpdate):
    db_feature = get_feature(db, feature_id)
    if not db_feature:
        return None
    for key, value in feature.dict().items():
        setattr(db_feature, key, value)
    db.commit()
    db.refresh(db_feature)
    return db_feature

def delete_feature(db: Session, feature_id: int):
    db_feature = get_feature(db, feature_id)
    if not db_feature:
        return None
    db.delete(db_feature)
    db.commit()
    return db_feature
