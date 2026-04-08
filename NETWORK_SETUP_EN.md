# Network Configuration Guide

## Problem
The application was only working on `localhost` and couldn't connect to agents on the local network.

## Solution
The following changes were made:

### 1. **Server Configuration (constants.py)**
- Added `get_local_ip()` function to automatically determine the machine's IP address
- Added `SERVER_IP` variable to use the real IP instead of localhost
- Server now listens on `0.0.0.0` (all interfaces instead of localhost only)

### 2. **API Server (api.py, server/main.py)**
- Updated connection URLs to use `SERVER_IP` instead of `localhost`
- Server starts with `host="0.0.0.0"` to accept connections from any interface

### 3. **Agent Config (agent/config.json)**
- Added `server_url` field to specify server address on the network
- Added `listen_address` field set to `0.0.0.0`

### 4. **GUI Interface**
- Updated all server address references from localhost to SERVER_IP
- Implemented automatic agent discovery on the network
- Added ability to dynamically update the list of connected workstations

### 5. **Agent Discovery (network_discovery.py)**
- Created new module for scanning the local network
- Automatically determines network range based on local IP
- Scans port 8001 to find active agents

## How to Use

### Starting the Server

```bash
# Navigate to project directory
cd /Volumes/ADATA/PROGRAMMING/class-assistant-project/lab_manager

# Install dependencies (if not installed)
pip install -r requirements.txt

# Run GUI application (recommended)
python -m server.gui.main_window

# OR run API server directly
python -m server.api
```

### Running Agent on Each Workstation

On each computer in the classroom:

```bash
# On Windows/Mac/Linux
python -m agent.main

# Or using uvicorn directly
uvicorn agent.main:app --host 0.0.0.0 --port 8001
```

### Automatic Agent Discovery

1. Make sure all agents are running on workstations
2. In GUI application, go to "⚙️ Management" → "🔍 Search agents"
3. Application will automatically find all agents on the network
4. Workstation list will update automatically

### Manual Agent Registration

If automatic discovery doesn't work, specify IP addresses manually:

1. Find IP addresses of all workstations (ping hostname or ipconfig)
2. In `server/gui/control_panel.py` update `workstations_ips` dictionary
3. Restart the application

## Troubleshooting

### Agents Not Discovered

1. **Check connectivity**:
   ```bash
   ping <agent_ip>
   # Should get response
   ```

2. **Check if agents are running**:
   ```bash
   nc -zv <agent_ip> 8001
   # Should output: Connection to <agent_ip> port 8001 [tcp/*] succeeded!
   ```

3. **Check firewall**:
   - Ensure ports 8000 and 8001 are open in firewall
   - Temporarily disable firewall for testing

### Slow Discovery

- Default scan waits 2 seconds per IP
- Speed depends on subnet size and active machines
- For large networks, consider specifying known MAC addresses

## Network Architecture

```
Teacher (GUI) on Server Machine
    ↓ (HTTP on 0.0.0.0:8000)
FastAPI Server (listens on all interfaces)
    ↓ (HTTP on 0.0.0.0:8001 to each agent)
Agents on Workstations
    ↑ (responses and status)
```

## Key Code Changes

1. **constants.py**: Added functions to determine local IP
2. **api.py**: Uses SERVER_IP instead of localhost
3. **server/main.py**: Updated API client connection
4. **agent/config.json**: Can specify server_url
5. **gui/main_window.py**: Implemented agent discovery
6. **gui/control_panel.py**: Dynamic workstation list updates
7. **network_discovery.py**: New module for network scanning

## Security Considerations

⚠️ **Important**: Current configuration uses simple token authentication. For production:

1. Use HTTPS instead of HTTP
2. Implement stronger authentication (OAuth, JWT)
3. Add data encryption in transit
4. Restrict access at network level (VPN, IP whitelist)
5. Add logging and monitoring for all connections

## Testing

```python
# Test agent discovery
from server.network_discovery import discover_agents_sync

agents = discover_agents_sync()
print(f"Found {len(agents)} agents: {agents}")
```

## Support

If you encounter issues:
1. Check console logs
2. Verify all machines are on the same subnet
3. Check firewall settings
4. Contact network administrator

