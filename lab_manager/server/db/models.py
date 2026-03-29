from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Workstation(Base):
    __tablename__ = "workstations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String, unique=True, index=True)
    status = Column(String, default="offline")  # online, offline

    logs = relationship("LogEntry", back_populates="workstation")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    settings = Column(JSON)  # Store settings as JSON

class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, index=True)
    workstation_id = Column(Integer, ForeignKey("workstations.id"))
    action = Column(String)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    workstation = relationship("Workstation", back_populates="logs")
