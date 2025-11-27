from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app.api.auth import get_current_user
import uuid

router = APIRouter()

# Family CRUD
@router.post("/families", response_model=schemas.FamilyResponse)
def create_family(family: schemas.FamilyCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_family = models.Family(**family.dict(), owner_id=current_user.id)
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family

@router.get("/families", response_model=List[schemas.FamilyResponse])
def get_families(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Family).filter(models.Family.owner_id == current_user.id).all()

# Blocklist
@router.post("/families/{family_id}/blocklist", response_model=schemas.BlocklistEntryResponse)
def add_blocklist_entry(family_id: int, entry: schemas.BlocklistEntryCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    family = db.query(models.Family).filter(models.Family.id == family_id, models.Family.owner_id == current_user.id).first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    
    db_entry = models.BlocklistEntry(**entry.dict(), family_id=family_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.delete("/families/{family_id}/blocklist/{entry_id}")
def remove_blocklist_entry(family_id: int, entry_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    family = db.query(models.Family).filter(models.Family.id == family_id, models.Family.owner_id == current_user.id).first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    
    db.query(models.BlocklistEntry).filter(models.BlocklistEntry.id == entry_id, models.BlocklistEntry.family_id == family_id).delete()
    db.commit()
    return {"ok": True}

# Public Policy Endpoint for Resolver/Extension
@router.get("/{family_id}", response_model=schemas.PolicyResponse)
def get_policy(family_id: int, db: Session = Depends(database.get_db)):
    family = db.query(models.Family).filter(models.Family.id == family_id).first()
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    
    blocklist = [e.domain for e in family.blocklist if e.entry_type == models.BlocklistType.BLOCK]
    whitelist = [e.domain for e in family.blocklist if e.entry_type == models.BlocklistType.ALLOW]
    
    return schemas.PolicyResponse(
        family_id=family.id,
        block_adult=family.block_adult,
        block_phishing=family.block_phishing,
        block_scam=family.block_scam,
        blocklist=blocklist,
        whitelist=whitelist
    )

# Override Request
@router.post("/override/request", response_model=schemas.OverrideRequestResponse)
def request_override(request: schemas.OverrideRequestCreate, db: Session = Depends(database.get_db)):
    token = str(uuid.uuid4())
    db_request = models.OverrideRequest(**request.dict(), token=token)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request
