# Quick Reference Guide - Classroom Manager

## 🚀 Starting the Application

### Terminal 1: Start the Server
```bash
cd /Volumes/ADATA/PROGRAMMING/class-assistant-project/lab_manager
source .venv/bin/activate
python -m uvicorn server.api:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Start the Agent
```bash
cd /Volumes/ADATA/PROGRAMMING/class-assistant-project/lab_manager
source .venv/bin/activate
python -m agent.main
```

### Terminal 3: Run Tests
```bash
cd /Volumes/ADATA/PROGRAMMING/class-assistant-project/lab_manager
source .venv/bin/activate
python test_api.py
```

---

## 📡 Essential API Endpoints

### Register a Workstation
```bash
curl -X POST "http://localhost:8000/workstations/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "PC1",
    "ip_address": "192.168.1.10",
    "status": "online"
  }'
```

### Get All Workstations
```bash
curl -X GET "http://localhost:8000/workstations/"
```

### Lock All Screens
```bash
for ip in 192.168.1.10 192.168.1.11 192.168.1.12; do
  curl -X POST "http://localhost:8000/command/$ip" \
    -H "Content-Type: application/json" \
    -d '{"command": "lock_screen"}'
done
```

### Get System Monitoring Data
```bash
curl -X GET "http://localhost:8001/monitor" \
  -H "Authorization: Bearer secret_token"
```

### Shutdown a PC
```bash
curl -X POST "http://localhost:8000/command/192.168.1.10" \
  -H "Content-Type: application/json" \
  -d '{"command": "shutdown"}'
```

### Create a Profile
```bash
curl -X POST "http://localhost:8000/profiles/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "lesson",
    "description": "Disable distractions during lesson",
    "settings": {
      "disable_animations": true,
      "block_sites": ["facebook.com", "youtube.com"]
    }
  }'
```

### Apply Profile to Workstations
```bash
curl -X POST "http://localhost:8000/apply_profile?profile_name=lesson" \
  -H "Content-Type: application/json" \
  -d '["192.168.1.10", "192.168.1.11"]'
```

### Generate Report
```bash
curl -X GET "http://localhost:8000/report?workstation_id=1" \
  -H "Content-Type: application/json"
```

### Export Report to PDF
```bash
curl -X POST "http://localhost:8000/export_report?workstation_id=1"
```

---

## 📁 Key Files Location

| File | Location | Purpose |
|------|----------|---------|
| Server API | `server/api.py` | Main FastAPI server |
| Agent API | `agent/main.py` | Student PC agent |
| Database Models | `server/db/models.py` | SQLAlchemy ORM models |
| Schemas | `shared/schemas.py` | Pydantic validation models |
| Constants | `shared/constants.py` | Configuration & constants |
| Documentation | `README.md` | Complete documentation |
| Test Suite | `test_api.py` | Comprehensive tests |
| Test Report | `TEST_REPORT.md` | Detailed test results |

---

## 🔧 Common Operations

### Kill a Process on Student PC
```bash
curl -X POST "http://localhost:8000/command/192.168.1.10" \
  -H "Content-Type: application/json" \
  -d '{
    "command": "kill_process",
    "params": {"pid": 1234}
  }'
```

### Block Internet on Student PC
```bash
curl -X POST "http://localhost:8000/command/192.168.1.10" \
  -H "Content-Type: application/json" \
  -d '{"command": "block_internet"}'
```

### Unblock Internet
```bash
curl -X POST "http://localhost:8000/command/192.168.1.10" \
  -H "Content-Type: application/json" \
  -d '{"command": "unblock_internet"}'
```

### Create Log Entry
```bash
curl -X POST "http://localhost:8000/logs/" \
  -H "Content-Type: application/json" \
  -d '{
    "workstation_id": 1,
    "action": "lock_screen",
    "details": "Locked for explanation",
    "timestamp": "2026-03-29T10:10:00"
  }'
```

### Get Logs for a Workstation
```bash
curl -X GET "http://localhost:8000/logs/?workstation_id=1"
```

---

## 🐛 Troubleshooting

### Server Won't Start
**Error**: `Address already in use`
```bash
# Kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Agent Won't Start
**Error**: `Connection refused on 8001`
```bash
# Kill process using port 8001
lsof -i :8001
kill -9 <PID>
```

### Database Locked
**Error**: `database is locked`
```bash
# Delete and recreate database
rm lab_manager/classroom.db
python -m uvicorn server.api:app --port 8000
```

### Import Errors
**Error**: `ModuleNotFoundError`
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📊 Database Reset

To reset everything and start fresh:
```bash
# Stop all services
pkill -f uvicorn
pkill -f "agent.main"

# Remove database
rm lab_manager/classroom.db

# Clear caches
find lab_manager -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Restart services
python -m uvicorn server.api:app --port 8000
```

---

## 🔑 Default Credentials

| Item | Value |
|------|-------|
| Server Port | 8000 |
| Agent Port | 8001 |
| Auth Token | `secret_token` |
| Database | `classroom.db` |
| DB Type | SQLite |

---

## 📝 Project Structure Summary

```
lab_manager/
├── agent/               # Student PC agent
├── server/              # Teacher control server
├── shared/              # Shared utilities
├── test_api.py          # Test suite
├── requirements.txt     # Dependencies
├── README.md            # Full documentation
├── TEST_REPORT.md       # Test results
├── PROJECT_STATUS.txt   # Project status
└── classroom.db         # SQLite database (auto-created)
```

---

## ✨ Features Checklist

- [x] Workstation Management
- [x] Command Execution
- [x] System Monitoring
- [x] Profile Management
- [x] Event Logging
- [x] Report Generation
- [x] Authentication
- [x] Database Operations
- [ ] PyQt6 GUI (basic framework in place)
- [ ] WebSocket Real-time Updates
- [ ] Advanced Scheduling

---

## 📚 More Information

For complete documentation, see:
- **README.md** - Full feature documentation
- **TEST_REPORT.md** - Test results and performance
- **PROJECT_STATUS.txt** - Project status overview

---

**Last Updated**: March 29, 2026
**Version**: 1.0.0 (Beta)
