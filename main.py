from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from spatial import operation, schemas
from spatial.database import engine, SessionLocal, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/features/", response_model=schemas.Feature)
def create_feature(feature: schemas.FeatureCreate, db: Session = Depends(get_db)):
    return operation.create_feature(db, feature)

@app.get("/features/", response_model=list[schemas.Feature])
def read_features(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return operation.get_all_features(db, skip=skip, limit=limit)

@app.get("/features/{feature_id}", response_model=schemas.Feature)
def read_feature(feature_id: int, db: Session = Depends(get_db)):
    db_feature = operation.get_feature(db, feature_id)
    if db_feature is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return db_feature

@app.put("/features/{feature_id}", response_model=schemas.Feature)
def update_feature(feature_id: int, feature: schemas.FeatureUpdate, db: Session = Depends(get_db)):
    updated = operation.update_feature(db, feature_id, feature)
    if updated is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return updated

@app.delete("/features/{feature_id}", response_model=schemas.Feature)
def delete_feature(feature_id: int, db: Session = Depends(get_db)):
    deleted = operation.delete_feature(db, feature_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Feature not found")
    return deleted
