from sqlalchemy.orm import Session
from shared import schemas
from . import models

def get_workstations(db: Session):
    return db.query(models.Workstation).all()

def get_workstation(db: Session, workstation_id: int):
    return db.query(models.Workstation).filter(models.Workstation.id == workstation_id).first()

def create_workstation(db: Session, workstation: schemas.WorkstationCreate):
    db_workstation = models.Workstation(name=workstation.name, ip_address=workstation.ip_address, status=workstation.status)
    db.add(db_workstation)
    db.commit()
    db.refresh(db_workstation)
    return db_workstation

def update_workstation_status(db: Session, workstation_id: int, status: str):
    db_workstation = get_workstation(db, workstation_id)
    if db_workstation:
        db_workstation.status = status
        db.commit()
        db.refresh(db_workstation)
    return db_workstation

def get_profiles(db: Session):
    return db.query(models.Profile).all()

def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(name=profile.name, description=profile.description, settings=profile.settings)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def create_log_entry(db: Session, log_entry: schemas.LogEntryCreate):
    db_log = models.LogEntry(workstation_id=log_entry.workstation_id, action=log_entry.action, details=log_entry.details, timestamp=log_entry.timestamp)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs(db: Session, workstation_id: int = None):
    query = db.query(models.LogEntry)
    if workstation_id:
        query = query.filter(models.LogEntry.workstation_id == workstation_id)
    return query.all()
