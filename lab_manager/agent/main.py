from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .modules import system_control, process_manager, monitor, optimization, network_manager
from shared import constants, schemas

app = FastAPI(title="Classroom Agent")
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != constants.AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/command")
def execute_command(command: schemas.CommandRequest, token=Depends(verify_token)):
    if command.command == "lock_screen":
        system_control.lock_screen()
        return {"status": "locked"}
    elif command.command == "shutdown":
        system_control.shutdown()
        return {"status": "shutting down"}
    elif command.command == "restart":
        system_control.restart()
        return {"status": "restarting"}
    elif command.command == "kill_process":
        pid = command.params.get("pid")
        if pid:
            success = process_manager.kill_process(pid)
            return {"status": "killed" if success else "failed"}
    elif command.command == "apply_profile":
        profile = command.params.get("profile")
        if profile == "lesson":
            optimization.apply_lesson_profile()
            return {"status": "profile applied"}
    elif command.command == "block_internet":
        network_manager.block_internet()
        return {"status": "internet blocked"}
    elif command.command == "unblock_internet":
        network_manager.unblock_internet()
        return {"status": "internet unblocked"}
    # Add more
    return {"status": "command executed"}

@app.get("/monitor", response_model=schemas.MonitorData)
def get_monitor_data(token=Depends(verify_token)):
    stats = monitor.get_system_stats()
    processes = monitor.get_processes()
    return schemas.MonitorData(
        cpu_usage=stats["cpu_usage"],
        ram_usage=stats["ram_usage"],
        disk_usage=stats["disk_usage"],
        processes=processes
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=constants.AGENT_PORT)
