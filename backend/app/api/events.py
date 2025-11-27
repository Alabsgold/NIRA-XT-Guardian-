from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db)):
    # This endpoint is called by the resolver/extension, so no auth for now (or use API key in future)
    db_event = models.EventLog(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/families/{family_id}", response_model=List[schemas.EventResponse])
def get_events(family_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    family = db.query(models.Family).filter(models.Family.id == family_id, models.Family.owner_id == current_user.id).first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    
    return db.query(models.EventLog).filter(models.EventLog.family_id == family_id).order_by(models.EventLog.timestamp.desc()).limit(100).all()
