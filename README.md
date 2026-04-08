# Classroom Manager - IT Classroom Management Application

A comprehensive Python-based client-server application for managing IT classrooms. Control student PCs, monitor system resources, optimize performance, and generate detailed reports—all from a teacher's control panel.

## 🎯 Features

### 1. **Workstation Management**
- ✅ Start/Stop/Restart any PC or all at once
- ✅ Lock student screens during explanations
- ✅ Force close applications on student machines
- ✅ Real-time online/offline status tracking

### 2. **Performance Optimization**
- ✅ Disable visual effects and animations on old hardware
- ✅ Auto-kill unnecessary background processes
- ✅ Apply preset profiles ("Lesson", "Exam", "Free Work")
- ✅ Auto-reset settings after session ends

### 3. **Network Management**
- ✅ Configure proxy settings across all PCs
- ✅ Block/unblock internet access
- ✅ Block specific websites via hosts file
- ✅ Enable/disable network access with one click

### 4. **Real-Time Monitoring**
- ✅ View CPU, RAM, and disk usage per machine
- ✅ See running applications on student PCs
- ✅ Monitor online/offline agent status
- ✅ Get process-level insights

### 5. **Reporting & Logging**
- ✅ Comprehensive event journal (who did what, when)
- ✅ Resource usage reports
- ✅ PDF export functionality
- ✅ Filterable logs by workstation and timeframe

### 6. **Profile Management**
- ✅ Create custom profiles with specific settings
- ✅ Apply profiles to individual or all workstations
- ✅ Schedule automatic profile application
- ✅ Persistent profile storage in database

## 📁 Project Structure

```
lab_manager/
├── agent/                          # Student PC Agent
│   ├── main.py                    # FastAPI server (runs on port 8001)
│   ├── config.json                # Agent configuration
│   ├── modules/
│   │   ├── system_control.py      # Lock/shutdown/restart
│   │   ├── process_manager.py     # Kill processes, list apps
│   │   ├── monitor.py             # psutil - CPU/RAM/Disk
│   │   ├── optimization.py        # Disable effects, kill processes
│   │   └── network_manager.py     # Proxy, block internet, edit hosts
│   └── __init__.py
│
├── server/                         # Teacher's Control Panel
│   ├── api.py                     # FastAPI server (port 8000)
│   ├── main.py                    # PyQt6 GUI
│   ├── api_client.py              # HTTP client for agent communication
│   ├── discovery.py               # Network discovery of agents
│   ├── db/
│   │   ├── database.py            # SQLite setup
│   │   ├── models.py              # SQLAlchemy ORM models
│   │   └── crud.py                # Database operations
│   ├── profiles/
│   │   ├── profile_engine.py      # Apply profiles to workstations
│   │   └── default_profiles/
│   │       ├── lesson.json        # Disable distractions
│   │       ├── exam.json          # Strict settings
│   │       └── free.json          # Minimal restrictions
│   ├── reports/
│   │   ├── report_generator.py    # Generate reports from logs
│   │   └── pdf_exporter.py        # Export to PDF using reportlab
│   ├── gui/                       # PyQt6 interface
│   │   ├── main_window.py         # Main dashboard
│   │   ├── monitor_panel.py       # CPU/RAM monitoring view
│   │   ├── control_panel.py       # Command buttons
│   │   └── profile_manager.py     # Profile UI
│   └── __init__.py
│
├── shared/                         # Shared utilities
│   ├── schemas.py                 # Pydantic data models
│   ├── constants.py               # App constants
│   └── __init__.py
│
├── test_api.py                    # Comprehensive API test suite
├── requirements.txt               # Python dependencies
└── classroom.db                   # SQLite database (created at runtime)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Install Dependencies
```bash
cd lab_manager
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Start the Server (Teacher's PC)
```bash
cd lab_manager
python -m uvicorn server.api:app --host 0.0.0.0 --port 8000 --reload
```

The server will:
- Start FastAPI on http://localhost:8000
- Create SQLite database automatically
- Be ready to receive commands

### Step 3: Start Agents (Student PCs)
On each student computer, run:
```bash
cd lab_manager
python -m agent.main
```

The agent will:
- Start FastAPI on http://localhost:8001
- Listen for commands from the server
- Monitor system resources

## 🧪 Testing

Run the comprehensive test suite to verify all functionality:
```bash
python test_api.py
```

This will test:
- ✅ Workstation CRUD operations
- ✅ Profile management
- ✅ Logging system
- ✅ Report generation
- ✅ Agent monitoring
- ✅ Command execution

## 📡 API Endpoints

### Server API (Port 8000)

**Workstations**
- `GET /workstations/` - List all workstations
- `POST /workstations/` - Register a new workstation
- `PUT /workstations/{id}/status` - Update workstation status

**Profiles**
- `GET /profiles/` - List all profiles
- `POST /profiles/` - Create a new profile
- `POST /apply_profile` - Apply profile to workstations

**Logs & Reporting**
- `GET /logs/` - Get event logs
- `POST /logs/` - Create log entry
- `GET /report` - Generate usage report
- `POST /export_report` - Export report to PDF

**Commands**
- `POST /command/{ip}` - Send command to agent

### Agent API (Port 8001)

**Monitoring**
- `GET /monitor` - Get system metrics (CPU, RAM, disk, processes)

**Commands**
- `POST /command` - Execute command (lock_screen, shutdown, restart, kill_process, etc.)

All agent endpoints require authentication header:
```
Authorization: Bearer secret_token
```

## 💡 Usage Examples

### Example 1: Lock All Student Screens
```bash
curl -X POST "http://localhost:8000/command/192.168.1.10" \
  -H "Content-Type: application/json" \
  -d '{"command": "lock_screen"}'
```

### Example 2: Get System Monitoring Data
```bash
curl -X GET "http://localhost:8001/monitor" \
  -H "Authorization: Bearer secret_token"
```

### Example 3: Create and Apply Lesson Profile
```bash
# Create profile
curl -X POST "http://localhost:8000/profiles/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "lesson",
    "description": "Lesson configuration",
    "settings": {"disable_animations": true, "block_sites": ["youtube.com"]}
  }'

# Apply profile
curl -X POST "http://localhost:8000/apply_profile?profile_name=lesson" \
  -H "Content-Type: application/json" \
  -d '["192.168.1.10", "192.168.1.11", "192.168.1.12"]'
```

### Example 4: Generate Report
```bash
curl -X GET "http://localhost:8000/report?workstation_id=1" \
  -H "Content-Type: application/json"
```

## 🔒 Security Notes

**Current Implementation** (Development):
- Simple token-based authentication
- `AUTH_TOKEN = "secret_token"`

**Production Recommendations**:
- Implement JWT (JSON Web Tokens)
- Use HTTPS/SSL encryption
- Implement role-based access control (RBAC)
- Add rate limiting
- Validate all inputs
- Use environment variables for secrets
- Implement audit logging
- Add IP whitelisting for agents

## 🛠️ Customization

### Adding New Commands

1. Add to `shared/constants.py`:
```python
COMMANDS = {
    "my_command": "my_command",
    ...
}
```

2. Implement in `agent/modules/` (create new file or add to existing):
```python
def my_command(params):
    # Implementation
    pass
```

3. Add endpoint in `agent/main.py`:
```python
elif command.command == "my_command":
    result = system_control.my_command()
    return {"status": result}
```

### Creating Custom Profiles

Add JSON files to `server/profiles/default_profiles/`:
```json
{
  "name": "my_profile",
  "disable_animations": true,
  "kill_processes": ["app1", "app2"],
  "block_sites": ["site1.com", "site2.com"]
}
```

## 📊 Database Schema

**Workstations Table**
- `id` - Primary key
- `name` - Computer name
- `ip_address` - Network IP
- `status` - online/offline

**Profiles Table**
- `id` - Primary key
- `name` - Profile name
- `description` - Profile description
- `settings` - JSON settings

**LogEntries Table**
- `id` - Primary key
- `workstation_id` - Foreign key
- `action` - Action performed
- `details` - Additional info
- `timestamp` - When action occurred

## 🐛 Troubleshooting

**Agent not connecting:**
- Check firewall settings
- Verify agent is running: `ps aux | grep agent`
- Check port 8001 is open: `netstat -an | grep 8001`

**Server API not responding:**
- Check if uvicorn is running: `ps aux | grep uvicorn`
- Verify port 8000 is available
- Check logs for errors

**Database errors:**
- Delete `classroom.db` to reset database
- Check file permissions in project directory

**Commands not executing:**
- Verify agent token in constants.py
- Check network connectivity
- Review agent logs for errors

## 📝 Logging

Server logs are available at: `[project_root]/classroom.db`

Agent events are logged to console and accessible via monitoring endpoints.

## 🔄 Workflow Example

1. **Teacher starts server** on their PC (port 8000)
2. **Students boot up** their PCs and agent starts (port 8001)
3. **Teacher registers workstations** via API or GUI
4. **Teacher applies profiles** (e.g., "Lesson" profile)
5. **Teacher monitors** student PC resources via dashboard
6. **Teacher sends commands** (lock screens, block internet, etc.)
7. **System logs all events** in database
8. **Teacher generates reports** at end of session

## 🚧 Future Enhancements

- [ ] Web-based GUI (React/Vue instead of PyQt6)
- [ ] Real-time WebSocket updates
- [ ] Docker containerization
- [ ] Multi-classroom support
- [ ] Advanced scheduling engine
- [ ] Machine learning for anomaly detection
- [ ] Mobile app for teachers
- [ ] Screenshot capture from student PCs
- [ ] Keyboard/mouse monitoring (with consent)
- [ ] Video recording of student screens
- [ ] Integration with Learning Management Systems (LMS)
- [ ] Multi-language support

## 📄 License

This project is provided as-is for educational purposes.

## 👥 Support

For issues, questions, or contributions, please refer to the project documentation or contact your administrator.

---

**Last Updated**: March 29, 2026
**Version**: 1.0.0 (Beta)
