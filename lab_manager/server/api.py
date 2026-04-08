from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db import database, crud
from .api_client import APIClient
from .profiles.profile_engine import ProfileEngine
from .reports.report_generator import generate_usage_report
from .reports.pdf_exporter import export_report_to_pdf
from shared import schemas, constants
import uvicorn

app = FastAPI(title="Classroom Manager Server")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

api_client = APIClient(f"http://{constants.SERVER_IP}:{constants.DEFAULT_PORT}")
profile_engine = ProfileEngine(api_client)

@app.get("/workstations/", response_model=list[schemas.Workstation])
def read_workstations(db: Session = Depends(get_db)):
    workstations = crud.get_workstations(db)
    return workstations

@app.post("/workstations/", response_model=schemas.Workstation)
def create_workstation(workstation: schemas.WorkstationCreate, db: Session = Depends(get_db)):
    return crud.create_workstation(db, workstation)

@app.put("/workstations/{workstation_id}/status")
def update_status(workstation_id: int, status: str, db: Session = Depends(get_db)):
    return crud.update_workstation_status(db, workstation_id, status)

@app.get("/profiles/", response_model=list[schemas.Profile])
def read_profiles(db: Session = Depends(get_db)):
    return crud.get_profiles(db)

@app.post("/profiles/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db, profile)

@app.get("/logs/", response_model=list[schemas.LogEntry])
def read_logs(workstation_id: int = None, db: Session = Depends(get_db)):
    return crud.get_logs(db, workstation_id)

@app.post("/logs/", response_model=schemas.LogEntry)
def create_log(log_entry: schemas.LogEntryCreate, db: Session = Depends(get_db)):
    return crud.create_log_entry(db, log_entry)

@app.post("/command/{ip}")
async def send_command(ip: str, command: schemas.CommandRequest):
    response = await api_client.send_command(ip, command)
    return response

@app.post("/apply_profile")
async def apply_profile_to_all(profile_name: str, workstations: list[str]):
    await profile_engine.apply_profile_to_all(workstations, profile_name)
    return {"status": "profile applied"}

@app.get("/report")
def get_report(workstation_id: int = None, db: Session = Depends(get_db)):
    return generate_usage_report(db, workstation_id)

@app.post("/export_report")
def export_report(workstation_id: int = None, db: Session = Depends(get_db)):
    report = generate_usage_report(db, workstation_id)
    export_report_to_pdf(report, "report.pdf")
    return {"status": "exported"}

if __name__ == "__main__":
    uvicorn.run(app, host=constants.SERVER_HOST, port=constants.DEFAULT_PORT)
