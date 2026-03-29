from ..db import crud, database
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

def generate_usage_report(db: Session, workstation_id: int = None, days: int = 7):
    start_date = datetime.utcnow() - timedelta(days=days)
    logs = crud.get_logs(db, workstation_id)
    # Filter by date
    recent_logs = [log for log in logs if log.timestamp >= start_date]
    report = {
        "workstation_id": workstation_id,
        "period": f"{days} days",
        "total_actions": len(recent_logs),
        "actions": [log.action for log in recent_logs]
    }
    return report

def generate_resource_report(db: Session):
    # Placeholder: in real, collect from monitor data, but since not stored, placeholder
    return {"cpu_avg": 50, "ram_avg": 60}
