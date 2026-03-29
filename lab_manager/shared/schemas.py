from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schemas for API communication

class WorkstationBase(BaseModel):
    name: str
    ip_address: str
    status: str  # online, offline

class WorkstationCreate(WorkstationBase):
    pass

class Workstation(WorkstationBase):
    id: int

    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    name: str
    description: Optional[str] = None
    settings: dict  # JSON-like settings

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True

class LogEntryBase(BaseModel):
    workstation_id: int
    action: str
    details: Optional[str] = None
    timestamp: datetime

class LogEntryCreate(LogEntryBase):
    pass

class LogEntry(LogEntryBase):
    id: int

    class Config:
        from_attributes = True

class CommandRequest(BaseModel):
    command: str  # e.g., lock_screen, shutdown
    params: Optional[dict] = None

class MonitorData(BaseModel):
    cpu_usage: float
    ram_usage: float
    disk_usage: float
    processes: List[dict]  # list of process info
